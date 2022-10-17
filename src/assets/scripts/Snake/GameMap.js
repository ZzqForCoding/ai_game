import { AcGameObject } from "../AcGameObject";
import { Wall } from "./Wall";
import { Snake } from './Snake';

export class GameMap extends AcGameObject {
    constructor(ctx, parent, store) {
        super();

        this.ctx = ctx;
        this.parent = parent;
        this.store = store;
        this.L = 0;
        
        // 两个蛇的坐标是(11, 1) 和 (1, 12), 因为预防两个蛇在同一时间走到同一格子，因此将13 * 13修改成13 * 14，修改了地图大小，因此要将地图的轴对称改成中心对称
        // 一个蛇的横纵坐标之和的奇偶性是：偶奇偶奇偶奇...
        // 另一个蛇的横纵坐标之和的奇偶性是：奇偶奇偶奇偶...
        // 因此在同一时刻不会相遇
        this.rows = 13;
        this.cols = 14;

        this.inner_walls_count = 20;
        this.walls = [];
    }

    create_walls() {
        const g = this.store.state.pk.gamemap;

        for(let r = 0; r < this.rows; r++) {
            for(let c = 0; c < this.cols; c++) {
                if(g[r][c]) {
                    this.walls.push(new Wall(r, c, this));
                }
            }
        }
    }

    start() {
        this.create_walls();
        let selfColor = 0, yourColor = 0;
        if(this.store.state.pk.a_id === this.store.state.user.id) selfColor = "#4876EC", yourColor = "#F94848";
        else selfColor = "#F94848", yourColor = "#4876EC";
        this.snakes = [
            new Snake({id: 0, color: selfColor, r: this.rows - 2, c: 1}, this),
            new Snake({id: 1, color: yourColor, r: 1, c: this.cols - 2}, this),
        ];
        this.add_listening_events();
    }

    transDir(d) {
        if(d <= 1) d += 2;
        else d -= 2;
        return d;
    }

    add_listening_events() {
        if(this.store.state.record.is_record) {
            let k = 0;
            const a_steps = this.store.state.record.a_steps;
            const b_steps = this.store.state.record.b_steps;
            const loser = this.store.state.record.record_loser;
            const [snake0, snake1] = this.snakes;
            const interval_id = setInterval(() => {
                if(k >= a_steps.length - 1) {
                    if(loser === "all" || loser === "A") {
                        snake0.status = "die";
                    }
                    if(loser === "all" || loser === "B") {
                        snake1.status = "die";
                    }   
                    clearInterval(interval_id);
                } else {
                    if(k < a_steps.length) snake0.set_direction(parseInt(a_steps[k]));
                    if(k < b_steps.length) snake1.set_direction(parseInt(b_steps[k]));
                }
                k++;
            }, 300);
        } else {
            this.ctx.canvas.focus();
            this.ctx.canvas.addEventListener("keydown", e => {
                let d = -1, dir;
                if(e.key === 'w') d = 0;
                else if(e.key === 'd') d = 1;
                else if(e.key === 's') d = 2;
                else if(e.key === 'a') d = 3;
                if(this.store.state.user.id !== this.store.state.pk.a_id) {
                    dir = this.transDir(d);
                }
                // else if(e.key === 'ArrowUp') snake1.set_direction(0);
                // else if(e.key === 'ArrowRight') snake1.set_direction(1);
                // else if(e.key === 'ArrowDown') snake1.set_direction(2);
                // else if(e.key === 'ArrowLeft') snake1.set_direction(3);
            
                if(dir >= 0) {
                    this.store.commit("updateDir", d);
                    this.store.state.pk.socket.send(JSON.stringify({
                        event: "move",
                        direction: dir,
                    }));
                }
            });
        }
    }

    update_size() {
        this.L = parseInt(Math.min(this.parent.clientWidth / this.cols, this.parent.clientHeight / this.rows));
        this.ctx.canvas.width = this.L * this.cols;
        this.ctx.canvas.height = this.L * this.rows;
    }

    // 判断两条蛇是否都准备好下一回合
    check_ready() {
        for(const snake of this.snakes) {
            if(snake.status !== 'idle') return false;
            if(snake.direction === -1) return false;
        }
        return true;
    }

    // 让两条蛇进入下一回合
    next_step() {
        for(const snake of this.snakes) {
            snake.next_step();
        }
    }

    check_valid(cell) {    // 检测目标位置是否合法：没有撞到两条蛇的身体和障碍物
        for(const wall of this.walls) {
            if(wall.r === cell.r && wall.c === cell.c) {
                return false;
            }
        }

        for(const snake of this.snakes) {
            let k = snake.cells.length;
            if(!snake.check_tail_increasing()) {    // 当蛇尾会前进的时候，蛇尾不要判断
                k--;
            }
            for(let i = 0; i < k; i++) {
                if(snake.cells[i].r === cell.r && snake.cells[i].c === cell.c) {
                    return false;
                }
            }
        }
        return true;
    }

    update() {
        this.update_size();
        if(this.check_ready()) {
            this.next_step();
        }
        this.render();
    }

    render() {
        const color_even = "#AAD751", color_odd = "#A2D149";
        for(let r = 0; r < this.rows; r++) {
            for(let c = 0; c < this.cols; c++) {
                if((r + c) % 2 === 0) {
                    this.ctx.fillStyle = color_even;
                } else {
                    this.ctx.fillStyle = color_odd;
                }
                this.ctx.fillRect(c * this.L, r * this.L, this.L, this.L);
            }
        }
    }
}
