# options in the "menu": "game", "help", "about", "bonus", "music"

from zclassicMode import *
from zbonusMode import *
import pygame
import os
import copy


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        # some constants
        self.numThree = 3               # used in list index
        self.numTwoTwoFive = 255        # used in color
        self.keyCodeOfa = 97
        self.keyCodeOfz = 122
        self.keyCodeOfEnter = 13
        self.keyCodeOfDelete = 8
        self.maxNameLen = 8
        # BGM
        self.BGM = pygame.mixer.music.load("Caketown 1.mp3")
        # this BGM is from: http://www.matthewpablo.com/contact
        # http://opengameart.org/users/matthewpablo
        volume = 0.4
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        self.pauseMusic = False
        self.musicImage = (pygame.image.load("music.png"),\
        pygame.image.load("musicNo.png"))
        self.musicPosition = (50,50)
        self.musicRB = (170,122)        # right bottom
        # main images
        self.menuImage = pygame.image.load("starter.png")
        self.help = pygame.image.load("help.png")
        self.about = pygame.image.load("notice.png")
        # board size
        self.width = 1100
        self.height = 825
        # from bottom layer of buttom to top layer
        self.bubbleAbout = pygame.image.load("aboutbutton.png")
        self.bubbleHelp = pygame.image.load("helpbutton.png")
        self.bubbleGame = pygame.image.load("startbutton.png")
        self.bubbleBonus = pygame.image.load("bonus.png")
        self.bubbleLeave = ((940, 727),(1095, 820)) # go back to menu
        self.currentMode = "menu"
        self.bubbles = self.bubbleInitialRandomMotion()
        self.timerCall = 0
        self.modeDict = {self.bubbleAbout: "about", self.bubbleHelp: "help",\
        self.bubbleGame: "game",self.bubbleBonus: "bonus"}
        self.changeRate = 300
        self.magicNum = 5   # for random call
        self.classicMode = ClassicMode()
        self.timerPeriod = 150
        self.bonusMode = BonusMode()
        # you must read helpPage before playing!
        self.read = pygame.image.load("readHelp.png")
        self.readHelp = False
        self.showReadMessge = False
        self.rankImage = pygame.image.load("rank.png")
        self.readImagePosition = (100,self.height/10)
        # players and text recordings
        self.enterNamePosition = [1260,618]
        self.nameImagePosition = [1100,60]
        self.nameImageSpeed = -20
        self.nameImageFinalPosition = [340,369]
        self.playerName = ""
        self.finishEnteringName = False
        self.nameImage = pygame.image.load("name.png")
        fontSize = 20
        self.font = pygame.font.SysFont("comicsansms", fontSize)     
        # used for modifying and updating text file
        self.topThree = self.readFile("rank.txt") 
        self.addWealth = 0
        self.wealth = 0
        self.first = self.getRankLst(1)
        self.second = self.getRankLst(2)
        self.third = self.getRankLst(self.numThree)
        self.firstPosition = ((594,542),(825,542))
        self.secondPosition = ((594,600),(825,600))
        self.thirdPosition = ((594,658),(825,658))
        self.rankImagePosition = (318,481)


    def getRankLst(self,rank):
        for item in self.topThree:
            currentRank = item[2]
            if currentRank == rank:
                return item


    def readFile(self,path):
    # gives a list of every line in the file
    # if does not exist, creates one
    # file records top three:
    # each line: "name/wealth/rank\n"
        if not os.path.exists(path):
            f = open(path,"w+")
        f = open(path,"r")
        lines = []
        for line in f:      # without ending "\n"
            if line[-1] == "\n":
                line = line[:-1]
            lst = line.split("/")
            lst[1] = int(lst[1])
            lst[2] = int(lst[2])
            lines.append(lst)
            # lines = [["name",wealth,rank],...]
        return lines
     
        
    def writeFile(self, path, addWealth):
        f = open(path, "w")
        lines = self.topThree
        existingPlayer = False
        for item in lines:
            if item[0] == self.playerName:
                item[1] += addWealth
                existingPlayer = True
        if existingPlayer == False:
            copyLine = copy.deepcopy(lines)
            for item in copyLine:
                rank = item[2]
                # if more than 3 players, truncate to 3
                if rank == self.numThree:
                    lines.remove(item)
            lines.append([self.playerName,0,self.numThree])
        self.topThree = lines
        # rank the players
        rankLst = []
        for item in self.topThree:
            rankLst.append(item[1])
        rankLst = sorted(rankLst)[::-1]
        
        newTop = []
        existingRanks = []
        for item in self.topThree:
            wealth = item[1]
            rank = rankLst.index(wealth)+1
            while (rank in existingRanks):
                rank += 1
            existingRanks.append(rank)
            item[2] = rank
        text = ""
        for item in self.topThree:
            text += str(item[0]+"/"+str(item[1])+"/"+str(item[2])+"\n")
        text = text[:-1]         # truncate the last "\n"
        f.write(text)
        
        
    def mousePressed(self,x,y):
        # can only click in bubbles during "menu" mode
        if self.currentMode == "menu":
            if self.musicPosition[0] < x < self.musicRB[0] and \
            self.musicPosition[1] < y < self.musicRB[1]:
                self.pauseMusic = not (self.pauseMusic)
                if self.pauseMusic == True:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if self.finishEnteringName == True:
                for bubble in self.bubbles:
                    (LTx,LTy) = self.bubbles[bubble][0]
                    (width,height) = self.bubbles[bubble][2]
                    if LTx<x<LTx+width and LTy<y<LTy+width:
                        # clicked inside the bubble
                        if self.readHelp == False:
                            if bubble == self.bubbleGame or\
                             bubble == self.bubbleBonus:
                                self.showReadMessge = True
                            elif bubble == self.bubbleHelp:
                                self.readHelp = True
                                self.showReadMessge = False
                                self.currentMode = self.modeDict[bubble]
                            elif bubble == self.bubbleAbout:
                                self.currentMode = self.modeDict[bubble]
                        else:
                            self.currentMode = self.modeDict[bubble]
        elif self.currentMode == "help" or self.currentMode == "about":       
        # current mode is ("game" or) "help" or "about"
            if self.bubbleLeave[0][0]<x<self.bubbleLeave[1][0] and \
            self.bubbleLeave[0][1]<y<self.bubbleLeave[1][1]:
                self.currentMode = "menu"
        elif self.currentMode == "game":
            self.classicMode.mousePressed(x,y)
            if self.classicMode.leave == True:      # back to menu option
                self.addWealth = self.classicMode.totalScoreInARound
                self.currentMode = "menu"
                # important!!! set back to DEFAULT condition
                self.classicMode = ClassicMode()
        elif self.currentMode == "bonus":
            self.bonusMode.mousePressed(x,y)
            if self.bonusMode.leave == True:      # back to menu option
                self.addWealth = self.bonusMode.totalScoreInARound
                self.currentMode = "menu"
                self.bonusMode = BonusMode()


    def bubbleInitialRandomMotion(self):
        # random direction and speed of linear movement
        randConstant = 8
        bubbles = {self.bubbleAbout: None, self.bubbleGame: None,\
        self.bubbleBonus: None, self.bubbleHelp: None}
        for bubble in bubbles:
            width = bubble.get_size()[0]
            height = bubble.get_size()[1]
            LTx = random.randint(0,self.width-width)
            LTy = random.randint(0,self.height-height)
            dx = random.randint(-randConstant,randConstant)
            dy = random.randint(-randConstant,randConstant)
            bubbles[bubble] = [[LTx,LTy],[dx,dy],[width,height]]
        return bubbles


    def timerFired(self):
        self.timerCall += 1
        # update bubble positions
        if self.currentMode == "menu":
            if self.nameImagePosition[0] > self.nameImageFinalPosition[0]:
                self.nameImagePosition[0] += self.nameImageSpeed
                self.enterNamePosition[0] += self.nameImageSpeed
            if self.finishEnteringName == True:
                for bubble in self.bubbles:
                    (LTx,LTy) = self.bubbles[bubble][0]
                    (dx,dy) = self.bubbles[bubble][1]
                    (width,height) = self.bubbles[bubble][2]
                    # check if bubble in bound and change it's speed
                    if not (0 < LTx + dx < self.width - width):
                        self.bubbles[bubble][1][0] = -self.bubbles[bubble][1][0]
                        dx = -dx
                    if not (0 < LTy + dy < self.height - height):
                        self.bubbles[bubble][1][1] = -self.bubbles[bubble][1][1]
                        dy = -dy
                    self.bubbles[bubble][0][0] += dx
                    self.bubbles[bubble][0][1] += dy
                    if self.timerCall % self.timerPeriod == 0:
                        randConstant = 8
                        self.bubbles[bubble][1] = [random.randint\
                        (-randConstant,randConstant), random.randint\
                        (-randConstant,randConstant)] 
                self.writeFile("rank.txt",self.addWealth)
                # clear after executing once
                self.addWealth = 0
                self.first = self.getRankLst(1)
                self.second = self.getRankLst(2)
                self.third = self.getRankLst(self.numThree)
        elif self.currentMode == "game":
            self.classicMode.timerFired()
        elif self.currentMode == "bonus":
            self.bonusMode.timerFired()

            
    def mouseMotion(self,x,y):
        if self.currentMode == "bonus":
            self.bonusMode.mouseMotion(x,y)


    def keyPressed(self, keyCode):
        if self.currentMode == "menu" and self.finishEnteringName == False:
            if keyCode == self.keyCodeOfEnter:
                if self.playerName != "":
                    self.finishEnteringName = True
                    #self.entryTime = len(self.textFileDict)
                    self.content = [self.playerName,0]
            if len(self.playerName) <= self.maxNameLen:
                if keyCode>=self.keyCodeOfa and keyCode <= self.keyCodeOfz:
                    self.playerName += chr(keyCode)
            if keyCode == self.keyCodeOfDelete:
                # delete last
                if len(self.playerName) >= 1:
                    self.playerName = self.playerName[:-1]
        if self.currentMode == "game":
            self.classicMode.keyPressed(keyCode)
        if self.currentMode == "bonus":
            self.bonusMode.keyPressed(keyCode)


    def redrawAll(self,screen):
        if self.currentMode == "menu":
            screen.blit(self.menuImage,(0,0))
            if self.pauseMusic == False:
                screen.blit(self.musicImage[0],self.musicPosition)
            else:
                screen.blit(self.musicImage[1],self.musicPosition)
            if self.finishEnteringName == False:
                screen.blit(self.nameImage,self.nameImagePosition)
                name = self.font.render(str(self.playerName), True, (0, 0, 0))
                screen.blit(name,self.enterNamePosition)
            else:
                screen.blit(self.rankImage,self.rankImagePosition)
                self.drawRank(screen)
                for bubble in self.bubbles:
                    (LTx,LTy) = self.bubbles[bubble][0]
                    screen.blit(bubble,(LTx,LTy))
                if self.showReadMessge == True:
                    screen.blit(self.read,self.readImagePosition)
        elif self.currentMode == "help":
            screen.blit(self.help,(0,0))
        elif self.currentMode == "about":
            screen.blit(self.about,(0,0))
        elif self.currentMode == "bonus":
            self.bonusMode.redrawAll(screen)
        elif self.currentMode == "game":
            self.classicMode.redrawAll(screen)


    def drawRank(self,screen):
        # there is no way to shorten this function since each position 
        #is unique, so I do it the controversial way
        # display name and wealth
        if len(self.topThree) >= 1:
            firstName = self.first[0]
            firstWealth = str(self.first[1])
            firstN = self.font.render(firstName, True, \
            (self.numTwoTwoFive, self.numTwoTwoFive, 0))
            first = self.font.render(firstWealth, True, \
            (self.numTwoTwoFive, self.numTwoTwoFive, 0))
            screen.blit(firstN,self.firstPosition[0])
            screen.blit(first,self.firstPosition[1])
        if len(self.topThree) >= 2:
            secondName = self.second[0]
            secondWealth = str(self.second[1])
            secondN = self.font.render(secondName, True, \
            (self.numTwoTwoFive, 0, self.numTwoTwoFive))
            second = self.font.render(secondWealth, True, \
            (self.numTwoTwoFive, 0, self.numTwoTwoFive))
            screen.blit(secondN,self.secondPosition[0])
            screen.blit(second,self.secondPosition[1])
        if len(self.topThree) == self.numThree:
            thirdName = self.third[0]
            thirdWealth = str(self.third[1])
            thirdN = self.font.render(thirdName, True, \
            (0, self.numTwoTwoFive, self.numTwoTwoFive))
            third = self.font.render(thirdWealth, True, \
            (0, self.numTwoTwoFive, self.numTwoTwoFive))
            screen.blit(thirdN,self.thirdPosition[0])
            screen.blit(third,self.thirdPosition[1])
       
        
