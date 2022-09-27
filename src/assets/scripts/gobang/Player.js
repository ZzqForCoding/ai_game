import { AcGameObject } from "../AcGameObject";
import { Chess } from "./Chess";

export class Player extends AcGameObject {
    constructor(gamemap, id, color, opaColor) {
        super();
        this.gamemap = gamemap;
        this.id = id;
        this.color = color;
        this.opaColor = opaColor;
        this.floatR = -1;
        this.floatC = -1;
        console.log(this.id, this.color, this.opaColor)
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
                if(!this.gamemap.pre_judge(r, c)) {
                    return;
                }

                this.gamemap.store.state.pk.socket.send(JSON.stringify({
                    event: "next_round",
                    x: c,
                    y: r
                }));
            });
            this.gamemap.ctx.canvas.addEventListener("mousemove", e => {
                const rect = this.gamemap.ctx.canvas.getBoundingClientRect();
                let x = (e.clientX - rect.left) / this.gamemap.L, y = (e.clientY - rect.top) / this.gamemap.L;
                this.floatR = Math.round(x), this.floatC = Math.round(y);
            });
        }
    }

    set_chess(x, y) {
        let chess = new Chess(this.gamemap, {
            color: this.color,
            r: y,
            c: x
        });
        this.gamemap.currentChess = chess;
        this.gamemap.chesses.push(chess);
    }

    render() {
        if(this.gamemap.store.state.pk.firstMove === this.id && this.id === this.gamemap.store.state.user.id && this.gamemap.store.state.pk.loser === 'none' &&
           this.floatR >= 1 && this.floatR < this.gamemap.rows && this.floatC >= 1 && this.floatC < this.gamemap.cols) {
            const L = this.gamemap.L;
            const ctx = this.gamemap.ctx;

            ctx.fillStyle = this.opaColor;
            ctx.beginPath();
            ctx.arc(this.floatR * L, this.floatC * L, L * 0.4, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}