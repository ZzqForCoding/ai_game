from django.core.cache import cache
from player.consumers.game.utils.snake.snake_player import SnakePlayer
from player.models.player import Player as Player_Model
from record.models.record import Record
from game.models.game import Game as GameModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import random
import threading
import time
import uuid
import re

from player.consumers.game.thrift.code_running_client.code_running_service import CodeRunning
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# 一局游戏一个线程
class Game(threading.Thread):
    # 上右下左四个方向偏移量
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    def __init__(self, rows, cols, inner_walls_count, idA, botA, idB, botB, room_name):
        threading.Thread.__init__(self)
        self.rows = rows
        self.cols = cols
        self.inner_walls_count = inner_walls_count
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

        self.playerA = SnakePlayer(idA, str(uuid.uuid1()), self.botIdA, self.languageA, self.botCodeA, self.rows - 2, 1, [])
        self.playerB = SnakePlayer(idB, str(uuid.uuid1()), self.botIdB, self.languageB, self.botCodeB, 1, self.cols - 2, [])

        self.nextStepA = None
        self.nextStepB = None
        self.lock = threading.Lock()
        self.status = "playing" # waiting -> playing -> overtime/illegal -> end
        self.loser = ""     # all: "平局", A: A输, B: B输
        self.room_name = room_name
        self.channel_layer = get_channel_layer()
        self.isStart = True
        self.round_time = 0
        if self.botIdA == -1 and self.botIdB == -1: self.round_time = 40 # 4s
        else:
            if self.languageA == 'cpp': self.round_time += 10
            else: self.round_time += 20
            if self.languageB == 'cpp': self.round_time += 10
            else: self.round_time += 20

        if botA: threading.Thread(target=self.estabCodeRunningConnect(self.playerA)).start()
        if botB: threading.Thread(target=self.estabCodeRunningConnect(self.playerB)).start()

    def estabCodeRunningConnect(self, player):
        # Make socket
        transport = TSocket.TSocket('120.76.157.21', 20104)
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


    def getMapString(self, t):
        res = ""
        if t == 1:
            for line in self.g:
                res += "".join(map(str, line))
        elif t == 2:
            for line in self.g:
                res += " ".join(map(str, line)) + "\n"
        return res

    def updatePlayerRating(self, player, rating):
        p = Player_Model.objects.get(id=player.id)
        p.rating = rating
        p.save()

    def saveToDataBase(self):
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

        game = GameModel.objects.get(name='绕蛇')
        record = Record.objects.create(
            game = game,
            a_id = self.playerA.id,
            a_is_robot = False if self.botIdA == -1 else True,
            a_language = self.languageA,
            b_id = self.playerB.id,
            b_is_robot = False if self.botIdB == -1 else True,
            b_language = self.languageB,
            a_steps = self.playerA.getStepsString(),
            b_steps = self.playerB.getStepsString(),
            map = self.getMapString(1),
            loser = self.loser
        )
        record.save()


    # 广播给一个房间的玩家的信息
    def sendAllMessage(self, message):
        message['type'] = "group_send_event"

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            message
        )

    def setNextStepA(self, nextStepA):
        self.lock.acquire()
        try:
            self.nextStepA = nextStepA
        finally:
            self.lock.release()

    def setNextStepB(self, nextStepB):
        self.lock.acquire()
        try:
            self.nextStepB = nextStepB
        finally:
            self.lock.release()

    def getInput(self, player):
        me = None
        you = None
        if self.playerA.id == player.id:
            me = self.playerA
            you = self.playerB
        else:
            me = self.playerB
            you = self.playerA

        return self.getMapString(2) +\
                me.getStepsInputString() +\
                you.getStepsInputString()

    def checkResult(self, res):
        try:
            if res == None or len(res) == 0:
                raise Exception("输出为空")
            # 匹配正号或负号和多位数字，+在正则表达式中表示匹配多次所以需要看转义
            if not re.match("^[-\\+]?\\d+$", res):
                raise Exception("非法输出：%s" % res)
            d = int(res)
            if d < 0 or d > 3:
                raise Exception("非法输出：%d" % d)
        except Exception as e:
            return e
        return res


    def runBot(self, player):
        player.client.prepare_data(player.uuid, self.getInput(player))
        res = player.client.run(player.uuid)
        ret = self.checkResult(res)
        if res != ret:
            # 错误提示
            pass
        else:
            if player.id == self.playerA.id:
                self.setNextStepA(int(res))
            else:
                self.setNextStepB(int(res))

    # 接收玩家输入
    def nextStep(self):
        if self.isStart:
            time.sleep(2)
            self.isStart = False
        else:
            time.sleep(0.2)

        if self.playerA.botId != -1:
            threading.Thread(target=self.runBot(self.playerA)).start()
        if self.playerB.botId != -1:
            threading.Thread(target=self.runBot(self.playerB)).start()

        # 接收固定时间内的输入
        for i in range(self.round_time):
            time.sleep(0.1)
            self.lock.acquire()
            try:
                if self.nextStepA != None and self.nextStepB != None:
                    self.playerA.steps.append(self.nextStepA)
                    self.playerB.steps.append(self.nextStepB)
                    return True
            finally:
                self.lock.release()
        return False

    # 判断操作是否有效
    def check_valid(self, cellsA, cellsB):
        n = len(cellsA)
        cell = cellsA[-1]    # 取出头结点
        # 若撞墙，则非法
        if self.g[cell.x][cell.y] == 1:
            return False

        for i in range(n - 1):
            if cellsA[i].x == cell.x and cellsA[i].y == cell.y:
                return False

        for i in range(n - 1):
            if cellsB[i].x == cell.x and cellsB[i].y == cell.y:
                return False

        return True

    # 判断操作是否非法
    def judge(self):
        cellsA = self.playerA.getCells()
        cellsB = self.playerB.getCells()

        validA = self.check_valid(cellsA, cellsB)
        validB = self.check_valid(cellsB, cellsA)
        if not validA or not validB:
            self.status = "illegal"
            if not validA and not validB:
                self.loser = "all"
            elif not validA:
                self.loser = "A"
            else:
                self.loser = "B"

    # 发送玩家的移动信息
    def sendMove(self):
        self.lock.acquire()
        try:
            nsa = self.nextStepA
            nsb = self.nextStepB
            self.nextStepA = None
            self.nextStepB = None
        finally:
            self.lock.release()
        resp = {
            'event': "move",
            'a_direction': nsa,
            'b_direction': nsb,
        }
        self.sendAllMessage(resp)

    # 发送移动结果
    def sendResult(self):
        resp = {
            'event': "result",
            'loser': self.loser,
            'status': self.status
        }
        self.lock.acquire()
        try:
            nsa = self.nextStepA
            nsb = self.nextStepB
        finally:
            self.lock.release()

        if self.status == "overtime":
            if nsa != None:
                self.playerA.steps.append(nsa)
            if nsb != None:
                self.playerB.steps.append(nsb)

        self.saveToDataBase()
        self.sendAllMessage(resp)
        cache.delete_pattern(self.playerA.id)
        cache.delete_pattern(self.playerB.id)

    # 线程入口
    def run(self):
        for i in range(1000):
            if self.nextStep():
                self.judge()
                if self.status == "playing":
                    self.sendMove()
                else:
                    self.sendResult()
                    break
            else:
                self.status = "overtime"
                self.lock.acquire()
                try:
                    nsa = self.nextStepA
                    nsb = self.nextStepB
                finally:
                    self.lock.release()
                if nsa == None and nsb == None:
                    self.loser = "all"
                elif nsa == None:
                    self.loser = "A"
                else:
                    self.loser = "B"

                self.sendResult()
                break
        if self.playerA.botId != -1: self.closeCodeRunningConnect(self.playerA)
        if self.playerB.botId != -1: self.closeCodeRunningConnect(self.playerB)

    # 获取地图
    def getG(self):
        return self.g

    # 判断游戏地图蛇头位置的连通性
    def check_connectivity(self, sx, sy, tx, ty):
        if sx == tx and sy == ty:
            return True
        self.g[sx][sy] = 1

        for i in range(4):
            x = sx + Game.dx[i]
            y = sy + Game.dy[i]
            if x >= 0 and x < self.rows and y >= 0 and y < self.cols and self.g[x][y] == 0:
                if self.check_connectivity(x, y, tx, ty):
                    self.g[sx][sy] = 0
                    return True

        self.g[sx][sy] = 0

    # 生成地图
    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.g[i][j] = 0

        for r in range(self.rows):
            self.g[r][0] = self.g[r][self.cols - 1] = 1

        for c in range(self.cols):
            self.g[0][c] = self.g[self.rows - 1][c] = 1

        count = self.inner_walls_count // 2
        for i in range(count):
            for j in range(1000):
                r = random.randint(1, self.rows - 2)
                c = random.randint(1, self.cols - 2)
                if self.g[r][c] == 1 or self.g[self.rows - 1 - r][self.cols - 1 - c] == 1:
                    continue
                if r == self.rows - 2 and c == 1 or r == 1 and c == self.cols - 2:
                    continue
                self.g[r][c] = self.g[self.rows - 1 - r][self.cols - 1 - c] = 1
                break
        return self.check_connectivity(self.rows - 2, 1, 1, self.cols - 2)

    # 创建地图
    def createMap(self):
        for i in range(1000):
            if self.draw():
                break
