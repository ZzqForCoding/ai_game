from django.core.cache import cache
from player.consumers.game.utils.gobang.gobang_player import GobangPlayer
from player.models.player import Player as Player_Model
from record.models.record import Record
from game.models.game import Game as GameModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import threading
import time
import copy

class Game(threading.Thread):
    def __init__(self, rows, cols, idA, botA, idB, botB, room_name):
        threading.Thread.__init__(self)
        self.rows = rows
        self.cols = cols
        self.g = [[0 for i in range(self.cols)] for i in range(self.rows)]

        self.botIdA = -1
        self.languageA = ""
        self.botCodeA = ""
        if botA:
            self.botIdA = botA.id
            self.languageA = botA.language
            self.botCodeA = botA.content

        self.botIdB = -1
        self.languageB = ""
        self.botCodeB = ""
        if botB:
            self.botIdB = botB.id
            self.languageB = botB.language
            self.botCodeB = botB.content

        self.playerA = GobangPlayer(idA, self.botIdA, self.languageA, self.botCodeA, [])
        self.playerB = GobangPlayer(idB, self.botIdB, self.languageB, self.botCodeB, [])

        self.nextCellA = None
        self.nextCellB = None
        self.lock = threading.Lock()
        self.status = "playing" # waiting -> playing -> overtime/illegal/A win -> end
        self.loser = ""
        self.room_name = room_name
        self.channel_layer = get_channel_layer()
        self.isStart = True
        self.currentRound = self.playerA.id

    def setNextCellA(self, nextCellA):
        self.lock.acquire()
        try:
            self.nextCellA = nextCellA
        finally:
            self.lock.release()

    def setNextCellB(self, nextCellB):
        self.lock.acquire()
        try:
            self.nextCellB = nextCellB
        finally:
            self.lock.release()

    def nextStep(self):
        if self.isStart:
            time.sleep(2)
            self.isStart = False
        else:
            time.sleep(0.2)

        for i in range(60):
            time.sleep(0.1)
            self.lock.acquire()
            try:
                if self.nextCellA != None:
                    self.g[self.nextCellA.x][self.nextCellA.y] = self.currentRound
                    self.playerA.cells.append(self.nextCellA)
                    return True
                elif self.nextCellB != None:
                    self.g[self.nextCellB.x][self.nextCellB.y] = self.currentRound
                    self.playerB.cells.append(self.nextCellB)
                    return True
            finally:
                self.lock.release()
        return False

    def check_valid(self, cell):
        if cell.x < 1 or cell.x > self.rows - 1 or cell.y < 1 or cell.y > self.cols - 1:
            return False
        # if self.g[cell.x][cell.y] != 0:
        #     return False
        return True

    # 判断是否走到非法区域和已下棋区域，并判断是否赢了游戏
    def judge(self):
        cell = None
        if self.currentRound == self.playerA.id:
            cell = self.playerA.cells[-1]
        elif self.currentRound == self.playerB.id:
            cell = self.playerB.cells[-1]

        valid = self.check_valid(cell)
        if not valid:
            self.status = "illegal"
            self.loser = 'A' if self.currentRound == self.playerA.id else 'B'
            return

        # 标记有无输
        flag = False

        # 上
        up = 0
        for i in range(1, 5):
            if cell.y + i <= self.cols - 1 and self.g[cell.x][cell.y + i] == self.g[cell.x][cell.y]:
                up += 1
            else:
                break
        if up == 4:
            flag = True

        # 下
        d = 0
        for i in range(1, 5):
            if cell.y - i >= 1 and self.g[cell.x][cell.y - i] == self.g[cell.x][cell.y]:
                d += 1
            else:
                break

        if d == 4:
            flag = True

        if up + d == 4:
            flag = True

        # 左
        l = 0
        for i in range(1, 5):
            if cell.x - i >= 1 and self.g[cell.x - i][cell.y] == self.g[cell.x][cell.y]:
                l += 1
            else:
                break

        if l == 4:
            flag = True

        # 右
        r = 0
        for i in range(1, 5):
            if cell.x + i <= self.rows - 1 and self.g[cell.x + i][cell.y] == self.g[cell.x][cell.y]:
                r += 1
            else:
                break

        if r == 4:
            flag = True

        if l + r == 4:
            flag = True

        # 左下
        ld = 0
        for i in range(1, 5):
            if cell.x - i >= 1 and cell.y - i >= 1 and self.g[cell.x - i][cell.y - i] == self.g[cell.x][cell.y]:
                ld += 1
            else:
                break

        if ld == 4:
            flag = True

        # 右下
        rd = 0
        for i in range(1, 5):
            if cell.x + i <= self.rows - 1 and cell.y - i >= 1 and self.g[cell.x + i][cell.y - i] == self.g[cell.x][cell.y]:
                rd += 1
            else:
                break
        if rd == 4:
            flag = True

        # 左上
        lu = 0
        for i in range(1, 5):
            if cell.x - i >= 1 and cell.y + i <= self.cols - 1 and self.g[cell.x - i][cell.y + i] == self.g[cell.x][cell.y]:
                lu += 1
            else:
                break

        if lu == 4:
            flag = True

        # 右上
        ru = 0
        for i in range(1, 5):
            if cell.x + i <= self.rows - 1 and cell.y + i <= self.cols - 1 and self.g[cell.x + i][cell.y + i] == self.g[cell.x][cell.y]:
                ru += 1
            else:
                break

        if ru == 4:
            flag = True

        if ld + ru == 4:
            flag = True

        if lu + rd == 4:
            flag = True

        if flag:
            self.status = 'A Win' if self.currentRound == self.playerA.id else 'B Win'
            self.loser = 'B' if self.currentRound == self.playerA.id else 'A'

    def sendAllMessage(self, message):
        message['type'] = "group_send_event"
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            message
        )

    def updatePlayerRating(self, player, rating):
        p = Player_Model.objects.get(id=player.id)
        p.rating = rating
        p.save()

    def saveToDatabase(self):
        ratingA = Player_Model.objects.get(id=self.playerA.id).rating
        ratingB = Player_Model.objects.get(id=self.playerB.id).rating

        if self.loser == "A":
            ratingA -= 2
            ratingB += 5
        elif self.loser == "B":
            ratingA += 5
            ratingB -= 2

        self.updatePlayerRating(self.playerA, ratingA)
        self.updatePlayerRating(self.playerB, ratingB)

        game = GameModel.objects.get(name="五子棋")
        record = Record.objects.create(
            game = game,
            a_id = self.playerA.id,
            a_is_robot = False if self.botIdA == -1 else True,
            a_language = self.languageA,
            b_id = self.playerB.id,
            b_is_robot = False if self.botIdB == -1 else True,
            b_language = self.languageB,
            a_steps = self.playerA.getCellsString(),
            b_steps = self.playerB.getCellsString(),
            loser = self.loser
        )
        record.save()


    def sendNextRound(self):
        self.lock.acquire()
        try:
            nca = copy.deepcopy(self.nextCellA)
            ncb = copy.deepcopy(self.nextCellB)
            self.nextCellA = None
            self.nextCellB = None
        finally:
            self.lock.release()
        resp = {
            'event': "nextRound",
            'x': nca.x if self.currentRound == self.playerA.id else ncb.x,
            'y': nca.y if self.currentRound == self.playerA.id else ncb.y,
            'round': self.currentRound
        }
        self.sendAllMessage(resp)
        if self.currentRound == self.playerA.id:
            self.currentRound = self.playerB.id
        elif self.currentRound == self.playerB.id:
            self.currentRound = self.playerA.id

    def sendResult(self):
        resp = {
            'event': "result",
            'loser': self.loser,
            'status': self.status
        }
        self.lock.acquire()
        try:
            nca = copy.deepcopy(self.nextCellA)
            ncb = copy.deepcopy(self.nextCellB)
        finally:
            self.lock.release()
        if self.status != "overtime":
            resp['x'] = nca.x if self.currentRound == self.playerA.id else ncb.x
            resp['y'] = nca.y if self.currentRound == self.playerA.id else ncb.y
            resp['round'] = self.currentRound
        self.saveToDatabase()
        self.sendAllMessage(resp)
        cache.delete_pattern(self.playerA.id)
        cache.delete_pattern(self.playerB.id)
        # del MultiPlayerGobangGame.users[self.playerA.id]
        # del MultiPlayerGobangGame.users[self.playerB.id]

    def run(self):
        for i in range(400):
            if self.nextStep():
                self.judge()
                if self.status == "playing":
                    self.sendNextRound()
                else:
                    self.sendResult()
                    break
            else:
                self.status = "overtime"
                self.loser = 'A' if self.currentRound == self.playerA.id else 'B'
                self.sendResult()
                break
