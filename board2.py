#creates the dining room board, with all of the properties that are appropriate
import pygame
from pygamegame import PygameGame
from player import Player
from customers import *
import random
import copy
import time
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

class Priority(object):
    def __init__(self, time, customer):
        self.priority = time
        self.customer = customer

    def __lt__(self, other):
        return self.priority < other.priority

class Board2(PygameGame):
    def __init__(self):
        super().__init__(self)
        background = pygame.image.load("images/background2.png")
        self.background = pygame.transform.scale(background, (893, 627))
        self.height = 627
        self.width = 893
        self.character = Player(300, 300)
        self.drawingChar = self.character.image
        self.tables = []
        for x in range(150, 800, 250):
            for y in range(100, 700, 300):
                self.tables.extend([Table(x,y)])
        arrow = pygame.image.load("images/greenArrow.png")
        arrow = pygame.transform.scale(arrow, (80, 60))
        self.greenArrow = pygame.transform.rotate(arrow, 180)
        self.customers = []
        self.notSeatedCustomers = []
        self.seatedCustomers = []
        self.takenTables = []
        self.notOrderedYet = dict()
        self.movingCustomer = None
        self.startTime = 0
        self.waitingCustomers = 0
        self.custAtTable = dict()
        self.score = 0
        self.level = 1
        self.orders = dict()
        self.custOrders = dict()
        self.oldX = 300
        self.oldY = 300
        self.customersNames = []
        self.font = pygame.font.SysFont("Courier New", 16)
        self.trashCan = pygame.image.load("images/trashCan.png")
        self.trashCan = pygame.transform.scale(self.trashCan, (100, 80))
        self.orderBar = pygame.Rect((0, self.height-40), (self.width, 40))
        self.tickets = []
        self.names = ["Kelly's group", "Taylor's group", "Andrea's group",
        "Arman's group", "Chaya's group", "Austin's group", "Kyle's group",
        "Christina's group", "Gabriella's group"]
        self.nameIndex = 0
        self.queue = Q.PriorityQueue()
        customer1 = Customer(0,450, time.time())
        self.getNameOfCustomer(customer1)
        self.customers.extend([customer1])
        self.queue.put(Priority(time.time(), customer1.name))
        pygame.init()
        pygame.mixer.init()

    def createOrder(self):
        food = ["steak", "springRolls", "nachos", "sushi", "juice", "coffee"]
        choice = random.choice(food)
        return choice

    def checkIfPicked(self, background):
        if pygame.mouse.get_pressed()[0] and background == True:
            for customer in self.customers:
                if customer.x <= pygame.mouse.get_pos()[0] <= customer.x + customer.image.get_size()[0] \
                and customer.y <= pygame.mouse.get_pos()[1] <= customer.y + customer.image.get_size()[1]:
                    self.movingCustomer = customer
                    self.movingCustomer.startTime = customer.startTime

    def checkIfPlacedOnTable(self, background):
        if pygame.mouse.get_pressed()[0] and background == True and self.movingCustomer != None:
            for i in range(len(self.tables)):
                table = self.tables[i]
                if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
                and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
                and table not in self.takenTables and pygame.mouse.get_pressed()[0] == True:
                    table.image = SeatedTable(table.x, table.y).image
                    mCIndex = self.customers.index(self.movingCustomer)
                    self.customers[mCIndex].endTime = time.time()
                    end = self.customers[mCIndex].endTime
                    start = self.movingCustomer.startTime
                    table.startTime = [time.time(), end-start]
                    self.custAtTable[table] = self.customers[mCIndex].name
                    self.takenTables.extend([table])
                    self.seatedCustomers.extend([self.movingCustomer])
                    self.notOrderedYet[table] = self.movingCustomer
                    self.customers.remove(self.movingCustomer) #the waiting customers
                    self.movingCustomer = None

    def moveToTable(self, background):
        if pygame.mouse.get_pressed()[0] and background == True:
            for table in self.tables:
                if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
                and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
                and self.movingCustomer == None:
                    self.character.x = table.x + 50
                    self.character.y = table.y +20

    def levelUp(self):
        if self.score != 0 and self.score % 20 == 0: #everytime someone gets 20 points
            self.level += 1 #we make it harder

    def getNameOfCustomer(self, customer):
        customer.name = self.names[self.nameIndex]
        if self.nameIndex < len(self.names)-1:
            self.nameIndex += 1
        else:
            self.nameIndex = 0

    def createCustomers(self):
        xpos = 0
        ypos = 450
        for i in range(len(self.customers)):
            if i <= 5 and self.customers[i].y != ypos:
                self.customers[i].y = ypos
            ypos -= 100
        if self.startTime % 90/self.level == 0:
            if self.customers != []:
                if len(self.customers) <= 5:
                    ypos = 450
                    for customer in self.customers: #set of 4 friends
                        if customer.y == ypos:
                            ypos -= 100
                    customer = Customer(xpos, ypos, time.time())
                    self.getNameOfCustomer(customer)
                    self.queue.put(Priority(time.time(), customer.name))
                    self.customers.extend([customer])
                else:
                    customer = Customer(xpos, ypos, time.time())
                    self.getNameOfCustomer(customer)
                    self.queue.put(Priority(time.time(), customer.name))
                    self.customers.extend([customer])
                    ypos -= 100

    def order(self):
        notOrdered = copy.copy(self.notOrderedYet)
        for table in self.notOrderedYet:
            self.orders[table] = [self.createOrder(), self.createOrder(), \
            self.createOrder(), self.createOrder()]
            self.custOrders[self.custAtTable[table]] = self.orders[table]
            del notOrdered[table]
        self.notOrderedYet = notOrdered

    def timerFired(self, dt, background):
        self.startTime += 1
        if len(self.customers) <= 5:
            self.waitingCustomers = 0
        else:
            self.waitingCustomers = len(self.customers) - 5
        self.levelUp()
        self.createCustomers()
        self.checkIfPicked(background)
        self.checkIfPlacedOnTable(background)
        self.order()
        self.moveToTable(background)

    #citation: https://www.pygame.org/wiki/TextWrap
    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
        y = rect.top
        lineSpacing = -2
        fontHeight = font.size("Tg")[1]
        while text:
            i = 1
            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break
            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1
            if bkg: # render the line and blit it to the surface
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[i:] # remove the text we just blitted
        return text

    def ticketCreation(self, screen):
        num = 1
        rectLeft = 0
        rectTop = self.height - 80
        for table in self.takenTables:
            if table in self.orders:
                outputString = str(self.orders[table][0])
                for item in self.orders[table][1:]:
                    outputString += ", " + str(item)
                text = str(self.custAtTable[table]) + " #" +str(num) + ": "+ outputString
                text_rect = pygame.Rect((rectLeft+ 10, rectTop + 25), (80, 200))
                ticketImage = pygame.image.load("images/ticket.png")
                ticketImage = pygame.transform.scale(ticketImage, (100, 80))
                screen.blit(ticketImage, (rectLeft, rectTop))
                self.drawText(screen, text, (0, 0, 0), text_rect, self.font)
                self.tickets.extend([(table, screen, text, (0,0,0), text_rect, self.font)])
                rectLeft += 90
                num+= 1

    def redrawAll(self, screen):
        background = pygame.image.load("images/background2.png")
        self.background = pygame.transform.scale(background, (893, 627))
        screen.blit(self.background, (-0, 0))
        pygame.draw.rect(screen, (0,102,204), self.orderBar)
        if self.movingCustomer != None:
            screen.blit(self.movingCustomer.image, (pygame.mouse.get_pos()[0],\
            pygame.mouse.get_pos()[1]))
        for table in self.tables:
            screen.blit(table.image, (table.x, table.y))
        for table in self.takenTables:
            text = self.font.render(str(self.custAtTable[table]), True, \
            (0, 0, 0)) #black
            text_rect = text.get_rect()
            text_rect.right = table.x + 135
            text_rect.y = table.y
            screen.blit(text, text_rect)
        self.ticketCreation(screen)
        screen.blit(self.greenArrow, (0, 300))
        screen.blit(self.trashCan, (780, 300))
