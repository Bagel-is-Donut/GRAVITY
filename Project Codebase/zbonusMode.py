# combine three submodes: "customize", "help", and "play"
# MODE DISPATCHER

from zcustomizePageBonus import *
from zplayPageBonus import *
import pygame
import math
import os


class BonusMode(pygame.sprite.Sprite):
    def __init__(self):
        self.keyCodeEnter = 13
        self.help = pygame.image.load("bonusHelp.png")
        self.customize = CustomizeBonus()
        self.leave = False              # back to menu option
        self.currentSubMode = "customize"   # by default
        self.score = 0
        self.restartPlay = False
        self.totalScoreInARound = 0

        
    def mousePressed(self,x,y):
        if self.leave == False:
            if self.currentSubMode == "customize":
                self.customize.mousePressed(x,y)
                self.leave = self.customize.leave
                if self.customize.allSet == True:
                    self.customize.getAllNum()
                    # pass on data to play mode
                    self.play = PlayModeBonus(self.customize.numDict)
                    self.currentSubMode = "help"
            elif self.currentSubMode == "play":
                self.play.mousePressed(x,y)
                self.leave = self.play.leave
                if self.restartPlay == True:
                    self.totalScoreInARound += self.score
                if self.play.win == True or self.play.lose == True:
                    self.totalScoreInARound += self.score

    def mouseMotion(self,x,y):
        if self.currentSubMode == "play":
            self.play.mouseMotion(x,y)

    def keyPressed(self, keyCode):
        if self.leave == False:
            if self.currentSubMode == "customize":
                self.customize.keyPressed(keyCode)
            elif self.currentSubMode == "help":
                if keyCode == self.keyCodeEnter:
                    # type "return/enter" to proceed
                    self.currentSubMode = "play"
            elif self.currentSubMode == "play":
                self.play.keyPressed(keyCode)
                

    def timerFired(self):
        if self.leave == False:
            if self.customize.allSet == False:      
            # not all set, still in customize mode
                self.currentSubMode = "customize"
            elif self.currentSubMode == "play":
                self.play.timerFired()
                self.restartPlay = self.play.restart
                if self.play.win == True or self.play.lose == True:
                    self.score = self.play.score

    def redrawAll(self,screen):
        if self.currentSubMode == "customize":
            self.customize.redrawAll(screen)
        elif self.currentSubMode == "help":
            screen.blit(self.help,(0,0))
        elif self.currentSubMode == "play":
            self.play.redrawAll(screen)
            




