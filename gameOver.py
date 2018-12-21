import pygame
from pygamegame import PygameGame

class gameOver(PygameGame):
    def __init__(self, score):
        self.bgColor = (0,0,0)
        self.font1 = pygame.font.SysFont('Comic Sans MS', 100)
        self.score = score
        pygame.font.init()

    def redrawAll(self, screen):
        screen.fill(self.bgColor)
        textSurface = self.font1.render("Game Over!", False, (255,255, 255))
        screen.blit(textSurface, (250,300))
        textSurface = self.font1.render("Score: " + str(self.score), False, (255,255, 255))
        screen.blit(textSurface, (300,0))
