import pygame
from pygamegame import PygameGame
from board1 import *
from board2 import *
from player import *
from customers import *
from startScreen import *
import math
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q


class runGame(PygameGame):
    def __init__(self):
        super().__init__(self)
        self.background0 = True
        self.background1 = False
        self.background2 = False
        self.justStarted = True
        self.startedPlaying = False
        self.kitchen = Board1()
        self.dining = Board2()
        self.startScreen = startScreen()
        self.customers = []
        self.collectMoneyTables = []
        self.background = self.kitchen.background
        self.drawingChar = self.kitchen.drawingChar
        self.character = self.kitchen.character
        (self.character.x, self.character.y) = (self.kitchen.character.x, self.kitchen.character.y)
        self.character.arm1 = self.kitchen.character.arm1
        self.character.arm2 = self.kitchen.character.arm2
        self.greenArrow = self.kitchen.greenArrow
        self.font = pygame.font.SysFont("Courier New", 24)
        self.highScore = self.startScreen.highScore
        pygame.init()

    def trash(self):
        if self.character.arm1 != None:
            self.character.arm1 = None
        if self.character.arm2 != None:
            self.character.arm2 = None
        self.drawingChar = pygame.image.load("images/fullcharacter.png")
        self.kitchen.character.holding = []
        self.character.holding = []

    def mousePressed(self, x, y):
        if self.background1 == True:
            if 800 < x < 880 and 290 < y < 350: #green Arrow placement
                self.background1 = False
                self.background2 = True
                pygame.mixer.stop()
                self.playMusic()
        elif self.background2 == True:
            if -100 < x < 100 and 290 < y < 350:  #green Arrow placement
                self.background1 = True
                self.background2 = False
                pygame.mixer.stop()
                self.playMusic()
            elif 780 < x < 880 and 300 < y < 380:
                self.trash()
            self.extendTableCarrying()
            self.placeOnTable()
            self.place()
            self.collectMoney()

    def extendTableCarrying(self):
        for table in self.dining.takenTables:
            if self.canBePlaced(table):
                if self.kitchen.images[self.character.arm1] in \
                self.dining.orders[table] and len(self.character.holding) == 1:
                    table.carrying.extend([self.character.arm1])
                elif len(self.character.holding) == 2 \
                and self.kitchen.images[self.character.arm1] in self.dining.orders[table] and \
                self.kitchen.images[self.character.arm2] not in self.dining.orders[table]:
                    table.carrying.extend([self.character.arm1])
                elif len(self.character.holding) == 2 \
                and self.kitchen.images[self.character.arm2] in self.dining.orders[table] and \
                self.kitchen.images[self.character.arm1] not in self.dining.orders[table]:
                    table.carrying.extend([self.character.arm2])
                elif len(self.character.holding) == 2 \
                and self.kitchen.images[self.character.arm2] in self.dining.orders[table] and \
                self.kitchen.images[self.character.arm1] in self.dining.orders[table]:
                    if self.kitchen.images[self.character.arm1] == self.kitchen.images[self.character.arm2] \
                    and self.dining.orders[table].count(self.kitchen.images[self.character.arm1]) == 1:
                        table.carrying.extend([self.character.arm2])
                    else:
                        table.carrying.extend([self.character.arm1])
                        table.carrying.extend([self.character.arm2])

    def canBePlaced(self, table):
        if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
        and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
        and self.dining.movingCustomer == None and self.character.arm1 != None:
            return True
        return False

    def oneArmImage(self, table, removeValue):
        self.dining.orders[table].remove(self.kitchen.images[removeValue])
        self.kitchen.character.holding.remove(self.kitchen.images[removeValue])
        self.character.arm2 = None
        imageOneArm = pygame.image.load("images/character1ArmUp.png")
        self.kitchen.character.imageOneArm = pygame.transform.scale(imageOneArm, (125, 150))
        self.kitchen.drawingChar = self.kitchen.character.imageOneArm

    def noArmImage(self):
        self.kitchen.character.image = pygame.image.load("images/fullcharacter.png")
        self.kitchen.drawingChar = self.kitchen.character.image

    def place(self):
        takenTables = copy.copy(self.dining.takenTables)
        for table in self.dining.takenTables:
            if self.canBePlaced(table):
                if self.kitchen.images[self.character.arm1] in \
                self.dining.orders[table] and len(self.character.holding) == 1:
                    self.dining.orders[table].remove(self.kitchen.images[self.character.arm1])
                    self.kitchen.character.holding.remove(self.kitchen.images[self.character.arm1])
                    self.character.arm1 = None
                    self.noArmImage()
                elif len(self.character.holding) == 2 \
                and self.kitchen.images[self.character.arm1] in self.dining.orders[table] and \
                self.kitchen.images[self.character.arm2] not in self.dining.orders[table]:
                    self.character.arm1, self.character.arm2 = self.character.arm2, \
                    self.character.arm1 #shift hands
                    self.oneArmImage(table, self.character.arm2)
                elif len(self.character.holding) == 2 \
                and self.kitchen.images[self.character.arm2] in self.dining.orders[table] and \
                self.kitchen.images[self.character.arm1] not in self.dining.orders[table]:
                    self.oneArmImage(table, self.character.arm2)
                elif len(self.character.holding) == 2 \
                and self.kitchen.images[self.character.arm2] in self.dining.orders[table] and \
                self.kitchen.images[self.character.arm1] in self.dining.orders[table]:
                    if self.kitchen.images[self.character.arm1] == self.kitchen.images[self.character.arm2] \
                    and self.dining.orders[table].count(self.kitchen.images[self.character.arm1]) == 1:
                        self.oneArmImage(table, self.character.arm2)
                    else:
                        self.dining.orders[table].remove(self.kitchen.images[self.character.arm1])
                        self.dining.orders[table].remove(self.kitchen.images[self.character.arm2])
                        self.kitchen.character.holding.remove(self.kitchen.images[self.character.arm1])
                        self.kitchen.character.holding.remove(self.kitchen.images[self.character.arm2])
                        self.character.arm1 = None
                        self.character.arm2 = None
                        self.noArmImage()
                if self.dining.orders[table] == []:
                    del self.dining.orders[table]
                    diningTickets = copy.copy(self.dining.tickets)
                    for ticket in self.dining.tickets:
                        if ticket[0] == table:
                            diningTickets.remove(ticket)
                    self.dining.tickets = diningTickets

    def placeOnTable(self):
        for table in self.dining.takenTables:
            x = -40
            for item in table.carrying:
                item = pygame.image.load(item)
                item = pygame.transform.scale(item, (20, 20))
                table.image.blit(item, ((table.image.get_size()[0])//2\
                + x, (table.image.get_size()[1])//2 - 20))
                x += 20
        for i in range(len(self.dining.takenTables)):
            if len(self.dining.takenTables[i].carrying) == 4:
                self.dining.takenTables[i].eating = True

    def customersLeaveTable(self):
        takenTables = []
        for i in range(len(self.dining.takenTables)):
            if self.dining.takenTables[i].eating == True:
                self.dining.seatedCustomers[i].time += 1
                if self.dining.seatedCustomers[i].time == 20:
                    self.dining.seatedCustomers.remove(self.dining.seatedCustomers[i])
                    tablesIndex = self.dining.tables.index(self.dining.takenTables[i])
                    self.dining.tables[tablesIndex] = Table(self.dining.takenTables[i].x, \
                    self.dining.takenTables[i].y)
                    self.collectMoneyTables.extend([self.dining.tables[tablesIndex]])
                    collectMoneyI = self.collectMoneyTables.index(self.dining.tables[tablesIndex])
                    self.collectMoneyTables[collectMoneyI].startTime = \
                    self.dining.takenTables[i].startTime
                    self.collectMoneyTables[collectMoneyI].endTime = time.time()
                else:
                    takenTables.extend([self.dining.takenTables[i]])
            else:
                takenTables.extend([self.dining.takenTables[i]])
        self.dining.takenTables = takenTables

    def collectMoney(self):
        moneyTables = copy.copy(self.collectMoneyTables)
        for table in self.collectMoneyTables:
            if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
            and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
            and self.dining.movingCustomer == None:
                self.character.x = table.x + 50
                self.character.y = table.y +20
                moneyTables.remove(table)
                self.dining.score += self.scoreFromOrder(table)
        self.collectMoneyTables = moneyTables

    def scoreFromOrder(self, table):
        timeTaken = table.endTime - table.startTime[0] + table.startTime[1]
        score = math.floor(1000/timeTaken)
        return score

    def drawMoney(self, screen):
        for table in self.collectMoneyTables:
            image = pygame.image.load("images/money.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, ((2*table.x + table.image.get_size()[0])//2, \
            (2*table.y + table.image.get_size()[1])//2 -20))

    def timerFired(self, dt):
        self.kitchen.timerFired(dt)
        self.dining.timerFired(dt, self.background2)
        self.drawingChar = self.kitchen.drawingChar
        self.character.holding = self.kitchen.character.holding
        if self.background1 == True:
            (self.character.x, self.character.y) = (self.kitchen.character.x, self.kitchen.character.y)
        elif self.background2 == True:
            (self.character.x, self.character.y) = (self.dining.character.x, self.dining.character.y)
            self.character.arm1 = self.kitchen.character.arm1
            self.character.arm2 = self.kitchen.character.arm2
            self.customersLeaveTable()
        self.customers = self.dining.customers

    def playMusic(self):
        if self.background1 == True:
            pygame.mixer.init()
            music = pygame.mixer.Sound("music.wav")
            music.play(-1,0)
        else:
            pygame.mixer.init()
            music = pygame.mixer.Sound("music2.wav")
            music.play(-1,0)


    def scoreAndWaiting(self, screen):
        text = self.font.render("Score: " + str(self.dining.score), True, (255, 0, 0)) #red
        text_rect = text.get_rect()
        text_rect.right = screen.get_rect().right - 10
        text_rect.y = 10
        screen.blit(text, text_rect)
        text2 = self.font.render("Waiting Outside: " + str(self.dining.waitingCustomers), True, (0, 255, 0))
        text2_rect = text.get_rect()
        text2_rect.right = screen.get_rect().right - 300
        text2_rect.y = 10
        screen.blit(text2, text2_rect)

    def drawCharacter(self, screen):
        if self.character.arm1 == None and self.character.arm2 == None:
            self.kitchen.drawingChar = pygame.image.load("images/fullcharacter.png")
            screen.blit(self.drawingChar, (self.character.x, self.character.y))
        elif self.character.arm1 != None and self.character.arm2 == None:
            food1 = pygame.image.load(self.character.arm1)
            food1 = pygame.transform.scale(food1, (40,40))
            self.kitchen.drawingChar.blit(food1, (60, 20))
            screen.blit(self.drawingChar, (self.character.x, self.character.y))
            imageOneArm = pygame.image.load("images/Character1ArmUp.png")
            self.kitchen.character.imageOneArm = pygame.transform.scale(imageOneArm, (125, 150))
            self.kitchen.drawingChar = self.kitchen.character.imageOneArm
        elif self.character.arm2 != None:
            food1 = pygame.image.load(self.character.arm1)
            food2 = pygame.image.load(self.character.arm2)
            food1 = pygame.transform.scale(food1, (40, 40))
            food2 = pygame.transform.scale(food2, (40, 40))
            self.kitchen.drawingChar.blit(food1, (80, 20))
            self.kitchen.drawingChar.blit(food2, (20, 20))
            screen.blit(self.drawingChar, (self.character.x, self.character.y))
            imageTwoArm = pygame.image.load("images/Character2ArmsUp.png")
            self.kitchen.character.imageTwoArm = pygame.transform.scale(imageTwoArm, (150, 150))
            self.kitchen.drawingChar = self.kitchen.character.imageTwoArm


    def redrawAll(self, screen):
        if self.background0:
            self.startScreen.redrawAll(screen)
        elif self.background2:
            self.dining.redrawAll(screen)
            for customer in self.customers:
                screen.blit(customer.image, (customer.x, customer.y))
            self.drawMoney(screen)
        elif self.background1:
            self.kitchen.redrawAll(screen)
            pygame.draw.rect(screen, (0,102,204), self.dining.orderBar)
            for ticket in self.dining.tickets:
                rectLeft = ticket[4].left - 10
                rectTop = ticket[4].top - 25
                ticketImage = pygame.image.load("images/ticket.png")
                ticketImage = pygame.transform.scale(ticketImage, (100, 80))
                screen.blit(ticketImage, (rectLeft, rectTop))
                self.dining.drawText(ticket[1], ticket[2], ticket[3], ticket[4], ticket[5])
        if self.background1 or self.background2:
            self.scoreAndWaiting(screen)
            self.drawCharacter(screen)

    def updateScore(self, filename):
        with open(filename, "rt") as f:
            pastScore = 0
            for line in f:
                pastScore = int(line[::])
                if self.dining.score > pastScore:
                    pastScore = self.dining.score
        with open(filename, "wt") as w:
            w.write(str(pastScore))

    #from 112 notes
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Diner Dash!")
        self.init()
        self.playMusic()
        self._keys = dict()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.background1 == True:
                        self.kitchen.mousePressed(*(event.pos))
                        self.mousePressed(*(event.pos))
                    else:
                        self.dining.mousePressed(*(event.pos))
                        self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.background1 == True:
                        self.kitchen.mouseReleased(*(event.pos))
                    else:
                        self.dining.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    if self.background1 == True:
                        self.kitchen.mouseMotion(*(event.pos))
                    else:
                        self.dining.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    if self.background1 == True:
                        self.kitchen.mouseDrag(*(event.pos))
                    else:
                        self.dining.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    if self.background1 == True:
                        self.kitchen._keys[event.key] = True
                        self.kitchen.keyPressed(event.key, event.mod)
                    else:
                        self.dining._keys[event.key] = True
                        self.dining.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    if self.background1 == True:
                        self.kitchen._keys[event.key] = False
                        self.kitchen.keyReleased(event.key, event.mod)
                    else:
                        self.dining._keys[event.key] = False
                        self.dining.keyReleased(event.key, event.mod)
            self.redrawAll(screen)
            pygame.display.flip()

        self.updateScore("scores.txt")
        pygame.quit()

def main():
    game = runGame()
    game.run()

if __name__ == "__main__":
    main()
