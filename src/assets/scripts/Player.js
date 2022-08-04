import { AcGameObject } from "./AcGameObject";
import { Chess } from "./Chess";

export class Player extends AcGameObject {
    // 可再添加character(是否是自己), isRobot(是否由机器人代下)两个参数
    constructor(gamemap, color, username, photo) {
        super();
        this.gamemap = gamemap;
        this.color = color;
        this.username = username;
        this.photo = photo;
    }

    start() {
        this.add_listening_events();
    }

    add_listening_events() {
        this.gamemap.ctx.canvas.addEventListener('click', e => {
            if(this.gamemap.status !== this.color) return;
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
            this.gamemap.currentChess = chess;
            this.gamemap.chesses.push(chess);
            this.gamemap.judge();
        });
    }
}