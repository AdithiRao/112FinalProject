import pygame
from pygamegame import PygameGame
from player import Player
from customers import *
import random
import copy


class Board2(PygameGame):
    def __init__(self):
        super().__init__(self)
        background = pygame.image.load("images/background2.png")
        self.background = pygame.transform.scale(background, (893, 627))
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
        self.seatedCustomers = []
        self.takenTables = []
        self.notOrderedYet = dict()
        self.movingCustomer = None
        self.startTime = 0
        self.waitingCustomers = 0
        self.score = 0
        self.level = 1
        self.orders = dict()
        pygame.init()
        pygame.mixer.init()


    def mousePressed(self, x, y):
        if -100 < x < 200 and 290 < y < 350:
            print("Move back to kitchen")

    def createOrder(self):
        food = ["steak", "vegSpringRolls", "nachos", "sushi", "juice", "coffee"]
        choice = random.choice(food)
        return choice

    def checkIfPicked(self):
        if pygame.mouse.get_pressed()[0]:
            for customer in self.customers:
                if customer.x <= pygame.mouse.get_pos()[0] <= customer.x + customer.image.get_size()[0] \
                and customer.y <= pygame.mouse.get_pos()[1] <= customer.y + customer.image.get_size()[1]:
                    self.movingCustomer = customer

    def checkIfPlacedOnTable(self):
        if pygame.mouse.get_pressed()[0]: #mouseButton down event
            if self.movingCustomer != None:
                for table in self.tables:
                    if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
                    and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
                    and table not in self.takenTables and pygame.mouse.get_pressed()[0] == True:
                        table.image = SeatedTable(table.x, table.y).image
                        self.takenTables.extend([table])
                        self.seatedCustomers.extend([self.movingCustomer])
                        self.notOrderedYet[table] = self.movingCustomer
                        self.customers.remove(self.movingCustomer) #the waiting customers
                        self.movingCustomer = None

    def moveToTable(self):
        if pygame.mouse.get_pressed()[0]:
            for table in self.tables:
                if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
                and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
                and self.movingCustomer == None:
                    self.character.x = table.x + 50
                    self.character.y = table.y +20




    # def scoring(self)
    # if a order is completed, we give them + 10 points / time
    #they took to finish

    def levelUp(self):
        if self.score != 0 and self.score % 100 == 0: #everytime someone gets 100 points
            self.level += 1 #we make it harder

    def leaveTable(self):
        customersSeated = copy.copy(self.seatedCustomers)
        for i in range(len(self.seatedCustomers)):
            self.seatedCustomers[i].time += 1
            if self.seatedCustomers[i].time == 10000:
                customersSeated.remove(self.seatedCustomers[i])
                tablesIndex = self.tables.index(self.takenTables[i])
                self.tables[tablesIndex] = Table(self.takenTables[i].x, self.takenTables[i].y)
                self.takenTables.remove(self.takenTables[i])
        self.seatedCustomers = customersSeated

    def createCustomers(self):
        if self.startTime % 100/self.level == 0:
            if self.customers != []:
                if len(self.customers) <= 6:
                    xpos = 0
                    ypos = 500
                    for customer in self.customers: #set of 4 friends
                        if customer.y == ypos:
                            ypos -= 100
                    customer = Customer(xpos, ypos)
                    self.customers.extend([customer])
                else:
                    self.waitingCustomers += 1
            else:
                customer = Customer(0,500)
                self.customers.extend([customer])

    def order(self):
        notOrdered = copy.copy(self.notOrderedYet)
        for table in self.notOrderedYet:
            self.orders[table] = (self.createOrder(), self.createOrder(), \
            self.createOrder(), self.createOrder())
            notOrdered.pop(table)
        self.notOrderedYet = notOrdered


    def timerFired(self, dt):
        self.startTime += 1
        self.levelUp()
        self.createCustomers()
        self.leaveTable()
        self.checkIfPicked()
        self.checkIfPlacedOnTable()
        self.moveToTable()
        self.order()
        #self.level()
        # for group in self.seatedCustomers:


    def redrawAll(self, screen):
        screen.blit(self.background, (-0, 0))
        if self.movingCustomer != None:
            screen.blit(self.movingCustomer.image, (pygame.mouse.get_pos()[0],\
            pygame.mouse.get_pos()[1]))
        for table in self.tables:
            screen.blit(table.image, (table.x, table.y))
        screen.blit(self.greenArrow, (0, 300))
