#import pygame
#import terrain
#import display
#import simplenet
from math import *
from baseparticle import baseparticle
from random import random
import display

class smokeparticle(baseparticle):
    def __init__(self,x,y,image,scale,startspeed, colour=[1,1,1]):
        xv = (random()*10-5)*startspeed
        yv = (random()*10-5)*startspeed
        baseparticle.__init__(self,x+xv,y+yv,xv,yv,image)
        self.x+=xv*(scale*1.4+8)
        self.y+=yv*(scale*1.4+8)
        self.scale = scale
        self.grav = random()*0.4-0.25
        self.totalmoves = 15.0
        self.startmoves = 25.0
        self.colour = colour
        self.image = display.loadtex(image)
        
