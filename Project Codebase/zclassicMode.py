# combine two submodes: "customize" and "play"
# MODE DISPATCHER

from zcustomizePage import *
from zplayPage import *
import pygame
import math
import os


class ClassicMode(pygame.sprite.Sprite):
    def __init__(self):
        self.customize = Customize()
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
                    self.play = PlayMode(self.customize.numDict)
                    self.currentSubMode = "play"
            elif self.currentSubMode == "play":
                self.play.mousePressed(x,y)
                self.leave = self.play.leave
                if self.restartPlay == True:
                    self.totalScoreInARound += self.score
                if self.play.win == True or self.play.lose == True:
                    self.totalScoreInARound += self.score


    def keyPressed(self, keyCode):
        if self.leave == False:
            if self.currentSubMode == "customize":
                self.customize.keyPressed(keyCode)


    def timerFired(self):
        if self.leave == False:
            if self.customize.allSet == False:      
            # not all set, still in customize mode
                self.currentSubMode = "customize"
            else:
                self.currentSubMode = "play"
                self.play.timerFired()
                self.restartPlay = self.play.restart
                if self.play.win == True or self.play.lose == True:
                    self.score = self.play.score

    def redrawAll(self,screen):
        if self.currentSubMode == "customize":
            self.customize.redrawAll(screen)
        elif self.currentSubMode == "play":
            self.play.redrawAll(screen)
            




