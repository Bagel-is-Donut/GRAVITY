# customize page for classic mode game

import pygame
import os

class Customize(pygame.sprite.Sprite):
    def __init__(self):
        self.customize = pygame.image.load("customize.png")
        # bubble location ranges [(LTx,LTy),(RBx,RBy)]
        self.bubbleS = ((300,206),(610,258))
        self.bubbleM = ((300,343),(610,394))
        self.bubbleL = ((300,494),(610,544))
        self.bubbleD = ((300,637),(610,686))
        self.bubbleP = ((704,483),(1051,525))       # play's goal, num of star
        self.bubbleDict = {self.bubbleS:"   Click to Enter a Number: 1-5", \
        self.bubbleM:"   Click to Enter a Number: 1-5", \
        self.bubbleL:"   Click to Enter a Number: 1-5", \
        self.bubbleD:"   Click to Enter a Number: 1-5", \
        self.bubbleP:"  Click to Enter a Number: 1-9"}
        self.currentBubble = self.bubbleS       # a bubble 2D lst
        self.myfont = pygame.font.SysFont("Comic Sans MS",20)
        self.keyCode = {1:49, 2:50, 3:51, 4:52, 5:53, 6:54, 7:55, 8:56, 9:57}
        self.allSetPosition = ((719, 190), (973, 333))
        self.allSet = False
        self.bubbleLeave = ((940,726),(1083,787))
        self.leave = False     # go back to menu page
        self.orangeColor = (255,153,51)

    def mousePressed(self, x, y):
        if self.allSet == False and self.leave == False:
            if self.bubbleLeave[0][0]<x<self.bubbleLeave[1][0] and \
            self.bubbleLeave[0][1]<y<self.bubbleLeave[1][1]:
                self.leave = True
            # check click in bubbles
            allBubbles = [self.bubbleS,self.bubbleM,self.bubbleL,\
            self.bubbleD,self.bubbleP]
            for bubble in allBubbles:
                if self.inBubble(x,y,bubble):
                    self.currentBubble = bubble
                    self.bubbleDict[self.currentBubble] = \
                    "   What's your lucky number?"
            if self.allSetPosition[0][0]<x<self.allSetPosition[1][0] and \
            self.allSetPosition[0][1]<y<self.allSetPosition[1][1]:
                self.allSet = True
                for bubble in self.bubbleDict:
                    text = self.bubbleDict[bubble]
                    if len(text) != 1:
                        self.allSet = False    # must all set valid numbers

    def getNumSMLDP(self):
        if self.allSet == True:
        # size of planets and their number, P means player's goal of stars
            newDict = {}
            # values are already numbers
            newDict["S"]=int(self.bubbleDict[self.bubbleS])
            newDict["M"]=int(self.bubbleDict[self.bubbleM])
            newDict["L"]=int(self.bubbleDict[self.bubbleL])
            newDict["D"]=int(self.bubbleDict[self.bubbleD])
            newDict["P"]=int(self.bubbleDict[self.bubbleP])
            return newDict

    def getAllNum(self):
        if self.allSet==True:
            self.numDict = self.getNumSMLDP()
            self.numSmall = self.numDict["S"]
            self.numMedium = self.numDict["M"]
            self.numLarge = self.numDict["L"]
            self.numDarkhole = self.numDict["D"]
            self.numStar = self.numDict["P"]

    def inBubble(self,x,y,bubbleLst):
        if bubbleLst[0][0]<x<bubbleLst[1][0] and\
         bubbleLst[0][1]<y<bubbleLst[1][1]:
            return True
        return False

    def keyPressed(self,keyCode):
        # only keys in keyCode will be valid
        if self.allSet == False and self.leave ==False:
            maxPlanets = 5
            for key in self.keyCode:
                if keyCode == self.keyCode[key]:
                    if self.currentBubble != self.bubbleP and key > maxPlanets:
                        self.bubbleDict[self.currentBubble] =\
                         "     invalid input"
                        break
                    self.bubbleDict[self.currentBubble] = str(key)

    def redrawAll(self, screen):
        # display the customize page
        screen.blit(self.customize,(0,0))
        for bubble in self.bubbleDict:
            text = self.bubbleDict[bubble]
            if len(text) == 1:
                text = "   number:"+"             " + text
            textsurface = self.myfont.render(text,True,self.orangeColor)
            screen.blit(textsurface,bubble[0])
        


