from player.consumers.game.utils.player import Player
from player.consumers.game.utils.cell import Cell

class SnakePlayer(Player):
    def __init__(self, id, uuid, botId, language, botCode, sx, sy, steps):
        super().__init__(id, uuid, botId, language, botCode)
        # 蛇头
        self.sx = sx
        self.sy = sy
        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]
        # 蛇身相对于蛇头的偏移量
        self.steps = steps
        self.client = None
        self.transport = None

    def getStepsString(self):
        res = ""
        for d in self.steps:
            res += str(d)
        return res

    def getStepsInputString(self):
        res = []
        x = self.sx
        y = self.sy
        res.append([x, y])
        for d in self.steps:
            x += self.dx[d]
            y += self.dy[d]
            res.append([x, y])
        res.reverse()
        ret = ""
        ret += "%d\n" % len(res)
        for item in res:
            ret += "%d %d\n" % (item[0], item[1])
        return ret

    def check_tail_increasing(self, step):
        if step <= 10:
            return True
        return step % 3 == 1

    def getCells(self):
        res = []
        x = self.sx
        y = self.sy
        res.append(Cell(x, y))
        step = 0

        for d in self.steps:
            x += self.dx[d]
            y += self.dy[d]
            res.append(Cell(x, y))
            step += 1
            if not self.check_tail_increasing(step):
                del res[0]
        return res
