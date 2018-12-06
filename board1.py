import pygame
from pygamegame import PygameGame
from player import Player
import time
import copy
import string
from colour import Color
import math
from astar import createPath


class Board1(PygameGame):
    def __init__(self):
        super().__init__(self)
        background = pygame.image.load("images/background1.png")
        self.background = pygame.transform.scale(background, (893, 627))
        self.character = Player(100,100)
        self.drawingChar = pygame.image.load("images/fullcharacter.png")
        self.greenArrow = pygame.image.load("images/greenArrow.png")
        self.greenArrow = pygame.transform.scale(self.greenArrow, (80, 60))
        self.trashCan = pygame.image.load("images/trashCan.png")
        self.trashCan = pygame.transform.scale(self.trashCan, (100, 80))
        self.centerTable = pygame.image.load("images/centerTable.png")
        self.centerTable = pygame.transform.scale(self.centerTable, (400-305, 80))
        self.pan1 = False
        self.pan2 = False
        self.beingCooked = [None, None]
        self.inAction = []
        self.path = []
        self.currTimes = dict()
        self.startTimes = dict()
        self.ready = dict()
        self.reached = dict()
        self.reachedKey = None
        self.circlePositions = [(40, 110), (120, 110), (330, 110), (420, 110),\
        (545, 110), (670, 110), (100, 530), (285, 530)]
        self.images ={"images/juice.png": "juice", "images/coffee.png": "coffee",\
        "images/sushi.png": "sushi", "images/nachos.png": "nachos", \
        "images/steak.png": "steak", "images/cabbage.png": "cabbage", \
        "images/uncookedSteak.png": "uncookedSteak", "images/springRolls.png": "springRolls"}
        self.cookedFood = {"cabbage": "springRolls", "uncookedSteak": "steak"}
        self.time = 0
        self.currClick = None
        self.colorIndex = dict()
        self.justClicked = [True]*8
        self.firstClicks = {'firstClickJ1': False, 'firstClickJ2': False, 'firstClickC1': False,\
            'firstClickC2': False, 'firstClickCook1': False, 'firstClickCook2': False, \
            'firstClickS': False, 'firstClickN': False, 'firstClickUS': False, 'firstClickV': False}
        self.doneWaitings = {'firstClickJ1': False, 'firstClickJ2': False, 'firstClickC1': False,\
            'firstClickC2': False, 'firstClickCook1': False, 'firstClickCook2': False, \
            'firstClickS': False, 'firstClickN': False, 'firstClickUS': False, 'firstClickV': False}
        self.greenToRed = list(Color("green").range_to(Color("red"),12))
        self.redToGreen = list(Color("red").range_to(Color("green"),12))

    def trash(self):
        if self.character.arm1 != None:
            self.character.arm1 = None
        if self.character.arm2 != None:
            self.character.arm2 = None
        self.drawingChar = self.character.image
        self.character.holding = []
        if len(self.reached) != 0:
            self.reached.pop("trash")

    def legalClick(self, x, y, x1, x2, y1, y2):
        return (x1 < x < x2 and y1 < y < y2)

    def case1(self):
        imgFile = "images/" + str(self.cookedFood[self.character.holding[0]]) + ".png"
        if self.pan1 == True and len(self.character.holding) >= 1 and self.beingCooked[0] == None:
            self.beingCooked[0] = [imgFile, self.cookedFood[self.character.holding[0]]]
            self.character.arm1 = None
            self.character.holding.pop(0)
        elif self.pan2 == True and len(self.character.holding) >= 1 and self.beingCooked[1] == None:
            self.beingCooked[1] = [imgFile, self.cookedFood[self.character.holding[0]]]
            self.character.arm1 = None
            self.character.holding.pop(0)

    def case2(self):
        imgFile = "images/" + str(self.cookedFood[self.character.holding[0]]) + ".png"
        if self.pan1 == True and self.beingCooked[0] == None:
            self.character.arm1 = self.character.arm2
            self.character.arm2 = None
            self.beingCooked[0] = [imgFile, self.cookedFood[self.character.holding[0]]]
            self.character.holding.pop(0)
        elif self.pan2 == True and self.beingCooked[1] == None:
            self.character.arm1 = self.character.arm2
            self.character.arm2 = None
            self.beingCooked[1] = [imgFile, self.cookedFood[self.character.holding[0]]]
            self.character.holding.pop(0)

    def case3(self):
        imgFile = "images/" + str(self.cookedFood[self.character.holding[1]]) + ".png"
        if self.pan1 == True and self.beingCooked[0] == None:
            self.beingCooked[0] = [imgFile, self.cookedFood[self.character.holding[1]]]
            self.character.arm2 = None
            self.character.holding.pop(1)
        elif self.pan2 == True and self.beingCooked[1] == None:
            self.beingCooked[1] = [imgFile, self.cookedFood[self.character.holding[1]]]
            self.character.arm2 = None
            self.character.holding.pop(1)

    def cookingImages(self):
        if self.character.holding[0] in self.cookedFood and len(self.character.holding) == 1:
            self.case1()
        elif len(self.character.holding) == 2 and self.character.holding[0] in self.cookedFood:
            self.case2()
        elif len(self.character.holding) == 2 and self.character.holding[1] in self.cookedFood:
            self.case3()

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
        if holding in self.reached:
            self.reached.pop(holding)

    def obtainCookedFood(self, click):
        cx = self.character.x + self.character.image.get_size()[0]//2
        cy = self.character.y + self.character.image.get_size()[1]//2
        if (click  == "firstClickCook1" and cx == 540 and cy == 180) or (click \
        == "firstClickCook2" and cx == 659 and cy == 180):
            if self.character.arm1 == None and self.ready[click] != None \
            and self.character.arm2 == None:
                self.character.arm1 = self.ready[click][0]
                self.character.holding.extend([self.images[self.character.arm1]])
                self.drawingChar = self.character.imageOneArm
                return True
            elif self.character.arm2 == None and self.character.arm1 != None and \
            self.ready[click] != None:
                self.drawingChar = self.character.imageTwoArm
                self.character.arm2 = self.ready[click][0]
                self.character.holding.extend([self.images[self.character.arm2]])
                return True
        elif click == "firstClickCook1":
            self.path = createPath(cx,cy,540,180)
            return False
        elif click == "firstClickCook2":
            self.path = createPath(cx, cy, 660, 180)
            return False

    def cooking(self, panNum, click, num):
        if panNum == 0: self.pan1 = True
        elif panNum == 1: self.pan2 = True
        if self.firstClicks[click] == True and self.doneWaitings[click] == True:
            self.ready[click] = self.beingCooked[panNum]
            if len(self.character.holding) <= 1 and self.currClick == click:
                if self.obtainCookedFood(click):
                    self.beingCooked[panNum] = None
                    if panNum == 0: self.pan1 = False
                    elif panNum == 1: self.pan2 = False
                    self.ready.pop(click)
                    self.startTimes.pop(self.circlePositions[num])
                    self.firstClicks.pop(click)
                    self.currTimes.pop(click)
                    self.firstClicks[click] = False
                    self.doneWaitings[click] = False
                    self.justClicked[num] = True
                    self.inAction.remove(self.circlePositions[num])
        elif self.character.holding != [] and self.justClicked[num] == True \
        and self.doneWaitings[click] == False:
            self.cookingImages()
            self.inAction.extend([self.circlePositions[num]])
            self.startTimes[self.circlePositions[num]] = time.time()
            self.currTimes[click] = time.time()
            self.firstClicks[click] = True
            self.justClicked[num] = False
        if (self.circlePositions[num] in self.colorIndex and \
        self.colorIndex[self.circlePositions[num]] == len(self.redToGreen) - 2):
            self.colorIndex.pop(self.circlePositions[num])
        self.reached.pop(click)

    def clicking(self, click, image, holding, num):
        if self.firstClicks[click] == True and self.doneWaitings[click] == True:
            self.ready[click] = image
            if len(self.character.holding) <= 1 and self.currClick == click:
                self.armChecking(image, holding)
                self.ready.pop(click)
                self.startTimes.pop(self.circlePositions[num])
                self.firstClicks.pop(click)
                self.currTimes.pop(click)
                self.firstClicks[click] = False
                self.doneWaitings[click] = False
                self.justClicked[num] = True
                if self.circlePositions[num] in self.inAction:
                    self.inAction.remove(self.circlePositions[num])
        elif self.justClicked[num] == True and self.doneWaitings[click] == False:
            self.inAction.extend([self.circlePositions[num]])
            self.startTimes[self.circlePositions[num]] = time.time()
            self.currTimes[click] = time.time()
            self.firstClicks[click] = True
            self.justClicked[num] = False
        if (self.circlePositions[num] in self.colorIndex and \
        self.colorIndex[self.circlePositions[num]] == len(self.redToGreen) - 2):
            self.colorIndex.pop(self.circlePositions[num])
        self.reached.pop(click)

    def mousePressed(self, x, y):
        cx = self.character.x + self.character.image.get_size()[0]//2
        cy = self.character.y + self.character.image.get_size()[1]//2
        #machine 1: juice
        if self.legalClick(x, y, 0, self.width//11, 0, self.height//5):
            if "firstClickJ1" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickJ1"
                self.path = createPath(cx,cy,30,180)
            else:
                self.reached["firstClickJ1"] = True
                self.currClick = "firstClickJ1"
                self.clicking('firstClickJ1',  "images/juice.png", "juice", 0)
        #machine 2: juice
        elif self.legalClick(x, y, self.width//11, 2*self.width//11, 0, \
        self.height//5):
            if "firstClickJ2" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickJ2"
                self.path = createPath(cx, cy,140,180)
            else:
                self.reached["firstClickJ2"] = True
                self.currClick = "firstClickJ2"
                self.clicking('firstClickJ2',  "images/juice.png", "juice", 1)
        #machine 1: coffee
        elif self.legalClick(x, y, 300, 358, 30, 115):
            if "firstClickC1" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickC1"
                self.path = createPath(cx,cy,330,150)
            else:
                self.reached["firstClickC1"] = True
                self.currClick = "firstClickC1"
                self.clicking('firstClickC1',  "images/coffee.png", "coffee", 2)
        #machine 2: coffee
        elif self.legalClick(x, y, 387, 450, 30, 115):
            if "firstClickC2" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickC2"
                self.path = createPath(cx,cy,415,150)
            else:
                self.reached["firstClick2"] = True
                self.currClick = "firstClickC2"
                self.clicking('firstClickC2',  "images/coffee.png", "coffee", 3)
        #pan 1
        elif self.legalClick(x, y, 522, 572, 75, 102):
            if "firstClickCook1" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickCook1"
                self.path = createPath(cx,cy,540,180)
            else:
                self.reached["firstClickCook1"] = True
                self.currClick = "firstClickCook1"
                self.cooking(0, "firstClickCook1", 4)
        #pan 2
        elif self.legalClick(x, y, 637, 690, 75, 102):
            if "firstClickCook2" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickCook2"
                self.path = createPath(cx, cy,660,180)
            else:
                self.reached["firstClickCook1"] = True
                self.currClick = "firstClickCook2"
                self.cooking(1, "firstClickCook2", 5)
        #sushi
        elif self.legalClick(x, y, 20, 158, self.height-150, self.height-100):
            if "firstClickS" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickS"
                self.path = createPath(cx,cy,95, 400)
            else:
                self.reached["firstClickS"] = True
                self.currClick = "firstClickS"
                self.clicking('firstClickS',  "images/sushi.png", "sushi", 6)
        #nachos
        elif self.legalClick(x, y, 250, 335, self.height-150, self.height-100):
            if "firstClickN" not in self.reached:
                self.reached = dict()
                self.reachedKey = "firstClickN"
                self.path = createPath(cx,cy,280,390)
            else:
                self.reached["firstClickN"] = True
                self.currClick = "firstClickN"
                self.clicking('firstClickN',  "images/nachos.png", "nachos", 7)
        #meat
        elif 518 < x < 596 and self.height-170 < y < self.height-100:
            if "uncookedSteak" not in self.reached:
                self.reached = dict()
                self.reachedKey = "uncookedSteak"
                self.path = createPath(cx,cy,475,450)
            else:
                self.reached["uncookedSteak"] = True
                self.currClick = "uncookedSteak"
                self.armChecking("images/uncookedSteak.png", "uncookedSteak")
        #veggies
        elif 710 < x < 805 and self.height-150 < y < self.height-100:
            if "cabbage" not in self.reached:
                self.reached = dict()
                self.reachedKey = "cabbage"
                self.path = createPath(cx,cy,680,450)
            else:
                self.reached["cabbage"] = True
                self.currClick = "cabbage"
                self.armChecking("images/cabbage.png", "cabbage")
        #trash
        elif 780 < x < 880 and 200 < y < 280:
            if "trash" not in self.reached:
                self.reached = dict()
                self.reachedKey = "trash"
                self.path = createPath(self.character.x,self.character.y,780,240)
            else:
                self.reached["trash"] = True
                self.trash()


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
        screen.blit(self.centerTable, (305, 315))
        # for pos in self.path:
        #     pygame.draw.circle(screen, (0,0,0), (pos[0], pos[1]), 3)
        self.drawTimerCircles(screen)


    def timerFired(self, dt):
        if len(self.path) >= 5:
            self.path.pop(0)
            self.path.pop(0)
            self.path.pop(0)
            self.path.pop(0)
            currPos = self.path.pop(0)
            self.character.x = currPos[0] - self.character.image.get_size()[0]//2
            self.character.y = currPos[1] - self.character.image.get_size()[1]//2
        if len(self.path) < 5 and len(self.path) != 0:
            if self.reachedKey != None:
                self.reached[self.reachedKey] = True
                self.path = []
                self.reachedKey = None
        for click in self.firstClicks:
            if self.firstClicks[click] == True:
                timeNow = time.time() - self.currTimes[click]
                if abs(timeNow - 2) < 7:
                    self.doneWaitings[click] = True
                    pass

#citation: http://code.activestate.com/recipes/266466-html-colors-tofrom-rgb-tuples/
def HTMLColorToRGB(colorstring):
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)
