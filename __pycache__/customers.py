import pygame

class Customer(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        image = pygame.image.load("customers.png")
        self.image = pygame.transform.scale(image, (120, 100))

class Table(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        image = pygame.image.load("table.png")
        self.image = pygame.transform.scale(image, (200, 150))


class SeatedTable(Table):
    def __init__(self, x, y):
        super().__init__(x,y)
        image = pygame.image.load("seated.png")
        self.image = pygame.transform.scale(image, (200, 150))
