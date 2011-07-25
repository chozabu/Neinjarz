#import pygame
#import terrain
import display
#import simplenet
from math import atan2, cos
import OpenGL.GL as GL
#from OpenGL.GLU import *

class baseparticle:
    #image = display.loadtex("nothing.png")
    def __init__(self,x,y,xv,yv,image):
        self.x = x
        self.y = y
        self.xvel = xv
        self.yvel = yv
        self.totalmoves = 100
        self.startmoves = 10
        self.dead = 0
        self.angle = 0
        self.vel = 0
        self.scale = 1
        self.movesleft = 0
        self.xn = 0
        self.yn = 0
        self.grav = 0.3
        self.xgrav = 0.0
        self.colour = [1,1,1]
        self.image = 0
    
    def timeUp(self):
        pass
    
    def move(self):
        self.yvel+=self.grav
        self.xvel+=self.xgrav
        self.yvel*=0.99
        self.xvel*=0.99
        self.x+=self.xvel
        self.y+=self.yvel
        '''self.vel = hypot(self.xvel,self.yvel)
        self.xn = self.xvel/self.vel
        self.yn = self.yvel/self.vel
        xs = self.x-self.xn*4
        ys = self.y-self.yn*4'''
        self.totalmoves-=1
        if self.totalmoves<0:
            self.timeUp()
            self.dead = 1
        return 0
    
    def dot(self,x1,y1,x2,y2):
        return x1*x2 + y1*y2
    def reflect(self,x,y,nx,ny):
        vdn = self.dot(x,y,nx,ny)*1.7
        return [x-nx*vdn,y-ny*vdn]
        #return self - normal*vdn
    def draw(self):
        GL.glPushMatrix()
        GL.glTranslatef(self.x, self.y, 0.0)
        #self.angle = -atan2(cos(-self.xvel),-self.yvel)/3.141573*180
        #GL.glRotatef(self.angle,0,0,1)
        #GL.glScalef(8,-8,8)
        dectime = self.totalmoves/self.startmoves
        agemod = 0.6+(dectime)*0.4
        GL.glScalef(self.scale*agemod*8,self.scale*agemod*-8,1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.image)
        GL.glColor4f(self.colour[0],self.colour[1],self.colour[2],(dectime*0.9))
        GL.glCallLists([display.qid])
        GL.glPopMatrix()
