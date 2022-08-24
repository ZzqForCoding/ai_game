from player.consumers.game.utils.snake.cell import Cell

class Player:
    def __init__(self, id, botId, botCode, sx, sy, steps):
        self.id = id
        self.botId = botId
        self.botCode = botCode
        # 蛇头
        self.sx = sx
        self.sy = sy
        # 蛇身相对于蛇头的偏移量
        self.steps = steps

    def getStepsString(self):
        res = ""
        for d in self.steps:
            res += str(d)
        return res

    def check_tail_increasing(self, step):
        if step <= 10:
            return True
        return step % 3 == 1

    def getCells(self):
        res = []
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        x = self.sx
        y = self.sy
        res.append(Cell(x, y))
        step = 0

        for d in self.steps:
            x += dx[d]
            y += dy[d]
            res.append(Cell(x, y))
            if not self.check_tail_increasing(++step):
                del res[0]
        return res
