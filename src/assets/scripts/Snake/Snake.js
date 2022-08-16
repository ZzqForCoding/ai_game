import { AcGameObject } from "../AcGameObject";
import { Cell } from "./Cell";

export class Snake extends AcGameObject {
    constructor(info, gamemap) {
        super();

        this.id = info.id;
        this.color = info.color;
        this.gamemap = gamemap;

        // 存放蛇的身体
        this.cells = [new Cell(info.r, info.c)];
        this.next_cell = null;  // 下一步的目标位置

        this.speed = 5;
        this.direction = -1;    // -1表示没有指令，0、1、2、3表示上右下左
        this.status = "idle";   // idle, move, die
    
        this.dr = [-1, 0, 1, 0];
        this.dc = [0, 1, 0, -1];
        this.step = 0;
        this.eps = 1e-2;

        this.eye_direction = 0;
        if(this.id === 1) this.eye_direction = 2;   // 左下角的蛇初始朝上，右上角的蛇初始朝下 

        this.eye_dx = [    // 蛇眼睛不同方向的x偏移量
            [-1, 1],
            [1, 1],
            [1, -1],    // 也可(-1,1)
            [-1, -1]
        ]
        this.eye_dy = [    // 蛇眼睛不同方向的y偏移量
            [-1, -1],
            [-1, 1],
            [1, 1],
            [-1, 1]
        ]
    }

    start() {

    }

    set_direction(d) {
        this.direction = d;
    }

    // 检测当前回合蛇的长度是否增加
    check_tail_increasing() {
        if(this.step <= 10) return true;
        if(this.step % 3 == 1) return true;
        return false;
    }

    // 将蛇状态变为走下一步
    next_step() {
        const d = this.direction;
        this.next_cell = new Cell(this.cells[0].r + this.dr[d], this.cells[0].c + this.dc[d]);
        
        this.eye_direction = d;

        this.direction = -1;
        this.status = "move";
        this.step++;

        // 让蛇在下一回合长一个格子
        const k = this.cells.length;
        for(let i = k; i > 0; i--) {
            this.cells[i] = JSON.parse(JSON.stringify(this.cells[i - 1]));
        }

        if(!this.gamemap.check_valid(this.next_cell)) {
            this.status = "die";
        }
    }

    update_move() {
        // x方向要移动的距离
        const dx = this.next_cell.x - this.cells[0].x;
        // y方向要移动的距离
        const dy = this.next_cell.y - this.cells[0].y;
        // 以x为横轴，y为纵轴的斜边长度
        const distance = Math.sqrt(dx * dx + dy * dy);

        // 若斜边长度足够小，说明不需要移动
        if(distance < this.eps) {
            this.cells[0] = this.next_cell;
            this.next_cell = null;
            this.status = "idle";

            if(!this.check_tail_increasing()) {
                this.cells.pop();
            }
        } else {
            // 需要移动的距离(将ms转成s)
            const move_distance = this.speed * this.timedelta / 1000;
            // 横轴的距离是：这一帧的移动距离 * cos θ = 总移动距离 * 邻边 / 斜边
            this.cells[0].x += move_distance * dx / distance;
            // 纵轴的距离是：这一帧的移动距离 * sin θ = 总移动距离 * 对边 / 斜边
            this.cells[0].y += move_distance * dy / distance;
            // 若不变长,则移动蛇尾到蛇次尾
            if(!this.check_tail_increasing()) {
                const k = this.cells.length;
                // 取出蛇尾后面两个格子
                const tail = this.cells[k - 1], tail_target = this.cells[k - 2];
                // 计算出蛇尾和蛇次尾之间的距离
                const tail_dx = tail_target.x - tail.x;
                const tail_dy = tail_target.y - tail.y;
                tail.x += move_distance * tail_dx / distance;
                tail.y += move_distance * tail_dy / distance;
            }
        }
    }

    update() {
        if(this.status === 'move') {
            this.update_move();
        }
        this.render();
    }

    render() {
        const L = this.gamemap.L;
        const ctx = this.gamemap.ctx;

        ctx.fillStyle = this.color;
        if(this.status === "die") {
            ctx.fillStyle = "white";
        }
        for(const cell of this.cells) {
            ctx.beginPath();
            ctx.arc(cell.x * L, cell.y * L, L / 2 * 0.8, 0, Math.PI * 2);
            ctx.fill();
        }

        // 在每两个相邻的蛇身中填充正方形
        for(let i = 1; i < this.cells.length; i++) {
            const a = this.cells[i - 1], b = this.cells[i];
            // 两个蛇身的横纵之间的正方形边长小于误差就不画
            if(Math.abs(a.x - b.x) < this.eps && Math.abs(a.y - b.y) < this.eps) {
                continue;
            }
            // 若横轴两球之间的正方形边长小于误差，则填充纵轴
            if(Math.abs(a.x - b.x) < this.eps) {
                // 参数分别为：矩形左上角x点，矩形左上角y点，矩形宽度，矩形高度
                ctx.fillRect((a.x - 0.5 + 0.1) * L, Math.min(a.y, b.y) * L, L * 0.8, Math.abs(a.y - b.y) * L);
            } else {
                // 参数分别为：矩形左上角x点，矩形左上角y点，矩形宽度，矩形高度
                ctx.fillRect(Math.min(a.x, b.x) * L, (a.y - 0.5 + 0.1) * L, Math.abs(a.x - b.x) * L, L * 0.8);
            }
        }

        // 画眼睛
        ctx.fillStyle = "black";
        // i表示左眼和右眼
        for(let i = 0; i < 2; i++) {
            const eye_x = (this.cells[0].x + this.eye_dx[this.eye_direction][i] * 0.15) * L;
            const eye_y = (this.cells[0].y + this.eye_dy[this.eye_direction][i] * 0.15) * L;
            ctx.beginPath();
            ctx.arc(eye_x, eye_y, L * 0.05, 0, Math.PI * 2)
            ctx.fill();
        }
    }
}
