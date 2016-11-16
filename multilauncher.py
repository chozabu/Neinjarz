#import pygame

#import terrain
import display

from math import hypot


import OpenGL.GL as GL

class multilauncher:
    def __init__(self, owner, ammo, filename):
        self.scale=1
        self.posmult = 0.01
        self.image = display.loadtex(filename)
        self.loadimage = display.loadtex("nothing.png")
        self.owner = owner
        self.ammo = ammo
        ammo(0,0,None)
        self.length = 0.001
        self.shooting = False
        self.timetofire = 0
        self.firedelay = 15
    def shoot(self,x,y):
      self.shooting = True
    def unshoot(self):
        self.shooting = False
    def shootcheck(self):
      pass
    def ammocheck(self, bullet):
      pass
    def update(self):
        if self.timetofire >= 0:
          self.timetofire-=1
        if self.shooting and self.timetofire < 0:
          self.shootcheck()
          self.shootabullet()
    def shootabullet(self):
        poix = self.owner.x+self.owner.dnx*16
        poiy = self.owner.y+self.owner.dny*16
        xv = self.owner.gmx-poix
        yv = self.owner.gmy-poiy
        self.length = hypot(xv,yv)
        if self.length == 0:self.length = 0.001
        xvn=xv/self.length
        yvn=yv/self.length
        newbullet = self.ammo(poix+xvn*8,poiy+yvn*8,self.owner)
        newbullet.xvel=self.owner.xvel*0.1+(xv)*0.1
        newbullet.yvel=self.owner.yvel*0.1+(yv)*0.1
        self.ammocheck(newbullet)
        self.owner.bullets.append(newbullet)
        self.timetofire = self.firedelay
    def dot(self,x1,y1,x2,y2):
        return x1*x2 + y1*y2
    def reflect(self,x,y,nx,ny):
        vdn = self.dot(x,y,nx,ny)*2
        return [x-nx*vdn,y-ny*vdn]
        #return self - normal*vdn
    def draw(self):
        ohs = self.owner.healthscale
        ohs = 1
        flippy = 1
        if self.owner.x > self.owner.gmx:
          flippy = -1
        #if self.on:
        GL.glPushMatrix()
        GL.glTranslatef(self.owner.cx, self.owner.cy, 0.0)
        GL.glRotatef(self.owner.aimgle,0,0,1)
        GL.glTranslatef(0.0, 12, 0.0)

        #print flippy
        GL.glTranslatef(self.owner.mx*self.posmult*ohs, self.owner.my*self.posmult*ohs, 0.0)
        GL.glScalef(flippy*self.scale,self.scale,1)
        GL.glScalef(8*ohs,8*ohs,12)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.image)
        if self.timetofire > 3:
          GL.glBindTexture(GL.GL_TEXTURE_2D, self.loadimage)
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0.0, 1.0)
        GL.glVertex3f(1.0, 1.0, 0.0)
        GL.glTexCoord2f(1.0, 1.0)
        GL.glVertex3f(-1.0, 1.0, 0.0)
        GL.glTexCoord2f(1.0, 0.0)
        GL.glVertex3f(-1.0, -1.0, 0.0)
        GL.glTexCoord2f(0.0, 0.0)
        GL.glVertex3f(1.0, -1.0, 0.0)
        GL.glEnd()
        GL.glPopMatrix()
