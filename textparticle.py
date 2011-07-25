#import pygame
#import terrain
import display
#import simplenet
from math import *
from baseparticle import baseparticle
from random import random

class textparticle(baseparticle):
    def __init__(self,x,y,image,scale,startspeed, colour=[1,1,1]):
        xv = (random()*10-5)*startspeed*0
        yv = (random()*10-5)*startspeed*0
        baseparticle.__init__(self,x+xv,y+yv,xv,yv,image)
        self.x+=xv*(scale*1.4+8)
        self.y+=yv*(scale*1.4+8)
        self.scale = scale
        self.grav = random()*0.4-0.25
        self.totalmoves = 15.0
        self.startmoves = 45.0
        self.colour = colour
        self.image = image
    def draw(self):
        #print self.x,self.y
        #print self.scale
        display.drawWord(pos=[self.x,self.y,0], string=self.image, color=self.colour,size=self.scale)
