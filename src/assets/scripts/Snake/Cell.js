export class Cell {
    constructor(r, c) {
        this.r = r;
        this.c = c;
        //将行列转换成坐标
        this.x = c + 0.5;
        this.y = r + 0.5;
    }
}
