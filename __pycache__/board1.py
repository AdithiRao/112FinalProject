import pygame
from pygamegame import PygameGame
from player import Player


class Board1(PygameGame):
    def __init__(self):
        super().__init__(self)
        background = pygame.image.load("background1.png")
        self.background = pygame.transform.scale(background, (893, 627))
        self.character = Player(-100,-100)
        self.drawingChar = self.character.image
        self.greenArrow = pygame.image.load("greenArrow.png")
        self.greenArrow = pygame.transform.scale(self.greenArrow, (80, 60))

    def mousePressed(self, x, y):
        if 0 < x < 90 and 0 < y < 115:
            self.moveTo(-430, -230)
            print("Making juice from machine 1!")
        elif 84 < x < 152 and 0 < y < 115:
            self.moveTo(-360, -230)
            print("Making juice from machine 2!")
        elif 175 < x < 285 and 0 < y < 115:
            self.moveTo(-270, -230)
            print("Getting a spatula!")
        elif 300 < x < 358 and 30 < y < 115:
            self.moveTo(-140, -230)
            print("Making coffee from machine 1!")
        elif 387 < x < 450 and 30 < y < 115:
            self.moveTo(-70, -230)
            print("Making coffee from machine 2!")
        elif 522 < x < 572 and 75 < y < 102:
            self.moveTo(50, -230)
            print("Cooking from pan 1!")
        elif 637 < x < 690 and 75 < y < 102:
            self.moveTo(150, -230)
            print("Cooking from pan 2!")
        elif 20 < x < 158 and self.height-150 < y < self.height-100:
            self.moveTo(-400, 40)
            print("Making sushi!")
        elif 250 < x < 335 and self.height-150 < y < self.height-100:
            self.moveTo(-175, 60)
            print("Making nachos!")
        elif 518 < x < 596 and self.height-170 < y < self.height-100:
            self.moveTo(50, 20)
            print("Meat shoppp")
        elif 710 < x < 805 and self.height-150 < y < self.height-100:
            self.moveTo(270, 40)
            print("Veggie time")
        elif 800 < x < 880 and 290 < y < 350:
            print("Move to next room")

    def moveTo(self, x2,y2):
        self.character.x = x2
        self.character.y = y2
