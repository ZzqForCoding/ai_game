import { AcGameObject } from "../AcGameObject";
import { Player } from './Player';
import { CanvasUtils } from "../CanvasUtils";

export class GameMap extends AcGameObject {
    constructor(ctx, parent, store) {
        super();

        this.ctx = ctx;
        this.parent = parent;
        this.store = store;

        this.rows = 17;
        this.cols = 17;
        this.points = [
            {
                x: 4,
                y: 4
            },
            {
                x: this.rows - 4,
                y: 4
            },
            {
                x: 4,
                y: this.cols - 4
            },
            {
                x: this.rows - 4,
                y: this.cols - 4
            },
        ];

        this.chesses = [];
        this.map = {};
        this.currentChess = null;
        this.canvasUtils = new CanvasUtils();
    }

    start() {
        this.players = [
            new Player(this, this.store.state.pk.a_id, "white"),
            new Player(this, this.store.state.pk.b_id, "black")
        ];
        if(this.store.state.record.is_record) {
            let a = 0, b = 0, k = 0;
            const a_steps = JSON.parse(this.store.state.record.a_steps);
            const b_steps = JSON.parse(this.store.state.record.b_steps);
            // const loser = this.store.state.record.record_loser;
            const [player0, player1] = this.players;
            const interval_id = setInterval(() => {
                if(a >= a_steps.length - 1 && b >= b_steps.length - 1) {
                    clearInterval(interval_id);
                } else {
                    if(a < a_steps.length && k % 2 === 0) player0.set_chess(a_steps[a].x, a_steps[a].y), a++;
                    else if(b < b_steps.length && k % 2 === 1) player1.set_chess(b_steps[b].x, b_steps[b].y), b++;
                    k++;
                }
            }, 500);
        }
    }

    

    update_size() {
        this.L = parseInt(Math.min(this.parent.clientWidth / this.cols, this.parent.clientHeight / this.rows));
        this.ctx.canvas.width = this.L * this.cols;
        this.ctx.canvas.height = this.L * this.rows;
    }

    update() {
        this.update_size();
        this.render();
    }

    pre_judge(r, c) {
        if(r < 1 || r > this.rows - 1 || c < 1 || c > this.cols - 1) return false;
        return true;
    }

    pushChess(chess) {
        this.chesses.push(chess);
        this.map[chess.r * 10 + chess.c] = chess.color;
    }

    render() {
        for(let r = 0; r < this.rows; r++) {
            for(let c = 0; c < this.cols; c++) {
                this.ctx.fillStyle = "rgb(249,215,87)";
                this.ctx.fillRect(c * this.L, r * this.L, this.L, this.L);
                if(r >= 1 && c >= 1 && r < this.rows - 1 && c < this.cols - 1) {
                    this.ctx.strokeStyle = "black";
                    this.ctx.strokeRect(c * this.L, r * this.L, this.L, this.L);
                }
            }
        }
        for(let i = 0; i < this.points.length ; i++) {
            this.ctx.fillStyle = "black";
            this.ctx.beginPath();
            this.ctx.arc(this.points[i].x * this.L, this.points[i].y * this.L, 0.1 * this.L, 0, Math.PI * 2);
            this.ctx.fill();
        }

        if(this.currentChess !== null) {
            // this.ctx.beginPath();
            // this.ctx.arc(this.currentChess.r * this.L, this.currentChess.c * this.L, this.L * 0.4 * 0.9, 0, Math.PI * 2);
            // this.ctx.strokeStyle = "red";
            // this.ctx.lineWidth = this.L * 0.085;
            // this.ctx.stroke();
            this.canvasUtils.drawAngle(this.ctx, this.currentChess.r * this.L - this.L / 2.0, this.currentChess.c * this.L - this.L / 2.0, this.L, this.L, this.L * 0.2, "rgba(255, 255, 255, 0)", "red");
        }

        // for(let chess of this.winChesses) {
        //     this.ctx.beginPath();
        //     this.ctx.arc(chess.r * this.L, chess.c * this.L, this.L * 0.4, 0, Math.PI * 2);
        //     this.ctx.strokeStyle = "red";
        //     this.ctx.lineWidth = this.L * 0.1;
        //     this.ctx.stroke();
        // }
    }
}