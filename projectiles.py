
import terrain
import display
from math import atan2
from basebomb import basebomb
import random
import particles

#        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/10, int((self.radius-5)*0.15+1))
#        particles.addParticle(self.x, self.y, 0.5, "fire.png", self.radius/10, int((self.radius-5)*0.05+1))

class shell(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self)
        self.owner = owner
        self.x = float(xp)
        self.y = float(yp)
        self.image = display.loadtex("shell.png")
        self.radius = 50

    def hitPlayer(self,p):
        self.finalHitLand()
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/10, int((self.radius-5)*0.15+1))
        particles.addParticle(self.x, self.y, 0.5, "fire.png", self.radius/10, int((self.radius-5)*0.05+1))


class bulletshotgun(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp)
        self.image = display.loadtex("bulletshotgun.png")
        self.radius = 9
        self.scale = 0.6
        self.drag = 0.995
        self.grav = 0.1
        self.maxbounces=2

    def hitPlayer(self,p):
        self.dead = 1
        p.damage(9, self.owner)
        p.xvel += self.xvel*0.1
        p.yvel += self.yvel*0.1
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
    def hitLand(self):
        self.explode(self.radius/2)

class bullet(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp)
        self.image = display.loadtex("bullet.png")
        self.radius = 9
        self.scale = 1
        self.drag = 0.995
        self.grav = 0.1
        self.maxbounces=2

    def hitPlayer(self,p):
        self.dead = 1
        p.damage(9, self.owner)
        p.xvel += self.xvel*0.1
        p.yvel += self.yvel*0.1
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
    def hitLand(self):
        self.explode(self.radius/2)
class chainbullet(bullet):
    def __init__(self, xp,yp,owner):
        bullet.__init__(self,xp,yp,owner)
        self.maxbounces = 1
        self.radius = 7
	
class sniperbullet(bullet):
    def __init__(self, xp,yp,owner):
        bullet.__init__(self,xp,yp,owner)
        self.maxbounces=7
        self.drag = 0.999
        self.grav = 0.01


class arrow(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp)
        self.image = display.loadtex("arrow.png")
        self.pix = display.loadpixID("arrow.png")
    
    def hitPlayer(self, p):
        self.dead = 1
        p.damage(26, self.owner)
        p.xvel += self.xvel
        p.yvel += self.yvel
    def finalHitLand(self):
        self.dead = 1
        myangle = atan2(-self.xvel, -self.yvel)/3.141573*180.0
        self.movesleft = 0
        xpos = self.x-self.xn*6
        ypos = self.y-self.yn*6
        terrain.pastesurfID(self.pix, xpos, ypos, myangle, 0.5)

class hominarrow(arrow):
    def __init__(self, xp,yp,owner):
        arrow.__init__(self,xp,yp,owner)
        self.image = display.loadtex("knife.png")
        self.pix = display.loadpixID("knife.png")
    def movDone(self, x1, y1, x2, y2):
      for i in self.owner.gamestate.clients:
        if i == self.owner: continue
        xd = i.x-self.x
        yd = i.y-self.y
        td = xd*xd+yd*yd
        if td < 125*125:
          self.xvel+=xd*0.05
          self.yvel+=yd*0.05


class guidedknife(arrow):
    def __init__(self, xp,yp,owner):
        arrow.__init__(self,xp,yp,owner)
        self.image = display.loadtex("grapple.png")
        self.pix = display.loadpixID("grapple.png")
    def movDone(self, x1, y1, x2, y2):
        xd = self.owner.gmx-self.x
        yd = self.owner.gmy-self.y
        td = xd*xd+yd*yd
        self.xvel+=xd*0.05
        self.yvel+=yd*0.05

class bridger(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp)
        self.image = display.loadtex("empty.png")
        self.pix = display.loadpixID("brick.png")
        self.destalpha = 35
        self.radius = 15
        self.maxbounces = 5

    def hitPlayer(self,p):
        self.explode(12)
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
    def hitLand(self):
        self.explode(12)
    def movDone(self,x1,y1,x2,y2):
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", 2.5, 1,[0.7,0.7,0.4])
        if self.vel < 14:
          self.xvel*=1.1
          self.yvel*=1.1
        if self.vel > 15:
          self.xvel*=0.9
          self.yvel*=0.9
        myangle = atan2(-self.xvel, -self.yvel)/3.141573*180.0
	if self.xvel<0:
	   myangle+=180
        xpos = self.x-self.xn*6
        ypos = self.y-self.yn*6
        terrain.pastesurfID(self.pix, x1, y1+2, myangle, 0.6)
        

class dirtclod(basebomb):
    #image = display.loadtex("dirtclod.png")
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp)
        #self.xvel+=random.randrange(-10,10)
        #self.yvel+=random.randrange(-10,10)
        self.image = display.loadtex("dirtclod.png")
        self.pix = display.loadpixID("dirtclod.png")
        self.destalpha = 235

    def hitPlayer(self,p):
        self.explode(15)
        self.finalHitLand()
    def finalHitLand(self):
        self.dead = 1
        #self.explode(30)
        myangle = atan2(-self.xvel,-self.yvel)/3.141573*180.0
        self.movesleft = 0
        xpos = self.x-self.xn*6
        ypos = self.y-self.yn*6
        terrain.pastesurfID(self.pix,xpos,ypos, myangle, 1.0)

