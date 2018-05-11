# star and meteor

import pygame
import random
import math
import os
import copy

class Star(pygame.sprite.Sprite):
    # No Gravity
    # count as a star once the player hits one (interact with player)
    # yellow stars have fixed location
    def __init__(self, goalNumber,planetDict):
        self.starImage = pygame.image.load("star.png")
        self.starSide = 24           # star side length
        self.starImage = pygame.transform.scale(self.starImage,\
        (self.starSide,self.starSide))
        self.numberOfStar = goalNumber + 2  # provide 2 more than goal
        self.margin = 80
        self.width = 1100
        self.height = 825
        self.starLst = self.createStarLst(planetDict)

    def createStarLst(self,planetDict):
        # [[x1,y1],[x2,y2],...] Left Top x,y
        # randomly place stars, but must NOT OVERLAP with any other objects
        # minimum margin between objects
        radius = self.starSide//2
        count = 0
        starLst = []
        while count < self.numberOfStar:
            x = random.randint(self.margin, \
            self.width-self.starSide-self.margin)
            y = random.randint(self.margin, \
            self.height-self.starSide-self.margin)
            if self.isValidLocationPlanet(planetDict,x,y,radius) == True\
            and self.isValidLocationStar(starLst,x,y,radius) == True :                  
                newStar = [x,y]
                count += 1
                starLst.append(newStar)
            else:
                continue
        return starLst

    def isValidLocationPlanet(self,planetDict,newX,newY,newRadius):    
    # no overlap with original planets
        centers = self.planetCenterLst(planetDict)
        minSpaceBetween = self.starSide
        for key in planetDict:
            if planetDict[key] == []: return True    # no planet yet
            (cx,cy)=(newX+newRadius,newY+newRadius)
            for item in centers:
                distance = math.sqrt((cx-item[0])**2+(cy-item[1])**2)
                if distance <= (newRadius + item[2] + minSpaceBetween):
                    return False
        return True

    def planetCenterLst(self,planetDict):
        centers = []        # [[cx0,cy0],[cx1,cy1],...]
        for key in planetDict:
            if key == "small": radius = 23
            if key == "medium": radius = 35
            if key == "large": radius = 57
            if key == "dark": radius = 20
            for item in planetDict[key]:
                itemCenter=[item[0][0]+radius, item[0][1]+radius,radius]
                centers.append(itemCenter)
        return centers

    def isValidLocationStar(self,starLst,newX,newY,radius):
        centers = self.starCenterLst(starLst,radius)
        minSpaceBetween = self.starSide
        if starLst == []:return True    # no star yet
        for item in starLst:
            (cx,cy)=(newX+radius,newY+radius)
            for item in centers:
                distance = math.sqrt((cx-item[0])**2+(cy-item[1])**2)
                if distance <= (self.starSide + minSpaceBetween):
                    return False
        return True

    def starCenterLst(self,starLst,radius):
        centers = []
        for item in starLst:
            itemCenter=[item[0]+radius, item[1]+radius]
            centers.append(itemCenter)
        return centers

    def redrawAll(self,screen):
        for star in self.starLst:
            screen.blit(self.starImage,star)



class Meteor(pygame.sprite.Sprite):
    # No Gravity
    # count as a star once the player hits one
    # random direction of motion; come once every 25-35 seconds
    # move in groups of 10 to 20 into screen and out(constant linear motion)
    def __init__(self):
        self.dx = 10
        self.dy = 10
        self.rainDelay = 500
        self.rainDelayUB = 700      # upper bound
        self.meteorImage = pygame.image.load("meteor.png")
        self.timerCall = 0
        self.meteorSide = 24           # star side length
        self.meteorImage = pygame.transform.scale(self.meteorImage,\
        (self.meteorSide,self.meteorSide))
        self.width = 1100
        self.height = 825
        self.meteorRainLst = []
        self.angle = 90
        # list of all starting positions
        self.allDirections = [[-self.meteorSide,-self.meteorSide],\
        [self.width+self.meteorSide,-self.meteorSide],\
        [-self.meteorSide,self.height+self.meteorSide],\
        [self.width+self.meteorSide,self.height+self.meteorSide]]
        self.five = 5 
        self.ten = 10
        self.twenty = 20
        
    
    def timerFired(self):
        self.timerCall += 1
        # new round of meteor rain
        if self.timerCall % self.rainDelay == 0:
            self.meteorRainLst = self.meteorRain()
            self.rainDelay = random.randint(self.rainDelay,self.rainDelayUB) 
        # no meteor on screen
        if self.meteorRainLst != []:
            for meteor in self.meteorRainLst:
                meteor[0][0] += meteor[1][0]
                meteor[0][1] += meteor[1][1]
        if self.timerCall % 2 == 0:        
                meteorCopy = copy.copy(self.meteorImage)
                new = pygame.transform.rotate(meteorCopy, self.angle)
                self.meteorImage = new


    def meteorRain(self):
        # meteorRainLst = [[[TLx1,TLy1],[dx,dy]],[[TLx,TLy],[ndx,ndy]],...]
        # all in one direction, dx and dy are multiples of each other
        #this list changes every time;items in it are removed once go off board
        #or player touches one
        # random frequency of occurance:
        meteorRainLst = []
        self.meteorNum = random.randint(self.ten,self.twenty)
        # starting point on screen, always travel in diagonal directions
        index = random.randint(0,len(self.allDirections)-1)
        allDirection = copy.deepcopy(self.allDirections)
        # avoid aliasing which changes original self.allDirections !!!
        newDirection = allDirection[index]
        adjustment = [self.ten,self.ten]
        if newDirection[0] <= 0:
            dx = random.randint(self.five,self.ten)
            adjustment[0] = -adjustment[0]
        if newDirection[0] >= self.width:
            dx = -random.randint(self.five,self.ten)
        if newDirection[1] <= 0:
            dy = random.randint(self.five,self.ten)
        if newDirection[1] >= self.height:
            dy = -random.randint(self.five,self.ten)
            adjustment[0] = -adjustment[0]
        for i in range(self.meteorNum):
            multiple = random.randrange(1,self.five)
            newDirection = [newDirection[0]+adjustment[0]*i,\
            newDirection[1]+adjustment[1]*i]
            new = [newDirection] + [[dx*multiple,dy*multiple]]
            meteorRainLst.append(new)
        return meteorRainLst
        
        
    def redrawAll(self,screen):
        for meteor in self.meteorRainLst:
            screen.blit(self.meteorImage,meteor[0])




