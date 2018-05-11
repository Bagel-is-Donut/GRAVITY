# planets and darkholes

import pygame
import random
import math
import os
import copy

class Planet(pygame.sprite.Sprite):
    # click on: color & gravity
    # click off: black n white & no gravity
    def __init__(self, numDict):
        self.planet0 = pygame.image.load("0.png")
        self.planet1 = pygame.image.load("1.png")
        self.planet2 = pygame.image.load("2.png")
        self.planet3 = pygame.image.load("3.png")
        self.planet4 = pygame.image.load("4.png")
        self.planet5 = pygame.image.load("5.png")
        self.dark012 = pygame.image.load("dark012.png")
        self.dark345 = pygame.image.load("dark345.png")
        self.darkhole = pygame.image.load("darkhole.png")
        self.angle = 90
        self.timerCalls = 0
        # number of each type
        self.smallNum = numDict["S"]
        self.mediumNum = numDict["M"]
        self.largeNum = numDict["L"]
        self.darkNum = numDict["D"]
        # radius
        self.radiusSmall = 23
        self.radiusMedium = 35
        self.radiusLarge = 57
        self.radiusDarkholeSmall = 15
        self.radiusDarkholeBig = 35
        # all image pairs [(light,dark),...]
        self.planetImages = [(self.planet0,self.dark012),\
        (self.planet1,self.dark012),(self.planet2,self.dark012),\
        (self.planet3,self.dark345),(self.planet4,self.dark345),\
        (self.planet5,self.dark345)]
        # avoid magic num
        self.numThree = 3       # used in list index
        # screen size
        self.width = 1100
        self.height = 825
        self.planetDict = self.createPlanetDict()



    def createPlanetDict(self):
        # random position and images of planets
        # {"small": [[(x1,y1),(light1,dark1),False,23],[...],...], \
        #"medium": [], "large": [], "dark": []}
        # values [(LTx, LTy), imageTupleOfPlanet,lightUp,radius,num]
        planetDict = {"small": [], "medium": [], "large": [], "dark": []}
        lightUp = [False,True]
        planetImageNum = len(self.planetImages)
        for key in planetDict:
            if key == "small": 
                num = self.smallNum
                radius = self.radiusSmall
            if key == "medium": 
                num = self.mediumNum
                radius = self.radiusMedium
            if key == "large": 
                num = self.largeNum
                radius = self.radiusLarge
            if key == "dark": 
                continue
            count = 0
            while count < num:
                # radius*2 is the margin
                x = random.randint(radius*2, self.width-radius*2-radius)
                y = random.randint(radius*2, self.height-radius*2-radius)
                if self.isValidLocation(planetDict,x,y,radius)==True:  
                    # choose random images
                    planetImage = self.planetImages\
                    [random.randint(0,planetImageNum-1)]
                    planetImage = (pygame.transform.scale(planetImage[0],\
                        (radius*2,radius*2)),pygame.transform.scale\
                        (planetImage[1],(radius*2,radius*2)))
                    light = lightUp[random.randint(0,1)]
                    newPlanet = [(x,y),planetImage,light,radius]
                    count += 1
                    planetDict[key].append(newPlanet)
        # darkholes
        num = self.darkNum
        count = 0
        darkLeftMargin = 200  
        # shouldn't be too close to player's initial position in Center Left
        while count < num:
            radius = random.randint\
            (self.radiusDarkholeSmall,self.radiusDarkholeBig)
            x = random.randint(darkLeftMargin, self.width-radius*2-radius)
            y = random.randint(radius, self.height-radius*2-radius)
            if self.isValidLocation(planetDict,x,y,radius)==True:  
                image = (pygame.transform.scale(self.darkhole,\
                (radius*2,radius*2)),pygame.transform.scale\
                (self.darkhole,(radius*2,radius*2)))
                new = [(x,y),image,True,radius]
                planetDict["dark"].append(new)
                count += 1
        return planetDict
        
        
    def isValidLocation(self,planetDict,newX,newY,newRadius):    
    # no overlap with original planets
        centers = self.planetCenterLst(planetDict)
        minSpaceBetween = 50
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
            if key == "small": radius = self.radiusSmall
            if key == "medium": radius = self.radiusMedium
            if key == "large": radius = self.radiusLarge
            if key == "dark": radius = self.radiusDarkholeBig
            for item in planetDict[key]:
                itemCenter=[item[0][0]+radius, item[0][1]+radius,radius]
                centers.append(itemCenter)
        return centers


    def mousePressed(self, x, y):
        # if click inside a planet, it's state changes
        # light: have gravity and color
        # dark: no gracity nor color
        # self.planetLst[i][2]==True --> light
        # self.planetLst[i][2]==False --> dark 
        for key in self.planetDict:
            if key == "dark": continue
            for item in self.planetDict[key]:
                radius = item[self.numThree]
                cx,cy = item[0][0]+radius, item[0][1]+radius
                distance = math.sqrt((x-cx)**2+(y-cy)**2)
                if distance <= radius:
                    item[2] = not (item[2])

    def timerFired(self):
        self.timerCalls += 1
        # rotate Darkhole
        if self.timerCalls % 2 == 0:
            for item in self.planetDict["dark"]:
                darkholeCopy = copy.copy(item[1][0])
                new = pygame.transform.rotate(darkholeCopy, self.angle)
                item[1] = (new,new)
        

    def redrawAll(self,screen):
        for key in self.planetDict:
            for planet in self.planetDict[key]:
                if planet[2] == True:
                    screen.blit(planet[1][0],planet[0])
                else:
                    screen.blit(planet[1][1],planet[0])
                pass








