import terrain
import display

from math import hypot


import OpenGL.GL as GL
#from OpenGL.GLU import *

class rope:
    def __init__(self, owner):
        self.image = display.loadtex("grapple.png")
        self.on = 0
        self.owner = owner
        self.x = 0
        self.y = 0
        self.length = 0
        self.angle = 0
    def unshoot(self):
      self.on = 0
    def shoot(self, x, y):
        xv = x - self.owner.x
        yv = y - self.owner.y
        self.length = hypot(xv, yv)
        if self.length == 0:self.length = 0.001
        dirx = xv / self.length
        diry = yv / self.length
        self.angle = self.owner.aimgle
        #self.length/=2
        xy = terrain.traceline(self.owner.x+dirx, self.owner.y+diry, xv, yv, 800)
        #self.xy=(x, y)
        #if xy != None:
        for i in self.owner.gamestate.clients:
            pdx = i.x-self.owner.x
            pdy = i.y-self.owner.y
            pdx*= dirx
            pdy*= diry
            print pdx,pdy
            
        if xy != None:
            self.x, self.y = xy
            #self.x-=dirx*80
            #self.y-=diry*80
            self.length = hypot(self.x-self.owner.x, self.y-self.owner.y)*0.85
            self.on = 1
        else:
            self.on = 0
    def update(self):
        if self.on:
            #self.length*=0.998
            xv = self.x-self.owner.x
            yv = self.y-self.owner.y
            dist = hypot(xv, yv)
            #if dist == 0:dist = 0.001
            if dist > self.length:
              yv /= dist
              xv /= dist
              diffd = dist-self.length
              self.owner.xvel += xv*diffd*0.03
              self.owner.yvel += yv*diffd*0.03
              #self.owner.xvel+=(self.x-self.owner.x)*0.01
              #self.owner.yvel+=(self.y-self.owner.y)*0.01
    def draw(self):
        GL.glPushMatrix()
        if self.on:
            GL.glLineWidth(2)
            GL.glDisable(GL.GL_TEXTURE_2D)
            GL.glColor4f(0.5, 0.25, 0.05, 1.0)
            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(self.x, self.y, 0.0)
            GL.glVertex3f(self.owner.cx, self.owner.cy, 0.0)
            GL.glEnd()
            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glTranslatef(self.x, self.y, 0.0)
            GL.glRotatef(self.angle, 0, 0, 1)
        else:
            GL.glTranslatef(self.owner.cx, self.owner.cy, 0.0)
            GL.glTranslatef(self.owner.mx/10, self.owner.my/10, 0.0)
            GL.glRotatef(self.owner.aimgle, 0, 0, 1)
        #angle = -atan2(-self.xvel, -self.yvel)/3.141573*180
        #glRotatef(angle, 0, 0, 1)
        if self.on:
            GL.glScalef(12*self.owner.healthscale, 12*self.owner.healthscale, 1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.image)
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0.0, 1.0)
            GL.glVertex3f(1.0, 0.5, 0.0)

            GL.glTexCoord2f(1.0, 1.0)
            GL.glVertex3f(-1.0, 0.5, 0.0)

            GL.glTexCoord2f(1.0, 0.0)
            GL.glVertex3f(-1.0, -1.50, 0)

            GL.glTexCoord2f(0.0, 0.0)
            GL.glVertex3f(1.0, -1.50, 0)
            GL.glEnd()
        GL.glPopMatrix()
