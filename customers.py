import pygame

class Customer(object):
    def __init__(self, x, y, start):
        self.x = x
        self.y = y
        self.time = 0
        image = pygame.image.load("images/customers.png")
        self.image = pygame.transform.scale(image, (120, 100))
        self.startTime = start
        self.endTime = None


class Table(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        image = pygame.image.load("images/table.png")
        self.image = pygame.transform.scale(image, (200, 150))
        self.carrying = []
        self.eating = False
        self.startTime = None
        self.endTime = None


class SeatedTable(Table):
    def __init__(self, x, y):
        super().__init__(x,y)
        image = pygame.image.load("images/seated.png")
        self.image = pygame.transform.scale(image, (200, 150))
