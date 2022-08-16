import { AcGameObject } from "../AcGameObject";

export class NoticeBoard extends AcGameObject {
    constructor(gamemap) {
        super();
        this.gamemap = gamemap;
        this.text = "即将开始：3";
        this.time = 3;
    }

    start() {
    }

    update() {
        this.render();
        if(this.gamemap.status === "waiting") {
            this.time -= this.timedelta / 1000;
            this.write("即将开始：" + parseInt(this.time));
        }
        if(this.time <= 0) {
            this.gamemap.status = "black";
            this.destroy();
        }
    }

    write(text) {
        this.text = text;
    }

    render() {
        const L = this.gamemap.L;
        const ctx = this.gamemap.ctx;
        ctx.font = "13px serif";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText(this.text, this.gamemap.cols / 2 * L, 15);
    }
}
