from player.consumers.game.utils.gobang.cell import Cell
import json

class Player:
    def __init__(self, id, cells):
        self.id = id
        self.cells = cells

    def getCellsString(self):
        res = []
        for cell in self.cells:
            res.append({
                'x': cell.x,
                'y': cell.y
            })
        return json.dumps(res)
