import { AcGameObject } from "./AcGameObject";
import { NoticeBoard } from "./NoticeBoard";
import { Player } from './Player';

export class GameMap extends AcGameObject {
    constructor(ctx, parent) {
        super();

        this.ctx = ctx;
        this.parent = parent;

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

        this.preStatus = "";
        this.status = "waiting";  // waiting -> black/white -> judge -> win/lose
        this.currentChess = null;

        this.winChesses = [];
    }

    start() {
        new NoticeBoard(this);
        new Player(this, "white", "zzq", "https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg");
        new Player(this, "black", "zzq", "https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg");
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
        for(let i = 0; i < this.chesses.length; i++) {
            if(this.chesses[i].r === r && this.chesses[i].c === c) {
                return false;
            }
        }
        return true;
    }

    get_chess(r, c) {
        for(let chess of this.chesses) {
            if(chess.r === r && chess.c === c && this.preStatus === chess.color) {
                return chess;
            }
        }
        return null;
    }

    judge() {
        this.preStatus = this.status;
        this.status = "judge";

        let cr = this.currentChess.r, cc = this.currentChess.c;
        // 各个方向的为this.preStatus颜色的子
        let lCnt = 0, luCnt = 0, uCnt = 0, ruCnt = 0, rCnt = 0, rdCnt = 0, dCnt = 0, ldCnt = 0;

        // 左
        let tr = cr, tc = cc - 1;
        while(this.get_chess(tr, tc)) {
            lCnt++;
            tc--;
        }

        // 左上
        tr = cr - 1, tc = cc - 1;
        while(this.get_chess(tr, tc)) {
            luCnt++;
            tr--, tc--;
        }

        // 上
        tr = cr - 1, tc = cc;
        while(this.get_chess(tr, tc)) {
            uCnt++;
            tr--;
        }

        // 右上
        tr = cr - 1, tc = cc + 1;
        while(this.get_chess(tr, tc)) {
            ruCnt++;
            tr--, tc++;
        }

        // 右
        tr = cr, tc = cc + 1;
        while(this.get_chess(tr, tc)) {
            rCnt++;
            tc++;
        }

        // 右下
        tr = cr + 1, tc = cc + 1;
        while(this.get_chess(tr, tc)) {
            rdCnt++;
            tr++, tc++;
        }

        // 下
        tr = cr + 1, tc = cc;
        while(this.get_chess(tr, tc)) {
            dCnt++;
            tr++;
        }

        // 左下
        tr = cr + 1, tc = cc - 1;
        while(this.get_chess(tr, tc)) {
            ldCnt++;
            tr++, tc--;
        }

        // 左4个
        if(lCnt === 4) {
            for(let i = cc - 4; i <= cc; i++) {
                this.winChesses.push(this.get_chess(cr, i));
            }
            this.currentChess = null;
            return false;
        }

        // 左上4个
        if(luCnt === 4) {
            for(let i = cr - 4, j = cc - 4; i <= cr; i++, j++) {
                this.winChesses.push(this.get_chess(i, j));
            }
            this.currentChess = null;
            return false;
        }

        // 上4个
        if(uCnt === 4) {
            for(let i = cr - 4; i <= cr; i++) {
                this.winChesses.push(this.get_chess(i, cc));
            }
            this.currentChess = null;
            return false;
        }

        // 右上4个
        if(ruCnt === 4) {
            for(let i = cr - 4, j = cc + 4; i <= cr; i++, j--) {
                this.winChesses.push(this.get_chess(i, j));
            }
            this.currentChess = null;
            return false;
        }

        // 右4个
        if(rCnt === 4) {
            for(let i = cc; i <= cc + 4; i++) {
                this.winChesses.push(this.get_chess(cr, i));
            }
            this.currentChess = null;
            return false;
        }

        // 右下4个
        if(rdCnt === 4) {
            for(let i = cr, j = cc; i <= cr + 4; i++, j++) {
                this.winChesses.push(this.get_chess(i, j));
            }
            this.currentChess = null;
            return false;
        }

        // 下4个
        if(dCnt === 4) {
            for(let i = cr; i <= cr + 4; i++) {
                this.winChesses.push(this.get_chess(i, cc));
            }
            this.currentChess = null;
            return false;
        }

        // 左下4个
        if(ldCnt === 4) {
            for(let i = cr + 4, j = cc - 4; i >= cr; i--, j++) {
                this.winChesses.push(this.get_chess(i, j));
            }
            this.currentChess = null;
            return false;
        }

        // 横5个
        if(lCnt + rCnt === 4) {
            for(let i = cc - lCnt; i <= cc + rCnt; i++) {
                this.winChesses.push(this.get_chess(cr, i));
            }
            this.currentChess = null;
            return false;
        }

        // 竖5个
        if(uCnt + dCnt === 4) {
            for(let i = cr - uCnt; i <= cr + dCnt; i++) {
                this.winChesses.push(this.get_chess(i, cc));
            }
            this.currentChess = null;
            return false;
        }

        // 正对角线5个
        if(luCnt + rdCnt === 4) {
            for(let i = cr - luCnt, j = cc - luCnt; i <= cr + luCnt; i++, j++) {
                this.winChesses.push(this.get_chess(i, j));
            }
            this.currentChess = null;
            return false;
        }

        // 反对角线5个
        if(ruCnt + ldCnt === 4) {
            for(let i = cr - ruCnt, j = cc + ruCnt; i <= cr + ldCnt; i++, j--) {
                this.winChesses.push(this.get_chess(i, j));
            }
            this.currentChess = null;
            return false;
        }

        setTimeout(() => {
            if(this.preStatus === "black") this.status = "white";
            else if(this.preStatus === "white") this.status = "black"
        }, 500);
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
            this.ctx.beginPath();
            this.ctx.arc(this.currentChess.r * this.L, this.currentChess.c * this.L, this.L * 0.4, 0, Math.PI * 2);
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = this.L * 0.1;
            this.ctx.stroke();
        }

        for(let chess of this.winChesses) {
            this.ctx.beginPath();
            this.ctx.arc(chess.r * this.L, chess.c * this.L, this.L * 0.4, 0, Math.PI * 2);
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = this.L * 0.1;
            this.ctx.stroke();
        }
    }
}