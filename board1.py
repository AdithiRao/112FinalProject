import pygame
from pygamegame import PygameGame
from player import Player
import time
import copy
import string
from colour import Color
import math


class Board1(PygameGame):
    def __init__(self):
        super().__init__(self)
        background = pygame.image.load("images/background1.png")
        self.background = pygame.transform.scale(background, (893, 627))
        self.character = Player(300,300)
        self.drawingChar = pygame.image.load("images/fullcharacter.png")
        self.greenArrow = pygame.image.load("images/greenArrow.png")
        self.greenArrow = pygame.transform.scale(self.greenArrow, (80, 60))
        self.trashCan = pygame.image.load("images/trashCan.png")
        self.trashCan = pygame.transform.scale(self.trashCan, (100, 80))
        self.pan1 = False
        self.pan2 = False
        self.beingCooked = [None, None]
        self.inAction = []
        self.currTimes = dict()
        self.startTimes = dict()
        self.circlePositions = [(40, 110), (120, 110), (330, 110), (420, 110),\
        (545, 110), (670, 110), (100, 530), (285, 530)]
        self.images ={"images/juice.png": "juice", "images/coffee.png": "coffee",\
        "images/sushi.png": "sushi", "images/nachos.png": "nachos", \
        "images/steak.png": "steak", "images/cabbage.png": "cabbage", \
        "images/uncookedSteak.png": "uncookedSteak", "images/springRolls.png": "springRolls"}
        self.cookedFood = {"cabbage": "springRolls", "uncookedSteak": "steak"}
        self.time = 0
        self.colorIndex = dict()
        self.justClicked = [False]*8
        self.firstClicks = {'firstClickJ1': False, 'firstClickJ2': False, 'firstClickC1': False,\
            'firstClickC2': False, 'firstClickCook1': False, 'firstClickCook2': False, \
            'firstClickS': False, 'firstClickN': False, 'firstClickUS': False, 'firstClickV': False}
        self.doneWaitings = {'firstClickJ1': False, 'firstClickJ2': False, 'firstClickC1': False,\
            'firstClickC2': False, 'firstClickCook1': False, 'firstClickCook2': False, \
            'firstClickS': False, 'firstClickN': False, 'firstClickUS': False, 'firstClickV': False}
        self.greenToRed = list(Color("green").range_to(Color("red"),12))
        self.redToGreen = list(Color("red").range_to(Color("green"),12))

    def armChecking(self, food, holding):
        if self.character.arm1 == None and self.character.arm2 == None:
            self.drawingChar = self.character.imageOneArm
            self.character.arm1 = food
            self.character.holding.extend([holding])
        elif (self.character.arm2 == None and self.character.arm1 != None \
        and self.drawingChar == self.character.imageOneArm):
            self.drawingChar = self.character.imageTwoArm
            self.character.arm2 = food
            self.character.holding.extend([holding])

    def addToPan(self, imgFile, panNum, handNum, )

    def cookingImages(self):
        if self.character.holding[0] in self.cookedFood and len(self.character.holding) == 1:
            imgFile = "images/" + str(self.cookedFood[self.character.holding[0]]) + ".png"
            if self.pan1 == True and len(self.character.holding) >= 1 and self.beingCooked[0] == None:
                self.beingCooked[0] = [imgFile, self.cookedFood[self.character.holding[0]]]
                self.character.arm1 = None
                self.character.holding.pop(0)
            elif self.pan2 == True and len(self.character.holding) >= 1 and self.beingCooked[1] == None:
                self.beingCooked[1] = [imgFile, self.cookedFood[self.character.holding[0]]]
                self.character.arm1 = None
                self.character.holding.pop(0)
        elif len(self.character.holding) == 2 and self.character.holding[0] in self.cookedFood:
            imgFile = "images/" + str(self.cookedFood[self.character.holding[0]]) + ".png"
            if self.pan1 == True and self.beingCooked[0] == None:
                self.character.arm1 = self.character.arm2
                self.character.arm2 = None
                self.beingCooked[0] = [imgFile, self.cookedFood[self.character.holding[0]]]
                self.character.holding.pop(0)
            elif self.pan1 == True and self.beingCooked[1] == None:
                self.character.arm1 = self.character.arm2
                self.character.arm2 = None
                self.beingCooked[1] = [imgFile, self.cookedFood[self.character.holding[0]]]
                self.character.holding.pop(0)
        elif len(self.character.holding) == 2 and self.character.holding[1] in self.cookedFood:
            imgFile = "images/" + str(self.cookedFood[self.character.holding[1]]) + ".png"
            if self.pan1 == True and self.beingCooked[0] == None:
                self.beingCooked[0] = [imgFile, self.cookedFood[self.character.holding[1]]]
                self.character.arm2 = None
                self.character.holding.pop(1)
            elif self.pan1 == True and self.beingCooked[1] == None:
                self.beingCooked[1] = [imgFile, self.cookedFood[self.character.holding[1]]]
                self.character.arm2 = None
                self.character.holding.pop(1)


    def obtainCookedFood(self):
        if self.character.arm1 == None and self.beingCooked[0] != None:
            self.character.arm1 = self.beingCooked[0][0]
            self.character.holding.extend([self.character.arm1])
            self.beingCooked[0] = None
        elif self.character.arm1 == None and self.beingCooked[1] != None:
            self.character.arm1 = self.beingCooked[1][0]
            self.character.holding.extend([self.character.arm1])
            self.beingCooked[1] = None
        elif self.character.arm2 == None and self.beingCooked[0] != None:
            self.character.arm2 = self.beingCooked[0][0]
            self.character.holding.extend([self.character.arm2])
            self.beingCooked[0] = None
        elif self.character.arm2 == None and self.beingCooked[1] != None:
            self.character.arm2 = self.beingCooked[1][0]
            self.character.holding.extend([self.character.arm2])
            self.beingCooked[1] = None


    def clicking(self, click, image, holding, num):
        self.justClicked[num] = True
        if self.firstClicks[click] == True and self.doneWaitings[click] == True:
            self.armChecking(image, holding)
            self.firstClicks[click] = False
            self.doneWaitings[click] = False
            if self.circlePositions[num] in self.inAction:
                self.inAction.remove(self.circlePositions[num])
        elif self.justClicked[num] == True:
            if num != None:
                self.inAction.extend([self.circlePositions[num]])
                self.startTimes[self.circlePositions[num]] = time.time()
                self.currTimes[click] = time.time()
            self.firstClicks[click] = True
            self.justClicked[num] = False
        if (self.circlePositions[num] in self.colorIndex and \
        self.colorIndex[self.circlePositions[num]] == len(self.redToGreen) - 2):
            self.colorIndex.pop(self.circlePositions[num])

    def trash(self):
        if self.character.arm1 != None:
            self.character.arm1 = None
        if self.character.arm2 != None:
            self.character.arm2 = None
        self.drawingChar = self.character.image
        self.character.holding = []

    def legalClick(self, x, y, x1, x2, y1, y2, click, num):
        return (x1 < x < x2 and y1 < y < y2 and (self.firstClicks[click] == False \
        and self.doneWaitings[click] == False) or (self.circlePositions[num] \
        in self.colorIndex and self.colorIndex[self.circlePositions[num]] \
        == len(self.redToGreen) - 2))

    def cooking(self, pan, click, num):
        if pan == self.pan1:
            self.pan1 = True
        elif pan == self.pan2:
            self.pan2 = True
        self.justClicked[num] = True
        if self.firstClicks[click] == True and self.doneWaitings[click] == True:
            self.obtainCookedFood()
            pan = False
            self.firstClicks[click] = False
            self.doneWaitings[click] = False
            self.inAction.remove(self.circlePositions[num])
            # print(self.character.holding)
        elif self.character.holding != [] and self.justClicked[num] == True:
            self.cookingImages()
            self.inAction.extend([self.circlePositions[num]])
            self.startTimes[self.circlePositions[num]] = time.time()
            self.currTimes[click] = time.time()
            self.firstClicks[click] = True
            self.justClicked[num] = False
        if (self.circlePositions[num] in self.colorIndex and \
        self.colorIndex[self.circlePositions[num]] == len(self.redToGreen) - 2):
            self.colorIndex.pop(self.circlePositions[num])

    def mousePressed(self, x, y):
        #machine 1: juice
        if self.legalClick(x, y, 0, self.width//11, 0, self.height//5, "firstClickJ1", 0):
            self.moveTo(0, 80)
            self.clicking('firstClickJ1',  "images/juice.png", "juice", 0)
        #machine 2: juice
        elif self.legalClick(x, y, self.width//11, 2*self.width//11, 0, \
        self.height//5, "firstClickJ2", 1):
            self.moveTo(80, 80)
            self.clicking('firstClickJ2',  "images/juice.png", "juice", 1)
        #machine 1: coffee
        elif self.legalClick(x, y, 300, 358, 30, 115, "firstClickC1", 2):
            self.moveTo(300, 80)
            self.clicking('firstClickC1',  "images/coffee.png", "coffee", 2)
        #machine 2: coffee
        elif self.legalClick(x, y, 387, 450, 30, 115, "firstClickC2", 3):
            self.moveTo(390, 80)
            self.clicking('firstClickC2',  "images/coffee.png", "coffee", 3)
        #pan 1
        elif self.legalClick(x, y, 522, 572, 75, 102, "firstClickCook1", 4):
            self.moveTo(520, 80)
            self.cooking(self.pan1, "firstClickCook1", 4)
        #pan 2
        elif self.legalClick(x, y, 637, 690, 75, 102, "firstClickCook2", 5):
            self.moveTo(635, 80)
            self.cooking(self.pan2, "firstClickCook2", 5)
        #sushi
        elif self.legalClick(x, y, 20, 158, self.height-150, self.height-100, "firstClickS", 6):
            self.moveTo(50, self.height-150)
            self.clicking('firstClickS',  "images/sushi.png", "sushi", 6)
        #nachos
        elif self.legalClick(x, y, 250, 335, self.height-150, self.height-100, "firstClickN", 7):
            self.moveTo(250, self.height-150)
            self.clicking('firstClickN',  "images/nachos.png", "nachos", 7)
        #meat
        elif 518 < x < 596 and self.height-170 < y < self.height-100:
            self.moveTo(520, self.height-170)
            self.armChecking("images/uncookedSteak.png", "uncookedSteak")
        #veggies
        elif 710 < x < 805 and self.height-150 < y < self.height-100:
            self.moveTo(730, self.height-150)
            self.armChecking("images/cabbage.png", "cabbage")
        elif 780 < x < 880 and 200 < y < 280:
            self.moveTo(780, 240)
            self.trash()
        else:
            self.moveTo(pygame.mouse.get_pos()[0] - \
            self.character.image.get_rect().width//2, \
            pygame.mouse.get_pos()[1] - self.character.image.get_rect().height//2)

    def drawTimerCircles(self, screen):
        currTime = 0
        for circle in self.circlePositions:
            if circle in self.inAction:
                currTime = time.time() - self.startTimes[circle]
                self.colorIndex[circle] = len(self.redToGreen) - 2
                if currTime <= 10:
                    self.colorIndex[circle]= int(currTime//1) + 1
                pygame.draw.circle(screen, (HTMLColorToRGB(str(self.redToGreen\
                [self.colorIndex[circle]]))), circle, 10)

    def redrawAll(self, screen):
        background = pygame.image.load("images/background1.png")
        self.background = pygame.transform.scale(background, (893, 627))
        screen.blit(self.background, (-0, 0))
        screen.blit(self.greenArrow, (810, 300))
        screen.blit(self.trashCan, (780, 200))
        self.drawTimerCircles(screen)




    def moveTo(self, x2,y2):
        self.character.x = x2
        self.character.y = y2

    def timerFired(self, dt):
        print(self.beingCooked)
        print(self.character.holding)
        for click in self.firstClicks:
            if self.firstClicks[click] == True:
                timeNow = time.time() - self.currTimes[click]
                if abs(timeNow - 7) < 0.2:
                    self.doneWaitings[click] = True
                    pass

#citation: http://code.activestate.com/recipes/266466-html-colors-tofrom-rgb-tuples/
def HTMLColorToRGB(colorstring):
#  convert #RRGGBB to an (R, G, B) tuple
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    # if len(colorstring) != 6:
    #     raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)
