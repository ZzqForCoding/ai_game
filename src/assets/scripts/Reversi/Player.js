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
        this.gamemap.ctx.canvas.addEventListener('click', e => {
            if(this.gamemap.store.state.pk.firstMove !== this.id) return;
            const rect = this.gamemap.ctx.canvas.getBoundingClientRect();
            let x = (e.clientX - rect.left) / this.gamemap.L, y = (e.clientY - rect.top) / this.gamemap.L;
            let r = Math.floor(x), c = Math.floor(y);
            if(this.gamemap.map[r * 10 + c]) return;
            let flag = this.gamemap.adviseChesses.some(chess => chess.r === r && chess.c === c);
            if(flag) this.set_chess(r, c);
        });
        this.gamemap.ctx.canvas.addEventListener("mousemove", e => {
            const rect = this.gamemap.ctx.canvas.getBoundingClientRect();
            let x = (e.clientX - rect.left) / this.gamemap.L, y = (e.clientY - rect.top) / this.gamemap.L;
            this.floatR = Math.floor(x), this.floatC = Math.floor(y);
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

    set_chess(r, c) {
        let chess = new Chess(this.gamemap, {
            color: this.color,
            r,
            c
        });
        // this.gamemap.currentChess = chess;
        this.gamemap.pushChess(chess);
        this.gamemap.process(chess);
        setTimeout(()=>{
            if(this.id === 1) {
                this.gamemap.store.commit("updateFirstMove", 2);
                this.gamemap.adviseChess("black");
            }
            else {
                this.gamemap.store.commit("updateFirstMove", 1);
                this.gamemap.adviseChess("white");
            }
        }, 200)
    }

    render() {
        if(this.gamemap.store.state.pk.firstMove === this.id &&
           this.floatR >= 0 && this.floatR < this.gamemap.rows && this.floatC >= 0 && this.floatC < this.gamemap.cols && !this.gamemap.map[this.floatR * 10 + this.floatC]) {
            const L = this.gamemap.L;
            const ctx = this.gamemap.ctx;

            this.gamemap.canvasUtils.drawRoundedRectangle(ctx, this.floatR * L, this.floatC * L, L, L, L * 0.2, "#1F1F1F", "gray");

            ctx.fillStyle = this.color;
            ctx.beginPath();
            let r = L * 0.31;
            if(this.isClick) r = L * 0.28;
            ctx.arc(this.floatR * L + L / 2.0, this.floatC * L + L / 2.0, r, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}