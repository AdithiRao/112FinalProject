import pygame
from pygamegame import PygameGame
from player import Player
from customers import *
import random
import copy

#TO ADD
# If customers go off the screen, they get added to the waiting list, which is
# a number at the top of the screen
# Randomly come up with orders for 4 people
# Make a way to keep track of the orders
# Make an orders bar at the top of the screen
# Create a queue to keep track of all the orders
# Pick up and drop customers into seats, which will remove them from the waiting
#list and shift everyone else down one position
# Make the speed at which customers are generated based on what level
#the player is on
# Create graphics for ordering food and waitress holding the food
# Keep score
# Make a timer for how long it takes to get the food to the customers

#Make the characters look different
#Add in sounds for the food being made
#




class Board2(PygameGame):
    def __init__(self):
        super().__init__(self)
        background = pygame.image.load("background2.png")
        self.background = pygame.transform.scale(background, (893, 627))
        self.character = Player(-100,-100)
        self.drawingChar = self.character.image
        self.tables = []
        for x in range(150, 800, 250):
            for y in range(100, 700, 300):
                self.tables.extend([Table(x,y)])
        arrow = pygame.image.load("greenArrow.png")
        arrow = pygame.transform.scale(arrow, (80, 60))
        self.greenArrow = pygame.transform.rotate(arrow, 180)
        self.customers = []
        self.seatedCustomers = []
        self.takenTables = []
        self.notOrderedYet = []
        self.movingCustomer = None
        self.startTime = 0
        self.waitingCustomers = 0
        self.score = 0
        self.level = 1
        pygame.init()
        pygame.mixer.init()


    def mousePressed(self, x, y):
        if -100 < x < 200 and 290 < y < 350:
            print("Move back to kitchen")

    def createOrder(self):
        food = ["steak", "vegSpringRolls", "nachos", "sushi"]
        drinks = ["juice", "water", "coffee"]
        foodDrink = (random.choice(food), random.choice(drinks))
        return foodDrink

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
                        self.notOrderedYet.extend([self.movingCustomer])
                        self.customers.remove(self.movingCustomer) #the waiting customers
                        self.movingCustomer = None

    def moveToTable(self):
        if pygame.mouse.get_pressed()[0]:
            for table in self.tables:
                if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
                and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
                and self.movingCustomer == None:
                    self.character.x = table.x - 370
                    self.character.y = table.y - 300

    def placeOrder(self):
        for customers in self.notOrderedYet:
            order1 = self.createOrder()
            order2 = self.createOrder()
            order3 = self.createOrder()
            order4 = self.createOrder()
            customers.orders = (order1, order2, order3, order4)


    # def scoring(self)
    # if a order is completed, we give them + 10 points / time
    #they took to finish

    def level(self):
        if self.score % 100 == 0: #everytime someone gets 100 points
            self.level += 1 #we make it harder


    def timerFired(self, dt):
        self.startTime += 1
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
                    print(self.waitingCustomers)
            else:
                customer = Customer(0,500)
                self.customers.extend([customer])
        customersSeated = copy.copy(self.seatedCustomers)
        for i in range(len(self.seatedCustomers)):
            self.seatedCustomers[i].time += 1
            if self.seatedCustomers[i].time == 100:
                customersSeated.remove(self.seatedCustomers[i])
                tablesIndex = self.tables.index(self.takenTables[i])
                self.tables[tablesIndex] = Table(self.takenTables[i].x, self.takenTables[i].y)
                self.takenTables.remove(self.takenTables[i])
        self.seatedCustomers = customersSeated


        self.checkIfPicked()
        self.checkIfPlacedOnTable()
        self.moveToTable()
        self.placeOrder()
        #self.level()
        # for group in self.seatedCustomers:


    def redrawAll(self, screen):
        if self.movingCustomer != None:
            screen.blit(self.movingCustomer.image, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
