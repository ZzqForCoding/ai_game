from player.consumers.game.utils.snake.player import Player
from record.models.record import Record
from game.models.game import Game as GameModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import random
import threading
import time

# 一局游戏一个线程
class Game(threading.Thread):
    # 上右下左四个方向偏移量
    dx = [-1, 0, 1, 0];
    dy = [0, 1, 0, -1];

    def __init__(self, rows, cols, inner_walls_count, idA, idB, room_name):
        threading.Thread.__init__(self)
        self.rows = rows
        self.cols = cols
        self.inner_walls_count = inner_walls_count
        self.g = [[0 for i in range(self.cols)] for i in range(self.rows)]
        self.playerA = Player(idA, self.rows - 2, 1, [])
        self.playerB = Player(idB, 1, self.cols - 2, [])
        self.nextStepA = None
        self.nextStepB = None
        self.lock = threading.Lock()
        self.status = "playing" # playing -> overtime/illegal
        self.loser = ""     # all: "平局", A: A输, B: B输
        self.room_name = room_name
        self.channel_layer = get_channel_layer()

    def getMapString(self):
        res = ""
        for i in range(self.rows):
            for j in range(self.cols):
                res += str(self.g[i][j])
        return res

    def saveToDataBase(self):
        game = GameModel.objects.get(name='绕蛇')
        record = Record.objects.create(
                game = game,
                a_id = self.playerA.id,
                a_sx = self.playerA.sx,
                a_sy = self.playerA.sy,
                b_id = self.playerB.id,
                b_sx = self.playerB.sx,
                b_sy = self.playerB.sy,
                a_steps = self.playerA.getStepsString(),
                b_steps = self.playerB.getStepsString(),
                map = self.getMapString(),
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

    # 接收玩家输入
    def nextStep(self):
        time.sleep(0.2)

        # 接收5s内的输入
        for i in range(50):
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
            resp = {
                'event': "move",
                'a_direction': self.nextStepA,
                'b_direction': self.nextStepB
            }
            self.sendAllMessage(resp)
            self.nextStepA = None
            self.nextStepB = None
        finally:
            self.lock.release()

    # 发送移动结果
    def sendResult(self):
        resp = {
            'event': "result",
            'loser': self.loser,
            'status': self.status
        }
        self.lock.acquire()
        try:
            if self.status == 'illegal':
                resp['a_direction'] = self.nextStepA
                self.playerA.steps.append(self.nextStepA)
                resp['b_direction'] = self.nextStepB
                self.playerB.steps.append(self.nextStepB)

            else:
                if self.nextStepA != None:
                    resp['a_direction'] = self.nextStepA
                    self.playerA.steps.append(self.nextStepA)
                if self.nextStepB != None:
                    resp['b_direction'] = self.nextStepB
                    self.playerB.steps.append(self.nextStepB)
        finally:
            self.lock.release()
        self.saveToDataBase()
        self.sendAllMessage(resp)

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
                    if self.nextStepA == None and self.nextStepB == None:
                        self.loser = "all"
                    elif self.nextStepA == None:
                        self.loser = "A"
                    else:
                        self.loser = "B"
                finally:
                    self.lock.release()
                self.sendResult()
                break

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
        for r in range(self.rows):
            self.g[r][0] = self.g[r][self.cols - 1] = 1

        for c in range(self.cols):
            self.g[0][c] = self.g[self.rows - 1][c] = 1

        count = self.inner_walls_count // 2
        for i in range(count):
            for j in range(1000):
                r = random.randint(1, self.rows - 2)
                c = random.randint(1, self.cols - 2)
                if self.g[r][c] == 1 or self.g[self.rows - 1 - c][self.cols - 1 - c] == 1:
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