class dirtcluster(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self)
        self.owner = owner
        self.x = float(xp)
        self.y = float(yp)
        self.image = display.loadtex("dirtclod.png")
        self.destalpha = 55
        self.radius = 55

    def hitPlayer(self,p):
        self.finalHitLand()
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
        for i in range(0,4):
            self.launchcluster()
    def launchcluster(self):
        newbullet = dirtclod(self.x,self.y,self.owner)
        newbullet.xvel=random.random()*16-8
        newbullet.yvel=random.random()*16-8
        self.owner.bullets.append(newbullet)

class gravbullet(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self)
        self.owner = owner
        self.x = float(xp)
        self.y = float(yp)
        self.image = display.loadtex("smoke.png")
        self.destalpha = 15
        self.radius = 25

    def hitPlayer(self,p):
        self.dead = 1
        self.explode(self.radius)
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
    def movDone(self, x1, y1, x2, y2):
      for i in self.owner.gamestate.clients:
        xd = i.x-self.x
        yd = i.y-self.y
        td = xd*xd+yd*yd
        if td < 125*125:
          i.xvel+=xd*0.05
          i.yvel+=yd*0.05
class grenade(basebomb):
    image = display.loadtex("grenade.png")
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp,"grenade.png")
        self.destalpha = 35
        self.radius = 50
        self.maxbounces = 29
        self.bouncing = 1
        self.totalmoves=50
        self.scale = 0.7
    #def hitPlayer(self,p):
    #   self.dead = 1
    #   self.explode(self.radius)
    #def finalHitLand(self):
    #   self.dead = 1
    #   self.explode(self.radius)
    #def hitLand(self):
    #   self.explode(10)
    def timeUp(self):
        self.explode(50)
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/10, int((self.radius-5)*0.15+1))
        particles.addParticle(self.x, self.y, 0.5, "fire.png", self.radius/10, int((self.radius-5)*0.05+1))
	
class nukelet(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self)
        self.owner = owner
        self.x = float(xp)
        self.y = float(yp)
        self.image = display.loadtex("nukelet.png")
        self.destalpha = 15
        self.radius = 25
        self.scale = 1
        self.bouncing = 1
        self.maxbounces = 500
        self.totalmoves=75
    
    def movDone(self,x1,y1,x2,y2):
        particles.addParticle(self.x, self.y, 0.5, "circle.png", 1.5, 1,[0,0.4,0])

    def hitPlayer(self,p):
        self.dead = 1
        self.explode(self.radius)
    
    def timeUp(self):
        self.explode(self.radius)
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/5,2,[0,0.1,0])
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/10,1,[0,0.5,0])


class fireball(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self)
        self.owner = owner
        self.x = float(xp)
        self.y = float(yp)
        self.image = display.loadtex("fire.png")
        self.destalpha = 15
        self.radius = 25
        self.scale = 1
        self.bouncing = 1
        self.maxbounces = 500
        self.totalmoves=75
    
    def movDone(self,x1,y1,x2,y2):
        particles.addParticle(self.x, self.y, 0.5, "fire.png", 2.5, 1,[1,1,1])

    def hitPlayer(self,p):
        self.dead = 1
        self.explode(self.radius)
    
    def timeUp(self):
        self.explode(self.radius)
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/5,2,[1,1,1])
        particles.addParticle(self.x, self.y, 0.5, "fire.png", self.radius/10,1,[1,1,1])
        
class nuke(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self)
        self.owner = owner
        self.x = float(xp)
        self.y = float(yp)
        self.image = display.loadtex("shellBFG.png")
        self.destalpha = 15
        self.radius = 150
        self.scale = 2.5
	
    def movDone(self,x1,y1,x2,y2):
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", 3, 2,[0,0,0])
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", 2.5, 2,[0,0.5,0])
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", 2, 1,[0,1,0])

    def hitPlayer(self,p):
	self.finalHitLand()

    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/10,5,[0,0.1,0])
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/20,3,[0,0.7,0])
        particles.addParticle(self.x, self.y, 0.5, "smoke.png", self.radius/25,1,[0,1,0])
        
	for i in range(0,10):
            self.launchcluster()
    def launchcluster(self):
        newbullet = nukelet(self.x,self.y,self.owner)
        newbullet.xvel=random.random()*16-8
        newbullet.yvel=random.random()*16-8
        self.owner.bullets.append(newbullet)
	
	

class ripper(basebomb):
    def __init__(self, xp,yp,owner):
        basebomb.__init__(self,owner,xp,yp)
        self.image = display.loadtex("drillgrenade.png")
        self.destalpha = 35
        self.radius = 50
        self.maxbounces = 9

    def hitPlayer(self,p):
        self.dead = 1
        self.explode(self.radius)
    def finalHitLand(self):
        self.dead = 1
        self.explode(self.radius)
    def hitLand(self):
        self.explode(10)
        
