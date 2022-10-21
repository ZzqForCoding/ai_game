from django.core.cache import cache
from player.consumers.game.utils.reversi.reversi_player import ReversiPlayer
from player.models.player import Player as Player_Model
from record.models.record import Record
from game.models.game import Game as GameModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import threading
import time
import copy

class Game(threading.Thread):
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    def __init__(self, rows, cols, idA, botA, idB, botB, room_name):
        threading.Thread.__init__(self)
        self.rows = rows
        self.cols = cols
        self.g = [[0 for i in range(self.cols)] for i in range(self.rows)]
        self.aCnt = 2
        self.bCnt = 2

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

        self.playerA = ReversiPlayer(idA, self.botIdA, self.languageA, self.botCodeA, [])
        self.playerB = ReversiPlayer(idB, self.botIdB, self.languageB, self.botCodeB, [])

        self.nextCellA = None
        self.nextCellB = None
        self.lock = threading.Lock()
        self.status = "playing"
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
        self.aCnt += 1

    def setNextCellB(self, nextCellB):
        self.lock.acquire()
        try:
            self.nextCellB = nextCellB
        finally:
            self.lock.release()
        self.bCnt += 1

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
                    self.playerA.cells.append(self.nextCellA)
                    return True
                elif self.nextCellB != None:
                    self.playerB.cells.append(self.nextCellB)
                    return True
            finally:
                self.lock.release()
        return False

    def check_valid(self, cell):
        if cell.x < 0 or cell.x >= self.rows or cell.y < 0 or cell.y >= self.cols:
            return False
        if self.g[cell.x][cell.y] != 0:
            return False
        return True

    def judge(self):
        cell = None
        enemy = -1
        if self.currentRound == self.playerA.id:
            enemy = self.playerB.id
            cell = self.playerA.cells[-1]
        elif self.currentRound == self.playerB.id:
            enemy = self.playerA.id
            cell = self.playerB.cells[-1]

        valid = self.check_valid(cell)
        if not valid:
            self.status = "illegal"
            self.loser = 'A' if self.currentRound == self.playerA.id else 'B'
            return

        # 变换操作
        for i in range(4):
            tx = cell.x
            ty = cell.y
            while self.g[Game.dx[i] + tx][Game.dy[i] + ty] == enemy:
                tx += Game.dx[i]
                ty += Game.dy[i]
            if tx != cell.x or ty != cell.y and self.g[Game.dx[i] + tx][Game.dy[i] + ty] == self.currentRound:
                re_dir = i ^ 2
                if self.currentRound == self.playerA.id:
                    self.aCnt += abs(tx - cell.x) + abs(ty - cell.y)
                elif self.currentRound == self.playerB.id:
                    self.bCnt += abs(tx - cell.x) + abs(ty - cell.y)
                while tx != cell.x or ty != cell.y:
                    self.g[tx][ty] = self.currentRound
                    tx += Game.dx[re_dir]
                    ty += Game.dy[re_dir]

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

        game = GameModel.objects.get(name="黑白棋")
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
            'status': self.status,
        }
        self.lock.acquire()
        try:
            nca = copy.deepcopy(self.nextCellA)
            ncb = copy.deepcopy(self.nextCellB)
        finally:
            self.lock.release()
        if self.status == 'illegal':
            resp['x'] = nca.x if self.currentRound == self.playerA.id else ncb.x
            resp['y'] = nca.y if self.currentRound == self.playerA.id else ncb.y
            resp['round'] = self.currentRound
        self.saveToDatabase()
        self.sendAllMessage(resp)
        cache.delete_pattern(self.playerA.id)
        cache.delete_pattern(self.playerB.id)

    def run(self):
        for i in range(60):
            if self.nextStep():
                self.judge()
                if self.nextCellA != None:
                    self.g[self.nextCellA.x][self.nextCellA.y] = self.currentRound
                elif self.nextCellB != None:
                    self.g[self.nextCellB.x][self.nextCellB.y] = self.currentRound
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
        if self.aCnt > self.bCnt:
            self.status = "A Win"
            self.loser = "B"
        elif self.bCnt > self.aCnt:
            self.status = "B Win"
            self.loser = "A"
        self.sendResult()
