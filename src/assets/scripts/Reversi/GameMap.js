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
        this.isShowTips = false;
        this.tipString = "";
        this.aCnt = 2;
        this.bCnt = 2;
    }

    start() {
        this.players = [
            new Player(this, this.store.state.pk.a_id, "white"),
            new Player(this, this.store.state.pk.b_id, "black")
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
        if(this.store.state.record.is_record) {
            let a = 2, b = 2, k = 4;
            const a_steps = JSON.parse(this.store.state.record.a_steps);
            const b_steps = JSON.parse(this.store.state.record.b_steps);
            // const loser = this.store.state.record.record_loser;
            const [player0, player1] = this.players;
            const interval_id = setInterval(() => {
                if(a >= a_steps.length && b >= b_steps.length) {
                    clearInterval(interval_id);
                } else {
                    if(a < a_steps.length && k % 2 === 0) player0.set_chess(a_steps[a].x, a_steps[a].y), a++;
                    else if(b < b_steps.length && k % 2 === 1) player1.set_chess(b_steps[b].x, b_steps[b].y), b++;
                    k++;
                }
            }, 500);
        } else {
            this.adviseChess("white");
        }
    }

    calcChessCnt() {
        let aCnt = 0, bCnt = 0;
        for(let chess of this.chesses) {
            if(chess.color === "white") {
                aCnt++;
            } else {
                bCnt++;
            }
        }
        this.store.commit("updateChessCnt", {
            aCnt,
            bCnt
        });
        this.aCnt = aCnt, this.bCnt = bCnt;
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
                    while(tx >= 0 && tx < this.rows && ty >= 0 && ty < this.cols && this.map[tx * 10 + ty] === enemy) {
                        tx = this.dx[i] + tx, ty = this.dy[i] + ty;
                        flag = true;
                    }
                    if(flag && tx >= 0 && tx < this.rows && ty >= 0 && ty < this.cols && !this.map[tx * 10 + ty]) {
                        let t = {r: tx, c: ty};
                        if(this.adviseChesses[t]) continue;
                        this.adviseChesses.push(t);
                    }
                }
            }
        }
        // 不能操作，跳过(发送给后端)
        if(this.adviseChesses.length === 0) {
            this.isShowTips = true;
            if(this.store.state.pk.firstMove === this.store.state.pk.a_id && this.aCnt === 0 || this.store.state.pk.firstMove === this.store.state.pk.b_id && this.bCnt === 0) {
                this.tipString = "无棋可下，游戏结束";
            } else {
                this.tipString = "无棋可下，跳过回合";
                this.store.state.pk.socket.send(JSON.stringify({
                    event: "toggle_round",
                }));
            }
            setTimeout(() => {
                this.isShowTips = false;
                this.tipString = "";
            }, 3000);
        }
    }

    // 下棋之后的处理
    process(chess) {
        let enemy;
        if(chess.color === "white") enemy = "black";
        else enemy = "white";
        for(let i = 0; i < 8; i++) {
            let tx = chess.r + this.dx[i], ty = chess.c + this.dy[i];
            let flag = false;   // i方向是否有!color棋子
            while(tx >= 0 && tx < this.rows && ty >= 0 && ty < this.cols && this.map[tx * 10 + ty] === enemy) {
                flag = true;
                tx = this.dx[i] + tx, ty = this.dy[i] + ty;
            }
            if(flag && tx >= 0 && tx < this.rows && ty >= 0 && ty < this.cols && this.map[tx * 10 + ty] === chess.color) {
                let sx = chess.r + this.dx[i], sy = chess.c + this.dy[i];
                while(sx !== tx || sy !== ty) {
                    this.updateChess({r: sx, c: sy, color: chess.color});
                    sx = this.dx[i] + sx, sy = this.dy[i] + sy;
                }
            }
        }
    }

    // 判断是否是机器人
    judgeRobot() {
        if(this.store.state.user.id == this.store.state.pk.a_id) {
            if(this.store.state.pk.a_is_robot) return true;
            else return false;
        } else {
            if(this.store.state.pk.b_is_robot) return true;
            else return false;
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

        if(this.store.state.pk.firstMove === this.store.state.user.id && this.store.state.pk.loser === "none" && !this.judgeRobot()) {
            for(let chess of this.adviseChesses) {
                ctx.fillStyle = this.store.state.pk.firstMove === this.store.state.pk.a_id ? "white" : "black";
                this.canvasUtils.drawDottedCircle(ctx, chess.r * L + L / 2.0, chess.c * L + L / 2.0, L * 0.31, L * 0.01, "red", L * 0.03);
                ctx.beginPath();
                ctx.arc(chess.r * L + L / 2.0, chess.c * L + L / 2.0, L * 0.3, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        if(this.isShowTips) {
            this.canvasUtils.drawRoundedRectangle(ctx, 50, this.ctx.canvas.width / 2, 200, 40, 5, "rgba(50, 50, 50, 0.5)", "#666666", "#333333", this.tipString);
        }
    }
}