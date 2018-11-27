import pygame
from pygamegame import PygameGame
from player import Player
import time
import copy
import string
from colour import Color


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
        self.inAction = []
        self.circlePositions = [(40, 110), (120, 110), (330, 110), (420, 110),\
        (545, 110), (670, 110), (100, 530), (285, 530)]
        self.images ={"images/juice.png": "juice", "images/coffee.png": "coffee",\
        "images/sushi.png": "sushi", "images/nachos.png": "nachos", \
        "images/steak.png": "steak", "images/cabbage.png": "cabbage", \
        "images/uncookedSteak.png": "uncookedSteak", "images/springRolls.png": "springRolls"}
        self.cookedFood = {"cabbage": "springRolls", "uncookedSteak": "steak"}
        self.time = 0
        self.firstClicks = {'firstClickJ1': False, 'firstClickJ2': False, 'firstClickC1': False,\
            'firstClickC2': False, 'firstClickCook1': False, 'firstClickCook2': False, \
            'firstClickS': False, 'firstClickN': False, 'firstClickUS': False, 'firstClickV': False}
        self.doneWaitings = {'firstClickJ1': False, 'firstClickJ2': False, 'firstClickC1': False,\
            'firstClickC2': False, 'firstClickCook1': False, 'firstClickCook2': False, \
            'firstClickS': False, 'firstClickN': False, 'firstClickUS': False, 'firstClickV': False}
        self.greenToRed = list(Color("green").range_to(Color("red"),10))
        self.redToGreen = list(Color("red").range_to(Color("green"),10))

    def armChecking(self, food, holding):
        if self.character.arm1 == None and self.character.arm2 == None \
        or ((self.pan1 == True or self.pan2 == True) and \
        len(self.character.holding) == 1):
            if (self.pan1 == True or self.pan2 == True) and len(self.character.holding) == 1:
                self.character.holding.pop()
            self.drawingChar = self.character.imageOneArm
            self.character.arm1 = food
            self.character.holding.extend([holding])
        elif (self.character.arm2 == None and self.character.arm1 != None \
        and self.drawingChar == \
        self.character.imageOneArm) or (self.pan1 == True or self.pan2 == True
        and len(self.character.holding) == 2):
            self.drawingChar = self.character.imageTwoArm
            if len(self.character.holding) == 2 and self.character.holding[0] in self.cookedFood:
                self.character.arm1 = food
                self.character.holding[0] = holding
            elif len(self.character.holding) == 2 and self.character.holding[1] in self.cookedFood:
                self.character.arm2 = food
                self.character.holding[1] = holding
            else:
                self.character.arm2 = food
                self.character.holding.extend([holding])

    def cooking(self):
        if self.character.holding[0] in self.cookedFood:
            imgFile = "images/" + str(self.cookedFood[self.character.holding[0]]) + ".png"
            self.armChecking(imgFile, self.cookedFood[self.character.holding[0]])
        elif len(self.character.holding) == 2 and self.character.holding[1] in self.cookedFood:
            imgFile = "images/" + str(self.cookedFood[self.character.holding[1]]) + ".png"
            self.armChecking(imgFile, self.cookedFood[self.character.holding[1]])

    def clicking(self, click, image, holding, num):
        if self.firstClicks[click] == True and self.doneWaitings[click] == True:
            self.armChecking(image, holding)
            self.firstClicks[click] = False
            self.doneWaitings[click] = False
            self.inAction.remove([self.circlePositions[num]])
        self.firstClicks[click] = True
        if num != None:
            self.inAction.extend([self.circlePositions[num]])

    def trash(self):
        if self.character.arm1 != None:
            self.character.arm1 = None
        if self.character.arm2 != None:
            self.character.arm2 = None
        self.drawingChar = self.character.image
        self.character.holding = []

    def mousePressed(self, x, y):
        #machine 1: juice
        if 0 < x < self.width//11 and 0 < y < self.height//5:
            self.moveTo(0, 80)
            self.clicking('firstClickJ1',  "images/juice.png", "juice", 0)
        #machine 2: juice
        elif self.width//11 < x <2*self.width//11 and 0 < y < self.height//5:
            self.moveTo(80, 80)
            self.clicking('firstClickJ2',  "images/juice.png", "juice", 1)
        #machine 1: coffee
        elif 300 < x < 358 and 30 < y < 115:
            self.moveTo(300, 80)
            self.clicking('firstClickC1',  "images/coffee.png", "coffee", 2)
        #machine 2: coffee
        elif 387 < x < 450 and 30 < y < 115:
            self.moveTo(390, 80)
            self.clicking('firstClickC2',  "images/coffee.png", "coffee", 3)
        #pan 1
        elif 522 < x < 572 and 75 < y < 102:
            self.moveTo(520, 80)
            if self.character.holding != []:
                self.pan1 = True
                if self.firstClicks['firstClickCook1'] == True and self.doneWaitings['firstClickCook1'] == True:
                    self.cooking()
                    self.pan1 = False
                    self.firstClicks['firstClickCook1'] = False
                    self.doneWaitings['firstClickCook1'] = False
                    self.inAction.remove([self.circlePositions[4]])
                self.firstClicks['firstClickCook1'] = True
                self.inAction.extend([self.circlePositions[4]])
        #pan 2
        elif 637 < x < 690 and 75 < y < 102:
            self.moveTo(635, 80)
            if self.character.holding != []:
                self.pan2 = True
                if self.firstClicks['firstClickCook1'] == True and self.doneWaitings['firstClickCook1'] == True:
                    self.cooking()
                    self.pan2 = False
                    self.firstClicks['firstClickCook1'] = False
                    self.doneWaitings['firstClickCook1'] = False
                    self.inAction.remove([self.circlePositions[5]])
                self.firstClicks['firstClickCook1'] = True
                self.inAction.extend([self.circlePositions[5]])
        #sushi
        elif 20 < x < 158 and self.height-150 < y < self.height-100:
            self.moveTo(50, self.height-150)
            self.clicking('firstClickS',  "images/sushi.png", "sushi", 6)
        #nachos
        elif 250 < x < 335 and self.height-150 < y < self.height-100:
            self.moveTo(250, self.height-150)
            self.clicking('firstClickN',  "images/nachos.png", "nachos", 7)
        #meat
        elif 518 < x < 596 and self.height-170 < y < self.height-100:
            self.moveTo(520, self.height-170)
            self.armChecking("images/uncookedSteak.png", "uncookedSteak", None)
        #veggies
        elif 710 < x < 805 and self.height-150 < y < self.height-100:
            self.moveTo(730, self.height-150)
            self.armChecking("images/cabbage.png", "cabbage", None)
        elif 780 < x < 880 and 200 < y < 280:
            self.moveTo(780, 240)
            self.trash()
        else:
            self.moveTo(pygame.mouse.get_pos()[0] - \
            self.character.image.get_rect().width//2, \
            pygame.mouse.get_pos()[1] - self.character.image.get_rect().height//2)



    def redrawAll(self, screen):
        background = pygame.image.load("images/background1.png")
        self.background = pygame.transform.scale(background, (893, 627))
        screen.blit(self.background, (-0, 0))
        screen.blit(self.greenArrow, (810, 300))
        screen.blit(self.trashCan, (780, 200))
        # if self.time == 10:
        #     print(self.redToGreen[0])
        #     print(self.redToGreen[1])
        # if self.time != 10
        for circle in self.circlePositions:
            if circle in self.inAction:
                pygame.circle(screen, (HTMLColorToRGB(str(self.redToGreen[1]))), circle, 10)

    def moveTo(self, x2,y2):
        self.character.x = x2
        self.character.y = y2

    def timerFired(self, dt):
        self.time += 1
        for click in self.firstClicks:
            if self.firstClicks[click] == True:
                start = time.time()
                if self.time % 10 == 0:
                    self.doneWaitings[click] = True
                elif self.doneWaitings[click] == False:
                    pass
                    # print(time.time() - start)

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
