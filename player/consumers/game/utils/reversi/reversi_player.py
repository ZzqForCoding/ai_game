from player.consumers.game.utils.player import Player
import json

class ReversiPlayer(Player):
    def __init__(self, id, botId, language, botCode, cells):
        super().__init__(id, botId, language, botCode)
        self.cells = cells

    def getCellsString(self):
        res = []
        for cell in self.cells:
            res.append({
                'x': cell.x,
                'y': cell.y
            })
        return json.dumps(res)
