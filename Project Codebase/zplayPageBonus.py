# play page for bonus mode game

from zplanet import *
from zstar import *
from zplayer import *
import pygame
import math
import os

# COMBINE "PLAYER, PLANET, STAR"

class PlayModeBonus(object):
    def __init__(self, numDict):
        self.currentMode = "setUp"
        self.BG = pygame.image.load("playModeBG.jpg")
        # some constants
        self.lightOrange = (255,178,102)
        self.numThree = 3           # used in list index
        self.keyCodeEnter = 13
        # numbers of each planets, darkholes, and stars number of \
        #stars(winning goal), are defined by users on CUSTOMIZE PAGE \
        #before game begins, and stored in numDict
        # e.g. numDict = {'S': 1, 'M': 2, 'L': 3, 'D': 4, 'P': 6}
        self.numDict = numDict
        # winning states
        self.score = 0
        self.goal = self.numDict["P"]
        self.win = False
        self.lose = False
        # planet data
        self.planets = Planet(self.numDict)
        # number of stars would alter in the game
        self.stars = Star(self.goal,self.planets.planetDict)
        self.meteors = Meteor()
        self.timerCalls = 0
        # menu bar
        self.leave = False      # go back to menu
        self.pause = False
        self.restart = False
        self.scoreImage = pygame.image.load("score.png")
        self.scoreImageDisplay = (14, 755) # Left top
        self.scoreDisplay = (150, 770)
        fontSize = 20
        self.myfont = pygame.font.SysFont("Comic Sans MS",fontSize)
        self.buttonLeaveImage = pygame.image.load("leave.png")
        self.buttonPauseImage = pygame.image.load("pause.png")
        self.buttonRestartImage = pygame.image.load("restart.png")
        self.buttonLeave = ((1000, 758),(1088, 802))
        self.buttonPause = ((899, 758),(987, 802))
        self.buttonRestart = ((782, 758),(884, 802))
        # win or lose
        self.winPosition = (38,10)
        self.losePosition = (38,10)
        self.winImage = pygame.image.load("win.png")
        self.loseImage = pygame.image.load("lose.png")
        # star and player data
        self.starR = 12
        self.playerR = 10
        self.playerImage =  pygame.image.load("player.png")
        self.playerImage =  pygame.transform.scale(self.playerImage,\
        (self.playerR*2,self.playerR*2))
        self.playerPostion = (50,412)   # left top
        self.selected = None
        self.selectedType = None
        self.clickOnOff = False         # True means on, False means off

    
    def mouseSelectObject(self,x,y):
        if self.currentMode == "setUp":
            # planetDict = {"small": [[(x1,y1),(light1,dark1),False,23]\
            #,[...],...], "medium": [], "large": [], "dark": []}
            for key in self.planets.planetDict:
                for i in range(len(self.planets.planetDict[key])):
                    item = self.planets.planetDict[key][i]
                    radius = item[self.numThree]
                    cx,cy = item[0][0]+radius, item[0][1]+radius
                    distance = math.sqrt((x-cx)**2+(y-cy)**2)
                    if distance <= radius:
                        self.selected = (key,i,radius) # record as tuple
                        self.selectedType = "planet"
            # StarLst = [[x1,y1],[x2,y2],...] Left Top x,y
            for i in range(len(self.stars.starLst)):
                item = self.stars.starLst[i]
                (cx,cy) = (item[0]+self.starR,item[1]+self.starR)
                distance = math.sqrt((x-cx)**2+(y-cy)**2)
                if distance <= self.starR:
                    self.selected = i       # int: index
                    self.selectedType = "star"
            # check if clicked on player
            distance = math.sqrt((x-(self.playerPostion[0]+self.playerR))**2+\
            (y-(self.playerPostion[1]+self.playerR))**2)
            if distance <= self.playerR:
                self.selected = self.playerPostion      # record as tuple
                self.selectedType = "player"


    def mouseMotion(self,x,y):
        if self.currentMode == "setUp":
            if self.selectedType == "planet":
                key = self.selected[0]
                index = self.selected[1]
                radius = self.selected[2]
                self.planets.planetDict[key][index][0] = (x-radius,y-radius)
            elif self.selectedType == "star":
                self.stars.starLst[self.selected] = [x-self.starR,y-self.starR]
            elif self.selectedType == "player":
                self.playerPostion = (x-self.playerR,y-self.playerR)


    def keyPressed(self, keyCode):
        if self.currentMode == "setUp":
            if keyCode == self.keyCodeEnter:
                # type "return/enter" to proceed
                self.currentMode = "play"
                # use the most recent to create instance of player
                self.player = Player(self.planets.planetDict,\
                self.stars.starLst,self.meteors.meteorRainLst,\
                self.goal,self.playerPostion[0],self.playerPostion[1])


    def mousePressed(self,x,y):
        # check if clicked on menu bar first
        if self.buttonLeave[0][0]<x<self.buttonLeave[1][0] and \
        self.buttonLeave[0][1]<y<self.buttonLeave[1][1]:
            self.leave = True
        if self.currentMode == "setUp":
            self.clickOnOff = not self.clickOnOff
            if self.clickOnOff == True:  # made selection, but not yet placed
                self.mouseSelectObject(x,y)
            else:                           # reset to default
                self.selected = None
                self.selectedType = None
        if self.currentMode == "play":
            if self.buttonPause[0][0]<x<self.buttonPause[1][0] and \
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
        if self.restart == True:        # restart starts from the "setUp" page
            self.__init__(self.numDict)     # use original numDict
        if self.currentMode == "play":
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
        if self.currentMode == "play": 
            self.player.redrawAll(screen)
            # display winning or losing
            if self.lose == True:
                screen.blit(self.loseImage,self.losePosition)
            elif self.win == True:
                screen.blit(self.winImage,self.winPosition)
            # place menu bar
            screen.blit(self.scoreImage,self.scoreImageDisplay)
            screen.blit(self.buttonPauseImage,self.buttonPause[0])
            screen.blit(self.buttonRestartImage,self.buttonRestart[0])
            # display score
            text = str(self.score)
            text = text +"   /   "+ str(self.goal)
            textsurface = self.myfont.render(text,True,self.lightOrange)
            screen.blit(textsurface,self.scoreDisplay)
        else:
            screen.blit(self.playerImage,self.playerPostion)
        screen.blit(self.buttonLeaveImage,self.buttonLeave[0])






