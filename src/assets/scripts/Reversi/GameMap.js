import { AcGameObject } from "../AcGameObject";
import { CanvasUtils } from "../CanvasUtils";
import { Chess } from "./Chess";
import { Player } from "./Player";

export class GameMap extends AcGameObject {
    constructor(ctx, parent, store) {
        super();

        this.ctx = ctx;
        this.parent = parent;
        this.store = store;

        this.rows = 8;
        this.cols = 8;

        this.canvasUtils = new CanvasUtils();
        this.chesses = [];
        this.map = {};
        this.adviseChesses = [];
        this.currentChess = null;
    }

    start() {
        this.players = [
            new Player(this, 1, "white"),
            new Player(this, 2, "black")
        ];
        this.pushChess(new Chess(this, {
            color: "white",
            r: 3,
            c: 3
        }));
        this.pushChess(new Chess(this, {
            color: "white",
            r: 4,
            c: 4
        }));
        this.pushChess(new Chess(this, {
            color: "black",
            r: 3,
            c: 4
        }));
        this.pushChess(new Chess(this, {
            color: "black",
            r: 4,
            c: 3
        }));
        // 左上，上，右上，右，右下，下，左下，左
        this.dx = [-1, -1, -1, 0, 1, 1,  1,  0];
        this.dy = [-1,  0,  1, 1, 1, 0, -1, -1];
        this.store.commit("updateFirstMove", 2);
        this.adviseChess("black");
        this.chessTime = 0;
    }

    update_size() {
        this.L = parseInt(Math.min(this.parent.clientWidth / this.cols, this.parent.clientHeight / this.rows));
        this.ctx.canvas.width = this.L * this.cols;
        this.ctx.canvas.height = this.L * this.rows;
    }

    pushChess(chess) {
        this.chesses.push(chess);
        this.map[chess.r * 10 + chess.c] = chess.color;
    }

    updateChess(chess) {
        this.map[chess.r * 10 + chess.c] = chess.color;
        let t = this.chesses.find(item => item.r === chess.r && item.c === chess.c);
        t.color = chess.color;
    }

    adviseChess(color) {
        this.adviseChesses = [];
        for(let chess of this.chesses) {
            if(chess.color === color) {
                let enemy;
                if(color === "white") enemy = "black";
                else enemy = "white";
                // 遍历8个方向是否有!color
                for(let i = 0; i < 8; i++) {
                    let tx = this.dx[i] + chess.r, ty = this.dy[i] + chess.c;
                    let flag = false;
                    while(this.map[tx * 10 + ty] === enemy) {
                        tx = this.dx[i] + tx, ty = this.dy[i] + ty;
                        flag = true;
                    }
                    if(flag && !this.map[tx * 10 + ty]) {
                        let t = {r: tx, c: ty};
                        if(this.adviseChesses[t]) continue;
                        this.adviseChesses.push(t);
                    }
                }
            }
        }
        // 不能操作，跳过
        if(this.adviseChesses.length === 0) this.store.commit("updateFirstMove", this.store.state.pk.firstMove === 1 ? 2 : 1);
    }

    // 下棋之后的处理
    process(chess) {
        let enemy;
        if(chess.color === "white") enemy = "black";
        else enemy = "white";
        for(let i = 0; i < 8; i++) {
            let tx = chess.r + this.dx[i], ty = chess.c + this.dy[i];
            let flag = false;   // i方向是否有!color棋子
            while(this.map[tx * 10 + ty] === enemy) {
                flag = true;
                tx = this.dx[i] + tx, ty = this.dy[i] + ty;
            }
            if(flag && this.map[tx * 10 + ty] === chess.color) {
                let sx = chess.r + this.dx[i], sy = chess.c + this.dy[i];
                while(sx !== tx || sy !== ty) {
                    this.updateChess({r: sx, c: sy, color: chess.color});
                    sx = this.dx[i] + sx, sy = this.dy[i] + sy;
                }
            }
        }
    }

    update() {
        this.update_size();
        this.render();
    }
    render() {
        const L = this.L;
        const ctx = this.ctx;

        // let margin = this.L * 0.05;
        const color_odd = "#404040", color_even = "#575757";
        for(let r = 0; r < this.rows; r++) {
            for(let c = 0; c < this.cols; c++) {
                this.canvasUtils.drawRoundedRectangle(ctx, c * L, r * L, L, L, L * 0.2, (r + c) % 2 == 0 ? color_even : color_odd, "gray");
            }
        }

        for(let chess of this.adviseChesses) {
            ctx.fillStyle = this.store.state.pk.firstMove === 1 ? "rgba(255, 255, 255)" : "rgba(0, 0, 0)";
            this.canvasUtils.drawDottedCircle(ctx, chess.r * L + L / 2.0, chess.c * L + L / 2.0, L * 0.31, L * 0.01, "yellow");
            ctx.beginPath();
            ctx.arc(chess.r * L + L / 2.0, chess.c * L + L / 2.0, L * 0.3, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}