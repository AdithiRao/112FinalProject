import pygame
from pygamegame import PygameGame

class startScreen(PygameGame):
    def __init__(self):
        super().__init__(self)
        self.highScore = self.getHighScore("scores.txt")
        pygame.font.init()
        self.font1 = pygame.font.SysFont('Comic Sans MS', 100)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 50)
        background = pygame.image.load("images/diner.png")
        self.dinerImage = pygame.transform.scale(background, (400, 200))
        self.bgColor = (0,0,0)

    def getHighScore(self, filename):
        with open(filename, "rt") as f:
            return f.read()

    def drawButton(self, screen):
        text = "Play Game!"
        text_rect = pygame.Rect((275,550), (350, 600))
        pygame.draw.rect(screen, (255,255,255), text_rect)
        image = self.font2.render(text, False, (0,0,0))
        imageLeft = image.get_size()[0] - image.get_size()[0]//2
        screen.blit(image, (text_rect.left+imageLeft, text_rect.top))

    def mousePressed(self, x, y):
        if 275 < x < 550 and 350 < y < 600:
            return True
        else:
            return False

    def redrawAll(self, screen):
        screen.fill(self.bgColor)
        textSurface = self.font2.render("High Score: " + str(self.highScore),
        False, (255,255, 255))
        screen.blit(textSurface, (325,0))
        textSurface2 = self.font1.render("Diner Dash!", False, (255, 0, 0))
        screen.blit(textSurface2, (250, 225))
        screen.blit(self.dinerImage, (250, 300))
        self.drawButton(screen)
