import pygame
from pygamegame import PygameGame


class startScreen(PygameGame):
    def __init__(self):
        super().__init__(self)
        self.highScore = self.getHighScore("scores.txt")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 100)
        background = pygame.image.load("images/diner.png")
        self.dinerImage = pygame.transform.scale(background, (400, 200))
        self.bgColor = (0,0,0)

    def getHighScore(self, filename):
        with open(filename, "rt") as f:
            return f.read()

    def redrawAll(self, screen):
        screen.fill(self.bgColor)
        textSurface = self.font.render("High Score: " + str(self.highScore),
        False, (255,255, 255))
        screen.blit(textSurface, (0,0))
        screen.blit(self.dinerImage, (50, 50))
