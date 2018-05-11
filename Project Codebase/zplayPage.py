# play page for classic mode game

from zplanet import *
from zstar import *
from zplayer import *
import pygame
import math
import os


# COMBINE "PLAYER, PLANET, STAR"

class PlayMode(object):
    def __init__(self, numDict):
        self.BG = pygame.image.load("playModeBG.jpg")
        # numbers of each planets, darkholes, and stars number of \
        #stars(winning goal), are defined by users on CUSTOMIZE PAGE \
        #before game begins, and stored in numDict
        # e.g. numDict = {'S': 1, 'M': 2, 'L': 3, 'D': 4, 'P': 6}
        self.numDict = numDict
        self.lightOrange = (255,178,102)
        # winning states
        self.score = 0
        self.goal = self.numDict["P"]
        self.win = False
        self.lose = False
        # planet data
        self.planets = Planet(self.numDict)
        self.planetDict = self.planets.planetDict
        # number of stars would alter in the game
        self.stars = Star(self.goal,self.planetDict)
        self.meteors = Meteor()
        self.player = Player(self.planetDict,\
        self.stars.starLst,self.meteors.meteorRainLst,self.goal)        
        self.timerCalls = 0
        # menu bar
        self.leave = False      # go back to menu
        self.pause = False
        self.restart = False
        self.scoreImage = pygame.image.load("score.png")
        self.scoreImageDisplay = (14, 755) # Left top
        self.scoreDisplay = (150, 770)
        fontSize = 20
        self.font = pygame.font.SysFont("comicsansms", fontSize)        
        self.buttonLeaveImage = pygame.image.load("leave.png")
        self.buttonPauseImage = pygame.image.load("pause.png")
        self.buttonRestartImage = pygame.image.load("restart.png")
        self.buttonLeave = ((1000, 758),(1088, 802))
        self.buttonPause = ((899, 758),(987, 802))
        self.buttonRestart = ((782, 758),(884, 802))
        self.winPosition = (38,10)
        self.losePosition = (38,10)
        self.winImage = pygame.image.load("win.png")
        self.loseImage = pygame.image.load("lose.png")
    


    def mousePressed(self,x,y):
        # check if clicked on menu bar first
        if self.buttonLeave[0][0]<x<self.buttonLeave[1][0] and \
        self.buttonLeave[0][1]<y<self.buttonLeave[1][1]:
            self.leave = True
        elif self.buttonPause[0][0]<x<self.buttonPause[1][0] and \
            self.buttonPause[0][1]<y<self.buttonPause[1][1]:
            self.pause = not self.pause
        elif self.buttonRestart[0][0]<x<self.buttonRestart[1][0] and \
            self.buttonRestart[0][1]<y<self.buttonRestart[1][1]:
            self.restart = True
        # check if clicked in planets
        if self.win == False and self.lose == False and self.pause == False:
            self.planets.mousePressed(x,y)
            self.player.mousePressed(x,y)


    def timerFired(self):
        if self.restart == True:
            self.__init__(self.numDict)     # use original numDict
        if self.win == False and self.lose == False:
            self.timerCalls += 1
            if self.score >= self.goal:
                self.player.win = True
            if self.pause == False:
                self.planets.timerFired()
                self.player.planetDict = self.planets.planetDict
                self.meteors.timerFired()
                # update meteorLst inside player
                self.player.meteorLst = self.meteors.meteorRainLst
                self.player.timerFired()
                self.stars.starLst = self.player.starLst
                self.meteors.meteorRainLst = self.player.meteorLst
                self.score = self.player.score
            self.win = self.player.win
            self.lose = self.player.lose


    def redrawAll(self,screen):
        screen.blit(self.BG,(0,0))
        # place player and planets
        self.planets.redrawAll(screen)
        self.stars.redrawAll(screen)
        self.meteors.redrawAll(screen)
        self.player.redrawAll(screen)
        # place menu bar
        screen.blit(self.scoreImage,self.scoreImageDisplay)
        screen.blit(self.buttonLeaveImage,self.buttonLeave[0])
        screen.blit(self.buttonPauseImage,self.buttonPause[0])
        screen.blit(self.buttonRestartImage,self.buttonRestart[0])
        # display score
        text = str(self.score)
        text = text +"   /   "+ str(self.goal)
        textsurface = self.font.render(text,True,self.lightOrange)
        screen.blit(textsurface,self.scoreDisplay)
        # display winning or losing
        if self.lose == True:
            screen.blit(self.loseImage,self.losePosition)
        elif self.win == True:
            screen.blit(self.winImage,self.winPosition)






