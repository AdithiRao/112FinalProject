import pygame

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("fullcharacter.png")
