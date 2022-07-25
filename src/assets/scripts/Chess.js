import { AcGameObject } from "./AcGameObject";

export class Chess extends AcGameObject {
    constructor(gamemap, info) {
        super();
        this.gamemap = gamemap;
        this.color = info.color;
        this.r = info.r;
        this.c = info.c;
    }

    update() {
        this.render();
    }

    render() {
        const L = this.gamemap.L;
        const ctx = this.gamemap.ctx;

        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.c * L, this.r * L, L * 0.5, 0, Math.PI * 2);
        ctx.fill();
    }
}