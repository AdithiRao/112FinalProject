import pygame
from pygamegame import PygameGame
from board1 import *
from board2 import *

class runGame(PygameGame):
    def __init__(self):
        super().__init__(self)
        self.background1 = True
        self.background2 = False
        self.justStarted = True
        self.startedPlaying = False
        self.kitchen = Board1()
        self.dining = Board2()
        self.customers = []
        self.background = self.kitchen.background
        self.drawingChar = self.kitchen.drawingChar
        self.character = self.kitchen.character
        (self.character.x, self.character.y) = (self.kitchen.character.x, self.kitchen.character.y)
        self.greenArrow = self.kitchen.greenArrow
        self.font = pygame.font.SysFont("Courier New", 24)
        pygame.init()

    def mousePressed(self, x, y):
        if self.background1 == True:
            if 800 < x < 880 and 290 < y < 350: #green Arrow placement
                self.background1 = False
                self.background2 = True
                pygame.mixer.stop()
                self.playMusic()
        elif self.background2 == True:
            if -100 < x < 100 and 290 < y < 350:  #green Arrow placement
                self.background1 = True
                self.background2 = False
                pygame.mixer.stop()
                self.playMusic()

    def timerFired(self, dt):
        if self.background1 == True:
            self.startedPlaying = False
            self.background = self.kitchen.background
            self.drawingChar = self.kitchen.drawingChar
            (self.character.x, self.character.y) = (self.kitchen.character.x, self.kitchen.character.y)
            self.greenArrow = self.kitchen.greenArrow
            self.coords = (810, 300)
        elif self.background2 == True:
            self.startedPlaying = False
            self.background = self.dining.background
            self.drawingChar = self.dining.drawingChar
            (self.character.x, self.character.y) = (self.dining.character.x, self.dining.character.y)
            self.greenArrow = self.dining.greenArrow
            self.coords = (0, 300)
        self.dining.timerFired(dt)
        self.customers = self.dining.customers

    def playMusic(self):
        if self.background1 == True:
            pygame.mixer.init()
            music = pygame.mixer.Sound("music.wav")
            music.play(-1,0)
        else:
            pygame.mixer.init()
            music = pygame.mixer.Sound("music2.wav")
            music.play(-1,0)

    def redrawAll(self, screen):
        for customer in self.customers:
            if self.background2:
                screen.blit(customer.image, (customer.x, customer.y))
        if self.background2:
            for table in self.dining.tables:
                screen.blit(table.image, (table.x, table.y))
            self.dining.redrawAll(screen)
            # screen.blit(self.dining.score, (0,0))
        text = self.font.render("Score: " + str(self.dining.score), True, (255, 0, 0)) #red
        text_rect = text.get_rect()
        text_rect.right = screen.get_rect().right - 10
        text_rect.y = 10
        screen.blit(text, text_rect)
        text2 = self.font.render("Waiting Outside: " + str(self.dining.waitingCustomers), True, (0, 255, 0))
        text2_rect = text.get_rect()
        text2_rect.right = screen.get_rect().right - 300
        text2_rect.y = 10
        screen.blit(text2, text2_rect)


    #Comes from pygamegame.py, provided to us by 112 staff
    def run(self):
        # call game-specific initialization
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption("Diner Dash!")
        self.init()
        self.playMusic()
        self._keys = dict()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.background1 == True:
                        self.kitchen.mousePressed(*(event.pos))
                        self.mousePressed(*(event.pos))
                    else:
                        self.dining.mousePressed(*(event.pos))
                        self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.background1 == True:
                        self.kitchen.mouseReleased(*(event.pos))
                    else:
                        self.dining.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    if self.background1 == True:
                        self.kitchen.mouseMotion(*(event.pos))
                    else:
                        self.dining.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    if self.background1 == True:
                        self.kitchen.mouseDrag(*(event.pos))
                    else:
                        self.dining.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    if self.background1 == True:
                        self.kitchen._keys[event.key] = True
                        self.kitchen.keyPressed(event.key, event.mod)
                    else:
                        self.dining._keys[event.key] = True
                        self.dining.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    if self.background1 == True:
                        self.kitchen._keys[event.key] = False
                        self.kitchen.keyReleased(event.key, event.mod)
                    else:
                        self.dining._keys[event.key] = False
                        self.dining.keyReleased(event.key, event.mod)
            screen.fill(self.bgColor)
            screen.blit(self.background, (-0, 0))
            self.redrawAll(screen)
            screen.blit(self.drawingChar, (self.character.x, self.character.y))
            screen.blit(self.greenArrow, self.coords)
            pygame.display.flip()


        pygame.quit()

def main():
    game = runGame()
    game.run()

if __name__ == "__main__":
    main()
