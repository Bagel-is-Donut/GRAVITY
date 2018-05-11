# main run file: execute this file to run the game
'''
template credit for pygameGame.py:
created by Lukas Peraza for 15-112 F15 Pygame Optional Lecture, 11/11/15
''' 
from zmenuHelpNotice import *
import pygame

#############################
class PygameGame(object):

    def init(self):
        self.menu = Menu()

    def mousePressed(self, x, y):
        self.menu.mousePressed(x,y)
        
    def mouseReleased(self, x, y):pass
    def mouseMotion(self, x, y):
        self.menu.mouseMotion(x,y)
        
    def mouseDrag(self, x, y):pass
        
    def keyPressed(self, keyCode, modifier):
        self.menu.keyPressed(keyCode)
        
    def keyReleased(self, keyCode, modifier):pass
    def timerFired(self, dt):
        self.menu.timerFired()
        
    def isKeyPressed(self, key):pass
    def redrawAll(self,screen):
        self.menu.redrawAll(screen)

    def __init__(self, width=1100, height=825, fps=50, title="GRAVITY"): 
        self.width = width
        self.height = height
        self.fps = fps      
        #the program will never run at more than fps frames per second
        self.title = title
        self.bgColor = (204, 229, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()
        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

#####################################################
#creating and running the game
game = PygameGame()

def main():
    game.run()

if __name__ == '__main__':
    main()