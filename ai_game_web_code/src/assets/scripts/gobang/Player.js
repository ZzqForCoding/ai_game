import { AcGameObject } from "../AcGameObject";
import { Chess } from "./Chess";

export class Player extends AcGameObject {
    constructor(gamemap, id, color) {
        super();
        this.gamemap = gamemap;
        this.id = id;
        this.color = color;
        this.floatR = -1;
        this.floatC = -1;
        this.isClick = false;   // 按下则悬浮棋子变小
    }
    
    start() {
        this.add_listening_events();
    }

    update() {
        this.render();
    }

    add_listening_events() {
        if(!this.gamemap.store.state.record.is_record) {
            this.gamemap.ctx.canvas.addEventListener('click', e => {
                if(this.gamemap.store.state.pk.firstMove !== this.id) return;
                const rect = this.gamemap.ctx.canvas.getBoundingClientRect();
                let x = (e.clientX - rect.left) / this.gamemap.L, y = (e.clientY - rect.top) / this.gamemap.L;
                let r = Math.round(x), c = Math.round(y);
                if(!this.gamemap.pre_judge(r, c) || this.gamemap.map[r * 10 + c]) {
                    return;
                }

                this.gamemap.store.state.pk.socket.send(JSON.stringify({
                    event: "next_round",
                    x: r,
                    y: c
                }));
            });
            this.gamemap.ctx.canvas.addEventListener("mousemove", e => {
                const rect = this.gamemap.ctx.canvas.getBoundingClientRect();
                let x = (e.clientX - rect.left) / this.gamemap.L, y = (e.clientY - rect.top) / this.gamemap.L;
                this.floatR = Math.round(x), this.floatC = Math.round(y);
            });
            this.gamemap.ctx.canvas.addEventListener("mousedown", () => {
                this.isClick = true;
            });
            this.gamemap.ctx.canvas.addEventListener("mouseup", () => {
                this.isClick = false;
            });
            this.gamemap.ctx.canvas.addEventListener("mouseout", () => {
                this.floatR = -1, this.floatC = -1;
            });
        }
    }

    set_chess(r, c) {
        let chess = new Chess(this.gamemap, {
            color: this.color,
            r,
            c
        });
        this.gamemap.currentChess = chess;
        this.gamemap.pushChess(chess);
    }

    render() {
        if(this.gamemap.store.state.pk.firstMove === this.id && this.id === this.gamemap.store.state.user.id && this.gamemap.store.state.pk.loser === 'none' &&
           this.floatR >= 1 && this.floatR < this.gamemap.rows && this.floatC >= 1 && this.floatC < this.gamemap.cols && !this.gamemap.map[this.floatR * 10 + this.floatC] &&
           !this.gamemap.judgeRobot()) {
            const L = this.gamemap.L;
            const ctx = this.gamemap.ctx;

            ctx.fillStyle = this.color;
            ctx.beginPath();
            let r = L * 0.39;
            if(this.isClick) r = L * 0.34;
            ctx.arc(this.floatR * L, this.floatC * L, r, 0, Math.PI * 2);
            ctx.fill();

            this.gamemap.canvasUtils.drawAim(ctx, this.floatR * L, this.floatC * L, L * 0.2, "red");
        }
    }
}