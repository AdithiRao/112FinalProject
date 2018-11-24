import pygame

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/fullcharacter.png")
        imageOneArm = pygame.image.load("images/character1ArmUp.png")
        self.imageOneArm = pygame.transform.scale(imageOneArm, (125, 150))
        imageTwoArm = pygame.image.load("images/Character2ArmsUp.png")
        self.imageTwoArm = pygame.transform.scale(imageTwoArm, (150, 150))
        self.arm1 = None
        self.arm2 = None
        self.holding = []
