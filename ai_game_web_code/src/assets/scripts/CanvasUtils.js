export class CanvasUtils {
    
    /**
     * 画一个圆角矩形
     * @param {*} x 起始x坐标
     * @param {*} y 起始y坐标
     * @param {*} width 矩形宽度
     * @param {*} height 矩形高度
     * @param {*} r 矩形圆角
     * @param {*} bgcolor 矩形填充颜色
     * @param {*} lineColor 矩形边框颜色
     */
    drawRoundedRectangle(ctx, x, y, width, height, r, bgcolor, lineColor) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + width - r, y);
        ctx.arc(x + width - r, y + r, r, Math.PI * 1.5, Math.PI * 2);
        ctx.lineTo(x + width, y + height - r);
        ctx.arc(x + width - r, y + height - r, r, 0, Math.PI * 0.5);
        ctx.lineTo(x + r, y + height);
        ctx.arc(x + r, y + height - r, r, Math.PI * 0.5, Math.PI);
        ctx.lineTo(x, y + r);
        ctx.arc(x + r, y + r, r, Math.PI, Math.PI * 1.5);
        ctx.fillStyle = bgcolor;
        ctx.strokeStyle = lineColor;
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
    }
    
    /**
     * 画四个圆角
     * @param {*} x 起始x坐标
     * @param {*} y 起始y坐标
     * @param {*} width 矩形宽度
     * @param {*} height 矩形高度
     * @param {*} r 矩形圆角
     * @param {*} bgcolor 矩形填充颜色
     * @param {*} lineColor 矩形边框颜色
     */
     drawAngle(ctx, x, y, width, height, r, bgcolor, lineColor) {
        ctx.beginPath();
        ctx.moveTo(x + width - r, y);
        ctx.arc(x + width - r, y + r, r, Math.PI * 1.5, Math.PI * 2);
        ctx.moveTo(x + width, y + height - r);
        ctx.arc(x + width - r, y + height - r, r, 0, Math.PI * 0.5);
        ctx.moveTo(x + r, y + height);
        ctx.arc(x + r, y + height - r, r, Math.PI * 0.5, Math.PI);
        ctx.moveTo(x, y + r);
        ctx.arc(x + r, y + r, r, Math.PI, Math.PI * 1.5);
        ctx.fillStyle = bgcolor;
        ctx.strokeStyle = lineColor;
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
    }

    /**
     * 画准心
     * @param {*} x 起始x坐标
     * @param {*} y 起始y坐标
     * @param {*} len 准心长度
     * @param {*} lineColor 矩形边框颜色
     */
     drawAim(ctx, x, y, len, lineColor) {
        ctx.beginPath();
    
        ctx.moveTo(x - len - len * 0.4, y);
        ctx.lineTo(x - len * 0.4, y);
    
    
        ctx.moveTo(x, y - len - len * 0.4);
        ctx.lineTo(x, y - len * 0.4);
    
    
        ctx.moveTo(x + len * 0.4, y);
        ctx.lineTo(x + len + len * 0.4, y);
    
    
        ctx.moveTo(x, y + len * 0.4);
        ctx.lineTo(x,y + len + len * 0.4);
        
        ctx.strokeStyle = lineColor;
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
    }

    /**
     * 画虚线圆
     * @param {*} cx 圆心x
     * @param {*} cy 圆心y
     * @param {*} r 圆半径
     * @param {*} dashLength 虚线长度
     * @param {*} lineWidth 虚线宽度
     */
    drawDottedCircle(ctx, cx, cy, r, dashLength, lineColor, lineWidth) {
        let n = r / dashLength;
        let alpha = Math.PI * 2 / n;
        let points = [];
        let i = -1;
      
        while(i < n) {
          let theta = alpha * i, theta2 = alpha * (i + 1);
          points.push({
            x : (Math.cos(theta) * r) + cx, 
            y : (Math.sin(theta) * r) + cy, 
            ex : (Math.cos(theta2) * r) + cx, 
            ey : (Math.sin(theta2) * r) + cy
          });
          i += 2;
        }
      
        ctx.lineWidth = lineWidth;
        ctx.strokeStyle = lineColor;
        ctx.beginPath();
      
        for(let p = 0; p < points.length; p++){
          ctx.moveTo(points[p].x, points[p].y);
          ctx.lineTo(points[p].ex, points[p].ey);
          ctx.stroke();
        }
      
        ctx.closePath();
    }

    // 棋子下完我/对方获胜
    /**
     * 画一个圆角矩形
     * @param {*} x 起始x坐标
     * @param {*} y 起始y坐标
     * @param {*} width 矩形宽度
     * @param {*} height 矩形高度
     * @param {*} r 矩形圆角
     * @param {*} bgcolor 矩形填充颜色
     * @param {*} lineColor 矩形边框颜色
     * @param {*} textColor 文字颜色
     * @param {*} text 文字
     */
    drawRoundedRectangleWithText(ctx, x, y, width, height, r, bgcolor, lineColor, textColor, text) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + width - r, y);
        ctx.arc(x + width - r, y + r, r, Math.PI * 1.5, Math.PI * 2);
        ctx.lineTo(x + width, y + height - r);
        ctx.arc(x + width - r, y + height - r, r, 0, Math.PI * 0.5);
        ctx.lineTo(x + r, y + height);
        ctx.arc(x + r, y + height - r, r, Math.PI * 0.5, Math.PI);
        ctx.lineTo(x, y + r);
        ctx.arc(x + r, y + r, r, Math.PI, Math.PI * 1.5);
        ctx.fillStyle = bgcolor;
        ctx.strokeStyle = lineColor;
        ctx.fill();
        ctx.stroke();
        ctx.closePath();

        ctx.font = "bold 17px Arial,sans-serif";
        ctx.fillStyle = textColor;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(text, x + width / 2, y + height / 2);
  }
}