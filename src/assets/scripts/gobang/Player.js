import { AcGameObject } from "../AcGameObject";
import { Chess } from "./Chess";

export class Player extends AcGameObject {
    constructor(gamemap, id, color) {
        super();
        this.gamemap = gamemap;
        this.id = id;
        this.color = color;
    }
    
    start() {
        this.add_listening_events();
    }

    add_listening_events() {
        this.gamemap.ctx.canvas.addEventListener('click', e => {
            if(this.gamemap.currentRound !== this.id) return;
            const rect = this.gamemap.ctx.canvas.getBoundingClientRect();
            let x = (e.clientX - rect.left) / this.gamemap.L, y = (e.clientY - rect.top) / this.gamemap.L;
            let r = Math.round(x), c = Math.round(y);
            if(!this.gamemap.pre_judge(r, c)) {
                return;
            }
            let chess = new Chess(this.gamemap, {
                color: this.color,
                r,
                c
            });
            this.set_chess(chess);
            this.gamemap.isStartTime = false;
            if(this.gamemap.roundTime >= 5) this.gamemap.over_game(this.gamemap.currentRound);
            if(this.gamemap.judge()) {
                this.gamemap.over_game(this.currentChess ^ 3);
            } else {
                this.gamemap.status = "playing";
                this.gamemap.roundTime = 0;
                this.gamemap.isStartTime = true;
                this.gamemap.currentRound ^= 3;
            }
        });
    }

    set_chess(chess) {
        this.gamemap.currentChess = chess;
        this.gamemap.chesses.push(chess);
    }
}