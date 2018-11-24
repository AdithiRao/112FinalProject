import pygame
from pygamegame import PygameGame
from board1 import *
from board2 import *
from player import *

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

    def canBePlaced(self, table):
        if table.x <= pygame.mouse.get_pos()[0] <= table.x + table.image.get_size()[0] \
        and table.y <= pygame.mouse.get_pos()[1] <= table.y + table.image.get_size()[1] \
        and self.dining.movingCustomer == None and self.character.holding != [] and \
        self.kitchen.images[self.character.arm1] in self.character.holding and \
        0 <= len(table.carrying) <= 4:
            return True
        return False

    def place(self):
        if pygame.mouse.get_pressed()[0]:
            for table in self.dining.takenTables:
                if self.canBePlaced(table):
                    table.carrying.extend([self.character.arm1])
                    if len(self.character.holding) == 2:
                        food2 = pygame.image.load(self.character.arm2)
                        food2 = pygame.transform.scale(food2, (20, 20))
                        table.image.blit(food2, ((table.image.get_size()[0])//2 -20, (table.image.get_size()[1])//2 - 20))
                        table.carrying.extend([self.character.arm2])
                        self.character.holding.remove(self.kitchen.images[self.character.arm2])
                        self.character.arm2 = None
                    self.character.holding.remove(self.kitchen.images[self.character.arm1])
                    self.character.arm1 = None
                    self.kitchen.drawingChar = self.kitchen.character.image

    def timerFired(self, dt):
        self.kitchen.timerFired(dt)
        self.drawingChar = self.kitchen.drawingChar
        if self.background1 == True:
            (self.character.x, self.character.y) = (self.kitchen.character.x, self.kitchen.character.y)
        elif self.background2 == True:
            self.dining.timerFired(dt)
            (self.character.x, self.character.y) = (self.dining.character.x, self.dining.character.y)
            if self.character.holding != None:
                self.place()
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
        screen.fill(self.bgColor)
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
        if self.background2:
            self.dining.redrawAll(screen)
            for customer in self.customers:
                screen.blit(customer.image, (customer.x, customer.y))
            for table in self.dining.takenTables:
                if table.carrying != []:
                    if len(table.carrying) <= 2:
                        x = -20
                        for item in table.carrying:
                            item = pygame.image.load(item)
                            item = pygame.transform.scale(item, (20, 20))
                            table.image.blit(item, ((table.image.get_size()[0])//2\
                            + x, (table.image.get_size()[1])//2 - 20))
                            x += 40
                    else:
                        x = -40
                        for item in table.carrying[2:]:
                            item = pygame.image.load(item)
                            item = pygame.transform.scale(item, (20, 20))
                            table.image.blit(item, ((table.image.get_size()[0])//2\
                            + x, (table.image.get_size()[1])//2 - 20))
                            x += 80
                    print(table.carrying)
            screen.blit(self.drawingChar, (self.character.x, self.character.y))
        elif self.background1:
            self.kitchen.redrawAll(screen)

    #from 112 notes
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
            self.redrawAll(screen)
            pygame.display.flip()


        pygame.quit()

def main():
    game = runGame()
    game.run()

if __name__ == "__main__":
    main()
