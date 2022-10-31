from player.consumers.game.utils.player import Player
import json

class GobangPlayer(Player):
    def __init__(self, id, uuid, botId, language, botCode, cells):
        super().__init__(id, uuid, botId, language, botCode)
        self.cells = cells

    def getCellsString(self):
        res = []
        for cell in self.cells:
            res.append({
                'x': cell.x,
                'y': cell.y
            })
        return json.dumps(res)

    def getCellsInputString(self):
        res = "%d\n" % len(self.cells)
        for cell in self.cells:
            res += "%d %d\n" % (cell.x, cell.y)
        return res
