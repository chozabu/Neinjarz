

import terrain
from math import hypot, atan2
import OpenGL.GL as GL
import display

class basebomb:
    image = None
    def __init__(self, owner=None,x=0,y=0,image="nothing.png"):
        self.x = x
        self.y = y
        self.drag = 0.99
        self.destalpha = 35
        self.totalmoves = 200
        self.bouncecount = 0
        self.dead = 0
        self.angle = 0
        self.xvel = 0
        self.yvel = 0
        self.vel = 0
        self.xn = 0
        self.yn = 0
        self.grav = 0.3
        self.maxbounces = 0
        self.bouncing = 0
        self.owner = owner
        self.scale = 1
    def setVelocity(self, vel):
      ov=hypot(self.xvel,self.yvel)+0.000001
      self.xvel=self.xvel/ov*vel
      self.yvel=self.yvel/ov*vel
    def hitPlayer(self, p):
        pass
    def hitLand(self):
        pass
    def finalHitLand(self):
        pass
    def movPix(self):
        pass
    def timeUp(self):
        pass
    def movDone(self, x1, y1, x2, y2):
        pass

    
    def explode(self, radius):
        setto = self.destalpha
        terrain.explode(self.x, self.y, radius, setto)
        for p in self.owner.gamestate.walkers:
            p.bang(self.x, self.y+5, radius*1.8, setto,self.owner)
    
    def move(self):
        self.yvel +=self.grav
        self.yvel *=self.drag
        self.xvel *=self.drag
        self.vel = hypot(self.xvel, self.yvel)
        self.xn = self.xvel /self.vel
        self.yn = self.yvel /self.vel
        xs = self.x -self.xn*4
        ys = self.y -self.yn*4
        maxmoves = self.vel/5
        if maxmoves > 15: maxmoves = 15
        while maxmoves > 0:
            maxmoves -= 1
            self.x += self.xn*5
            self.y += self.yn*5
            #if self.x > terrain.x2 - 10:
            #    self.x-=terrain.x2-20
            #    #self.x = terrain.x2 - 10
            #    #self.finalHitLand()
            #    break
            if self.y > terrain.y2*3:
              self.dead = 1
              break
            #if self.y > terrain.y2 - 10:
            #    self.y-=terrain.y2-20
            #    #self.y = terrain.y2 - 10
            #    #self.finalHitLand()
            #    break
            #if self.x < 10:
            #    self.x+=terrain.x2-20
            #    #self.x = 10
            #    #self.finalHitLand()
            #    break
            #if self.y < 10:
            #    self.y+=terrain.y2-20
            #    #self.y = 10
            #    #self.finalHitLand()
            #    break
            if terrain.getalpha(int(self.x), int(self.y)) > 128:
                self.x -= self.xn*4
                self.y -= self.yn*4
                while terrain.getalpha(int(self.x), int(self.y)) < 128:
                  self.x += self.xn
                  self.y += self.yn
                self.bouncecount +=1
                if self.bouncecount > self.maxbounces:
                    self.finalHitLand()
                    break
                self.hitLand()
                if self.bouncing:
                    tn = terrain.getnormal(int(self.x), int(self.y))
                    self.x += tn[0]#*3
                    self.y += tn[1]#*3
                    nv = self.reflect(self.xn, self.yn, tn[0], tn[1])
                    self.xn = nv[0]
                    self.yn = nv[1]
                    self.xvel *= 0.7
                    self.yvel *= 0.7
                    self.xvel = self.xn * self.vel
                    self.yvel = self.yn * self.vel
            #self.movPix()
        self.totalmoves -= 1
        if self.totalmoves < 0:
            self.timeUp()
            self.dead = 1
        for c in self.owner.gamestate.clients:
            if c is self.owner: continue
            xd = c.cx - self.x
            yd = c.cy - self.y
            td = xd * xd + yd * yd
            if td < 250:
                self.hitPlayer(c)
        self.movDone(xs, ys, self.x - self.xn * 4, self.y - self.yn * 4)
        
        return 0
    
    def dot(self, x1, y1, x2, y2):
        return x1 * x2 + y1 * y2
    def reflect(self, x, y, nx, ny):
        vdn = self.dot(x, y, nx, ny) * 1.7
        return [x - nx * vdn, y - ny * vdn]
        #return self - normal*vdn
    def draw(self):
        self.angle = -atan2(-self.xvel, -self.yvel)/3.141573*180
        GL.glPushMatrix()
        GL.glTranslatef(self.x, self.y, 0.0)
        GL.glRotatef(self.angle, 0, 0, 1)
        GL.glScalef(8*self.scale, -8*self.scale, 8)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.image)
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glCallLists([display.qid2])
        GL.glPopMatrix()
