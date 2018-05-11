# player interacts with all objects in the galaxy

import os
import pygame
import math
import copy

class Player(pygame.sprite.Sprite):
    # affected by gravitational pull of planets backholes
    # must catch the user's set amount of stars to win 
    # user sets the num of stars as goal
    def __init__(self,planetDict,starLst,meteorLst,goal,x=50,y=412):
        # colors
        self.losePopColor = (150,150)
        self.loseScoreColor = (553, 268)
        self.loseDistanceColor = (553, 350)
        self.loseTimeColor = (553, 438)
        self.loseReasonColor = (460,523)
        self.winPopColor = (150,150)
        self.winScoreColor = (553, 300)
        self.winDistanceColor = (553, 385)
        self.winTimeColor = (553, 470)
        # constant
        self.numThree = 3       # used in list index
        # planetDict = {"small": [[(x1,y1),(light1,dark1),False,23],\
        #[...],...],"medium": [], "large": [], "dark": []}
        # StarLst = [[x1,y1],[x2,y2],...] Left Top x,y
        # MeteorLst = [[[TLx1,TLy1],[dx,dy]],[[TLx,TLy],[ndx,ndy]],...] 
        # MeteorLst should be constantly updated
        self.meteorLst = meteorLst
        self.planetDict = planetDict
        self.starLst = starLst
        self.playerR = 10       # player radius
        self.width = 1100
        self.height = 825       # cannot go off boarders
        self.starSide = 24
        self.toleranceStar = 5  # catch a star within boarder range
        self.playerPosition = [self.playerR*2,self.height//2] # center position
        self.player = pygame.image.load("player.png")
        self.player = pygame.transform.scale(self.player,\
        (self.playerR*2,self.playerR*2))
        self.density = 0.001
        self.darkholeAdjust = 4/3
        self.darkholeEscapeSpeed = 15
        playerMassConstant = 0.5        # should be small
        self.playerMass = self.planetMass(playerMassConstant)
        self.cx = x         # CENTER x and y !!!
        self.cy = y
        self.dx = 2        # speed
        self.dy = 0
        self.fx = 0         # resultant force
        self.fy = 0
        self.ax = 0         # acceleration
        self.ay = 0
        self.gravityConstant = 1.e4
        # 1.e4 value is not universal gravitational constant, but\
        #referenced from: http://users.softlab.ntua.gr/~ttsiod/gravity.html
        self.win = False
        self.lose = False
        self.score = 0      # num of stars caught
        self.goal = goal
        self.outSideBoarderMargin = 100
        self.stick = False      # stick on planet
        self.offBoardTime = 0
        # losing summary
        self.loseReason = None
        # summary
        self.distance = 0
        self.time = 0       # in seconds
        fontSize = 36
        self.font = pygame.font.SysFont("comicsansms",fontSize)
        self.winPop = pygame.image.load("summaryWin.png")
        self.losePop = pygame.image.load("summaryLose.png")
        self.timerCalls = 0
        self.offBoardSeconds = 0
        self.maxOffBoardTime = 5
        # based on actual testing, about 20 calls per seconds
        self.callPerSecond = 20
        # track of player
        self.track = []
        self.showTrack = False
        self.trackButtonPosition = ((680, 758),(768, 802))
        self.white = (255,255,204)
        self.trackImage = pygame.image.load("track.png")

    def mousePressed(self,x,y):
        # click to show track
        if self.trackButtonPosition[0][0]<x<self.trackButtonPosition[1][0] and\
         self.trackButtonPosition[0][1]<y<self.trackButtonPosition[1][1]:
            self.showTrack = not self.showTrack
        if self.showTrack == False:
            self.track = []


    def timerFired(self):
        self.timerCalls += 1
        if self.timerCalls % self.callPerSecond == 0:
            self.time += 1
        if self.win == False and self.lose == False:
            # update player positions
            self.moveDueToGravity()
            if self.showTrack == True:
                self.track += [(self.cx,self.cy)]
            # check collision with darkhole, meteor, star
            if self.collideWithDarkhole():
                self.lose = True
                self.loseReason = "Dragged into a darkhole!"
            self.collideWithStar()
            if self.meteorLst != []:
                self.collideWithMeteor()
            if self.offBoard() == True:
                # check collision with boarder of screen
                self.offBoardTime += 1
                if self.offBoardTime % self.callPerSecond == 0:     
                    self.offBoardSeconds += 1
                if self.offBoardSeconds >= self.maxOffBoardTime:
                    self.lose = True
                    self.loseReason = "Off board 5 seconds!"
            else:
                self.offBoardTime = 0
                self.offBoardSeconds = 0
                


    def offBoard(self):
        if self.cx < 0 or self.cx > self.width or self.cy < 0 \
        or self.cy > self.height:
            return True
        return False
        

    def planetMass(self,radius):     
    # mass due to density and radius of mass (a spheric mass)
        # density due to area
        exponent = 3
        constant = 4 / 3
        volume = (math.pi * (radius ** exponent))* constant
        mass = self.density * volume
        return mass


    def gravityAcceleration(self,planetCX,planetCY,planetMass):
        distance = math.hypot((self.cx-planetCX),(self.cy-planetCY))
        if distance == 0:
            return (0,0)
        else:
            gravity = self.gravityConstant*\
            (self.playerMass*planetMass)/distance
            accelerationX = gravity * (planetCX - self.cx) / distance
            accelerationY = gravity * (planetCY - self.cy) / distance
        return (accelerationX, accelerationY)


    def resultantAcceleration(self):
        totalAccelerationX = 0
        totalAccelerationY = 0
        for key in self.planetDict:
            for item in self.planetDict[key]:
                if item[2] == False: continue   # dark planet no gravity
                radius = item[self.numThree]
                (cx , cy) = (item[0][0]+radius , item[0][1]+radius)
                if key == "small":
                    massRadius = 26
                elif key == "medium":
                    massRadius = 30
                elif key == "large":
                    massRadius = 35
                if key == "dark":
                    # darkholes have smaller gravity volume ratio
                    massRadius = radius * self.darkholeAdjust
                adjust = 10
                mass = self.planetMass(massRadius)/adjust
                (accelerationX, accelerationY) = \
                self.gravityAcceleration(cx,cy,mass)
                totalAccelerationX += accelerationX
                totalAccelerationY += accelerationY
        self.ax = totalAccelerationX
        self.ay = totalAccelerationY
        
    def moveDueToGravity(self):
        self.resultantAcceleration()
        # update current speed
        self.dx += self.ax
        self.dy += self.ay
        # update total distance
        self.distance += math.sqrt(self.dx**2+self.dy**2)
        originalCX = self.cx
        newCX = self.cx+self.dx
        newCY = self.cy+self.dy
        self.stick = False
        originalDX = self.dx
        if self.isValidMove(newCX,originalDX,self.cy,self.dy)==False:
            self.stick = True
            self.dx = 0
        else:
            self.cx = newCX
        if self.isValidMove(originalCX,originalDX,newCY,self.dy)==False:
            self.stick = True
            self.dy = 0
        else:
            self.cy = newCY
        self.playerPosition = [self.cx,self.cy]


    def isValidMove(self,cx,dx,cy,dy):  # these are player's data
    # check so that not cllide "into" planets(not darholes!!!) in X direction
        for key in self.planetDict:
            if key != "dark":
                for item in self.planetDict[key]:
                    planetRadius = item[self.numThree]
                    (planetCX, planetCY) = (item[0][0]+planetRadius , \
                    item[0][1]+planetRadius)
                    if self.toleranceCollide(cx,cy,planetCX,planetCY,\
                    planetRadius,0) == True:
                        collideInto = self.collideIntoDistance(cx,cy,\
                        planetCX,planetCY,planetRadius)
                        if 0 < collideInto < 2*self.playerR:
                            # tolerable collision, adjust self.dx \
                            #and self.dx to get the player out
                            self.pullOut(cx,cy,planetCX,planetCY,planetRadius)
                        # collide without tolerance value 
                        # perfect collide: edge to edge
                        return False
        return True
        
        
    def pullOut(self,cx,cy,planetCX,planetCY,planetRadius):
        #player might be embeded into a planet due to timer constraint in pygame
        # these codes are to correct the constraints by pulling the player out
        # find the connecting line between planet center and player center
        slope = (cy-planetCY)/(cx-planetCX)
        # need to trace this line to pull out
        adjust = 0.5
        pullGoal = self.playerR + planetRadius + adjust    
        # IMPORTANT!!! this is because if pulled a short distance from the 
        #surface, the player will be able to move swiftly\
        #due to gravitation from other planets, although the player is\
        #currently "stuck" to a planet, and its instantaneous dx,dy = 0
        # y = xk - x0k + y0    x0,y0 are planet centers, k is slope
        # pullGoal**2 = (x-x0)**2 + (y-y0)**2
        cx1 = math.sqrt(pullGoal**2/(slope**2+1))+planetCX
        cx2 = -math.sqrt(pullGoal**2/(slope**2+1))+planetCX
        cy1 = slope*(cx1-planetCX) + planetCY
        cy2 = slope*(cx2-planetCX) + planetCY
        # compare which solution is closer to original position
        if math.hypot((cx1-cx),(cy1-cy)) <= math.hypot((cx2-cx),(cy2-cy)):
            self.cx = cx1
            self.cy = cy1
        else:
            self.cx = cx2
            self.cy = cy2
        
        
    def collideIntoDistance(self,playerCX,playerCY,planetCX,planetCY,\
    planetRadius):     
    # player collides into sth (distance into)
        distance = math.hypot((playerCX-planetCX),(playerCY-planetCY))
        distanceInto = planetRadius + self.playerR - distance
        return distanceInto
        
        
    def toleranceCollide(self,playerCX,playerCY,planetCX,planetCY,\
    planetRadius,tolerance = 3):
    # for darkhole or for adjusting planetary collision position
        distance = math.hypot((playerCX-planetCX),(playerCY-planetCY))
        if (distance - tolerance) <= (planetRadius + self.playerR):
            return True
        return False
        
        
    def collideWithStar(self):      
    # being able to modify Star's self.starLst, and remove that collided star
    # StarLst = [[x1,y1],[x2,y2],...] Left Top x,y
        copyStarLst = copy.deepcopy(self.starLst)
        for star in copyStarLst:
            if self.toleranceCollide(self.cx,self.cy,star[0]+self.starSide/2,\
            star[1]+self.starSide/2,self.starSide/2,self.toleranceStar):
                self.starLst.remove(star)
                self.score += 1


    def collideWithMeteor(self):
        # MeteorLst = [[[TLx1,TLy1],[dx,dy]],[[TLx,TLy],[ndx,ndy]],...] 
        # should be constantly updated
        copyMeteorLst = copy.deepcopy(self.meteorLst)
        for meteor in copyMeteorLst:
            if self.toleranceCollide(self.cx,self.cy,\
            meteor[0][0]+self.starSide/2,meteor[0][1]+self.starSide/2,\
            self.starSide/2,self.toleranceStar):
                self.meteorLst.remove(meteor)
                self.score += 1
                
                
    def collideWithDarkhole(self):
        for item in self.planetDict["dark"]:
            radius = item[self.numThree]
            (cx , cy) = (item[0][0]+radius , item[0][1]+radius)
            if self.toleranceCollide(self.cx,self.cy,cx,cy,radius,\
            self.darkholeEscapeSpeed) and \
            (abs(self.dx)<self.darkholeEscapeSpeed \
            and abs(self.dy)<self.darkholeEscapeSpeed):
                # get sucked in
                return True
        return False


    def redrawAll(self,screen):
        screen.blit(self.player,(self.playerPosition[0]-self.playerR,\
        self.playerPosition[1]-self.playerR))
        screen.blit(self.trackImage,self.trackButtonPosition)
        if self.showTrack == True:
            for item in self.track:
                pygame.draw.circle(screen,self.white,\
                (int(item[0]),int(item[1])),1)
            #circle(Surface, color, pos, radius, width=0)
        # show winning summary or losing summary
        if self.win == True or self.lose == True:
            adjustDistance = 100
            score = self.font.render(str(self.score), True, (0, 0, 0))
            distance = self.font.render(str(int\
            (self.distance/adjustDistance)),True, (0, 0, 0))
            time = self.font.render(str(self.time), True, (0, 0, 0))
            if self.win == True:
                screen.blit(self.winPop, self.winPopColor)
                screen.blit(score,self.winScoreColor)
                screen.blit(distance,self.winDistanceColor)
                screen.blit(time,self.winTimeColor)
            if self.lose == True:
                screen.blit(self.losePop, self.losePopColor)
                screen.blit(score,self.loseScoreColor)
                screen.blit(distance,self.loseDistanceColor)
                screen.blit(time,self.loseTimeColor)
                reason = self.font.render(str(self.loseReason), True, (0, 0, 0))
                screen.blit(reason, self.loseReasonColor)


