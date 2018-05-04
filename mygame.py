import random
import math
import pygame

class Player:

    def __init__(self, window, posn, img):
        self.window = window
        self.windowsize = tuple(window.get_size())
        self.nwPosn = list(posn)
        self.img = img
        self.speed = 7
        self.isUp = False
        self.isDown = False
        self.isLeft = False
        self.isRight = False
    
    def left(self):
        if self.nwPosn[0] > 0:
            self.nwPosn[0] -= self.speed
        else:
            self.nwPosn[0] = 0
    
    def right(self):
        if self.nwPosn[0] < self.windowsize[0] - self.img.get_size()[0]:
            self.nwPosn[0] += self.speed
        else:
            self.nwPosn[0] = self.windowsize[0] - self.img.get_size()[0]
    
    def up(self):
        if self.nwPosn[1] > 0:
            self.nwPosn[1] -= self.speed
        else:
            self.nwPosn[1] = 0
    
    def down(self):
        if self.nwPosn[1] < self.windowsize[1] - self.img.get_size()[1]:
            self.nwPosn[1] += self.speed
        else:
            self.nwPosn[1] = self.windowsize[1] - self.img.get_size()[1]

    def handle(self):
        if self.isUp: self.up()
        if self.isDown: self.down()
        if self.isLeft: self.left()
        if self.isRight: self.right()

    def getCenter(self):
        x = self.nwPosn[0] + self.img.get_size()[0]
        y = self.nwPosn[1] + self.img.get_size()[1]
        return x, y


class Ball:

    def __init__(self, window, img):
        self.window = window
        self.windowsize = tuple(window.get_size())
        self.nwPosn = [random.randint(0, 800), random.randint(0, 600)]
        self.dirn = 2*math.pi*random.random()
        self.img = img
        self.speed = 10
        self.resistance = 0

    def getCenter(self):
        x = self.nwPosn[0] + self.img.get_size()[0]
        y = self.nwPosn[1] + self.img.get_size()[1]
        return x, y
    
    def calcDist(self, playerPosn):
        center = self.getCenter()
        dist2 = (center[0] - playerPosn[0])**2 + (center[1] - playerPosn[1])**2
        return dist2**0.5
    
    def move(self):
        x = self.speed * math.cos(self.dirn)
        y = - self.speed * math.sin(self.dirn)
        self.nwPosn[0] += x
        self.nwPosn[1] += y
    
    def slow(self):
        if self.speed > 0:
            self.speed -= self.resistance
        else:
            self.speed = 0
        self.move()

    def handle(self, playerPosns):
        for playerPosn in playerPosns:
            if self.calcDist(playerPosn) < 50:
                y = playerPosn[1] - self.getCenter()[1]
                angle = math.asin(y / self.calcDist(playerPosn))
                self.dirn = angle
        if self.nwPosn[1] < 0:
            self.dirn = - self.dirn
        if self.nwPosn[1] > self.windowsize[1] - self.img.get_size()[1]:
            self.dirn = - self.dirn
        if self.nwPosn[0] < 0:
            self.dirn = math.pi - self.dirn
            if 200 < self.nwPosn[1] < 400:
                return "R"
        if self.nwPosn[0] > self.windowsize[0] - self.img.get_size()[0]:
            self.dirn = math.pi - self.dirn
            if 200 < self.nwPosn[1] < 400:
                return "L"
        self.move()


pygame.init()
window = pygame.display.set_mode((800, 600))

playerImg = pygame.image.load("player.png")
player1 = Player(window, (5, 100), playerImg)
player2 = Player(window, (600, 100), playerImg)
ballImg = pygame.image.load("ball.png")
ball = Ball(window, ballImg)

while True:
    window.fill((200, 200, 200))
    window.fill((100, 100, 100), (0, 200, 10, 200))
    window.fill((100, 100, 100), (790, 200, 10, 200))
    ev = pygame.event.poll()

    if ev.type == pygame.QUIT:
        pygame.quit()
        break

    if ev.type == pygame.KEYDOWN:
        evKey = ev.dict["key"]

        if evKey == 273: player1.isUp = True
        if evKey == 274: player1.isDown = True
        if evKey == 275: player1.isRight = True
        if evKey == 276: player1.isLeft = True
        if evKey == 119: player2.isUp = True
        if evKey == 115: player2.isDown = True
        if evKey == 100: player2.isRight = True
        if evKey == 97: player2.isLeft = True

    if ev.type == pygame.KEYUP:
        evKey = ev.dict["key"]

        if evKey == 273: player1.isUp = False
        if evKey == 274: player1.isDown = False
        if evKey == 275: player1.isRight = False
        if evKey == 276: player1.isLeft = False
        if evKey == 119: player2.isUp = False
        if evKey == 115: player2.isDown = False
        if evKey == 100: player2.isRight = False
        if evKey == 97: player2.isLeft = False

    result = ball.handle([player1.getCenter(), player2.getCenter()])
    if result == None:
        player1.handle()
        player2.handle()
    elif result == "L":
        print("left wins")
    elif result == "R":
        print("right wins")
    
    window.blit(player1.img, player1.nwPosn)
    window.blit(player2.img, player2.nwPosn)
    window.blit(ball.img, ball.nwPosn)

    pygame.display.flip()
    
    
