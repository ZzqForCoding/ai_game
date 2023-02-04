from django.core.cache import cache
from player.consumers.game.utils.cell import Cell
from player.consumers.game.utils.reversi.reversi_player import ReversiPlayer
from player.models.player import Player as Player_Model
from record.models.record import Record
from game.models.game import Game as GameModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import threading
import time
import copy
import uuid
import re
import json

from player.consumers.game.thrift.code_running_client.code_running_service import CodeRunning
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class Game(threading.Thread):
    dx = [-1, -1, -1, 0, 1, 1,  1,  0]
    dy = [-1,  0,  1, 1, 1, 0, -1, -1]

    def __init__(self, rows, cols, idA, botA, idB, botB, room_name):
        threading.Thread.__init__(self)
        self.rows = rows
        self.cols = cols
        self.g = [[0 for i in range(self.cols)] for i in range(self.rows)]
        self.g[3][3] = idA
        self.g[4][4] = idA
        self.g[3][4] = idB
        self.g[4][3] = idB
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

        self.playerA = ReversiPlayer(idA, str(uuid.uuid1()), self.botIdA, self.languageA, self.botCodeA, [Cell(3, 3), Cell(4, 4)])
        self.playerB = ReversiPlayer(idB, str(uuid.uuid1()), self.botIdB, self.languageB, self.botCodeB, [Cell(3, 4), Cell(4, 3)])

        self.nextCellA = None
        self.nextCellB = None
        self.lock = threading.Lock()
        self.status = "playing"     # playing -> illegal/overtime/A Win
        self.loser = ""
        self.room_name = room_name
        self.channel_layer = get_channel_layer()
        self.isStart = True
        self.currentRound = self.playerA.id
        self.toggleRound = False
        self.toggleRoundLock = threading.Lock()

        self.round_time = 50
        # if self.botIdA == -1 and self.botIdB == -1: self.round_time = 40 # 4s
        # else:
        #     if self.languageA == 'cpp': self.round_time += 10
        #     else: self.round_time += 20
        #     if self.languageB == 'cpp': self.round_time += 10
        #     else: self.round_time += 20

        if botA: threading.Thread(target=self.estabCodeRunningConnect(self.playerA)).start()
        if botB: threading.Thread(target=self.estabCodeRunningConnect(self.playerB)).start()

    def estabCodeRunningConnect(self, player):
        # Make socket
        transport = TSocket.TSocket('runner', 9090)
        # Buffering is critical. Raw sockets are very slow
        player.transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(player.transport)
        # Create a client to use the protocol encoder
        player.client = CodeRunning.Client(protocol)
        # Connect!
        player.transport.open()
        # 开启容器
        player.client.start_container(player.uuid, player.botCode, player.language)
        player.client.compile(player.uuid)

    def closeCodeRunningConnect(self, player):
        player.client.stop_container(player.uuid)
        player.transport.close()
        del player.client
        del player.transport

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

    def getInput(self, player):
        me = None
        you = None
        if self.playerA.id == player.id:
            me = self.playerA
            you = self.playerB
        else:
            me = self.playerB
            you = self.playerA
        return me.getCellsInputString() +\
                you.getCellsInputString()

    def checkResult(self, res):
        try:
            if res == None or len(res) == 0:
                raise Exception("输出为空")
            if not re.match("^[-\\+]?\\d+\s{1}[-\\+]?\\d+$", res):
                raise Exception("非法输出：%s" % res)
            a, b = map(int, res.split())
            if a < 1 or a > self.rows - 1 or b < 1 or b > self.cols - 1:
                raise Exception("非法输出：%s" % res)
        except Exception as e:
            return e
        return res

    def runBot(self, player):
        player.client.prepare_data(player.uuid, self.getInput(player))
        res = json.loads(player.client.run(player.uuid))
        if res['returncode'] != 0:
            return
        else:
            res = res['output']
        ret = self.checkResult(res)
        if res != ret:
            # 错误提示
            pass
        else:
            a, b = map(int, res.split())
            cell = Cell(a, b)
            if player.id == self.playerA.id:
                self.setNextCellA(cell)
            else:
                self.setNextCellB(cell)

    # 0: 无输入
    # 1：有输入
    # 2: 跳过回合
    def nextStep(self):
        if self.isStart:
            time.sleep(2)
            self.isStart = False
        else:
            time.sleep(0.2)
        self.toggleRoundLock.acquire()
        try:
            if self.toggleRound:
                print("toggle")
                return 2
        finally:
            self.toggleRoundLock.release()

        if self.currentRound == self.playerA.id and self.playerA.botId != -1:
            threading.Thread(target=self.runBot(self.playerA)).start()
        if self.currentRound == self.playerB.id and self.playerB.botId != -1:
            threading.Thread(target=self.runBot(self.playerB)).start()

        for i in range(self.round_time):
            time.sleep(0.1)
            self.lock.acquire()
            try:
                if self.nextCellA != None:
                    self.g[self.nextCellA.x][self.nextCellA.y] = self.currentRound
                    self.playerA.cells.append(self.nextCellA)
                    return 1
                elif self.nextCellB != None:
                    self.g[self.nextCellB.x][self.nextCellB.y] = self.currentRound
                    self.playerB.cells.append(self.nextCellB)
                    return 1
            finally:
                self.lock.release()
            self.toggleRoundLock.acquire()
            try:
                if self.toggleRound:
                    print("toggle 2")
                    return 2
            finally:
                self.toggleRoundLock.release()
        return 0

    def check_valid(self, cell):
        if cell.x < 0 or cell.x >= self.rows or cell.y < 0 or cell.y >= self.cols:
            return False
        # if self.g[cell.x][cell.y] != 0:
        #     return False
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
        for i in range(8):
            tx = cell.x + Game.dx[i]
            ty = cell.y + Game.dy[i]
            flag = False
            while tx >= 0 and tx < self.rows and ty >= 0 and ty < self.cols and self.g[tx][ty] == enemy:
                tx += Game.dx[i]
                ty += Game.dy[i]
                flag = True
            if flag and tx >= 0 and tx < self.rows and ty >= 0 and ty < self.cols and self.g[tx][ty] == self.currentRound:
                sx = cell.x + Game.dx[i]
                sy = cell.y + Game.dy[i]
                while sx != tx or sy != ty:
                    self.g[sx][sy] = self.currentRound
                    sx += Game.dx[i]
                    sy += Game.dy[i]
                    if self.currentRound == self.playerA.id:
                        self.aCnt += 1
                        self.bCnt -= 1
                    else:
                        self.aCnt -= 1
                        self.bCnt += 1

    def sendAllMessage(self, message):
        message['type'] = "group_send_event"
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            message
        )

    def updatePlayerRating(self, player, rating):
        p = Player_Model.objects.get(user__id=player.id)
        p.rating = rating
        p.save()

    def saveToDatabase(self):
        ratingA = Player_Model.objects.get(user__id=self.playerA.id).rating
        ratingB = Player_Model.objects.get(user__id=self.playerB.id).rating

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
            'round': self.currentRound,
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

    def setToggleRound(self):
        self.toggleRoundLock.acquire()
        try:
            self.toggleRound = True
        finally:
            self.toggleRoundLock.release()

    def run(self):
        try:
            for i in range(60):
                t = self.nextStep()
                if t == 1:
                    self.judge()
                    if self.status == "playing":
                        self.sendNextRound()
                    else:
                        self.sendResult()
                        return
                elif t == 0:
                    print("overtime")
                    self.status = "overtime"
                    self.loser = 'A' if self.currentRound == self.playerA.id else 'B'
                    self.sendResult()
                    return
                elif t == 2:
                    tr = None
                    self.toggleRoundLock.acquire()
                    try:
                        tr = self.toggleRound
                    finally:
                        self.toggleRoundLock.release()
                    if tr:
                        if self.currentRound == self.playerA.id:
                            self.currentRound = self.playerB.id
                        elif self.currentRound == self.playerB.id:
                            self.currentRound = self.playerA.id
                    resp = {
                        'event': "toggleRound"
                    }
                    print("send toggleRound")
                    self.sendAllMessage(resp)
                    time.sleep(1)
                if self.aCnt == 0 or self.bCnt == 0:
                    break
            if self.aCnt > self.bCnt:
                self.status = "A Win"
                self.loser = "B"
            elif self.bCnt > self.aCnt:
                self.status = "B Win"
                self.loser = "A"
            self.sendResult()
        except Exception as e:
            print("except: ", e)
        finally:
            if self.playerA.botId != -1: self.closeCodeRunningConnect(self.playerA)
            if self.playerB.botId != -1: self.closeCodeRunningConnect(self.playerB)

            gameCnt = cache.get('game_cnt', 0)
            if gameCnt > 0:
                cache.set('game_cnt', gameCnt - 1)
