
import terrain
import display
import timer
import rope

import weapons

from math import hypot, atan2, sqrt

import OpenGL.GL as GL
from random import random

#import simplenet
import particles

class playerclass:
    def reset(self):
        self.health = 100.0
        self.x = 20.0+random()*(terrain.x2-40.0)
        self.y = 1.0+random()*terrain.y2-(terrain.y2*0.5)
        self.yvel = -3
        self.xvel = 0
        self.resetcount = 0
    def die(self):
        self.altunshoot()
        self.resetcount = 30
    def __init__(self, gamestate, name, netdata):
        self.isbot = 0
        self.healthscale = 1
        self.kills = 0
        self.damagedealt = 0
        self.msinx = 300
        self.msiny = 300
        self.camx = 1
        self.camy = 1
        self.gmx = 0
        self.gmy = 0
        self.reset()
        self.gamestate = gamestate
        self.name = name
        self.netdata = netdata
        self.landcolour=[1,1,1]
        self.cx = self.x
        self.cy = self.y+8.0
        self.image = display.loadtex("minimar.png")
        self.runs = [display.loadtex("run1.png"), display.loadtex("run2.png"), display.loadtex("run3.png"), display.loadtex("run4.png"), display.loadtex("run5.png")]
        self.runanim = 0
        self.jumps = [display.loadtex("jump1.png"), display.loadtex("jump2.png")]
        #self.pix = display.loadpix("minimar.png")
        self.bullets = []
        self.onground = 0
        self.wasonground = 0
        self.guns = []
        #self.guns.append(rope.rope(self))
        self.guns.append(weapons.chaingun(self))
        self.guns.append(weapons.sword(self))
        self.guns.append(weapons.shotgun(self))
        self.guns.append(weapons.bazooka(self))
        self.guns.append(weapons.uzi(self))
        self.guns.append(weapons.redeemer(self))
        self.guns.append(weapons.gravgun(self))
        self.guns.append(weapons.bow(self))
        self.guns.append(weapons.bridgegun(self))
        self.guns.append(weapons.dirtthrower(self))
        self.guns.append(weapons.dirtsprayer(self))
        self.guns.append(weapons.digger(self))
        self.guns.append(weapons.grenadelauncher(self))
        self.guns.append(weapons.hominbow(self))
        self.guns.append(weapons.guidedbow(self))
        self.gunid = 0
        self.gun = self.guns[self.gunid]
        self.altgun = rope.rope(self)
        #self.jumpsound = pygame.mixer.Sound('ouh.ogg')

        self.upkey = 0
        self.dnkey = 0
        self.ltkey = 0
        self.rtkey = 0
        self.jumpkey = 0
        self.digkey = 0
        self.crouchkey = 0
        self.shootkey = 0
        self.grapplekey = 0

        #these were dodge
        self.xvel = 0
        self.yvel = 0
        self.vel = 0
        self.movesleft = 0
        self.xn = 0
        self.yn = 0
        self.mx = 0
        self.my = 0
        self.tnx = 0
        self.tny = -1
        self.dnx = 0
        self.dny = -1
        self.lastdig = 0
        self.aimgle = 0
        #self.onground = 0
        self.canjump = 1
        self.jumpwait = 0
        #end of dodgyness
    def bang(self, x, y, radius, setto,cause):
        xd = x-self.x
        yd = y-self.y
        td = xd*xd+yd*yd
        r2 = (radius*radius)
        if td < r2:
            td=sqrt(td)
            diffd = sqrt(radius-td)
            xd/=td
            yd/=td
            self.xvel-=(xd*diffd)*3
            self.yvel-=(yd*diffd)*3
            self.damage(diffd*4,cause)
    def damage(self, amount,cause):
        if self.health < 0:
          return
        self.health-=amount
        cause.damagedealt+=amount
        if cause == self:self.damagedealt-=amount*2
        particles.addTextParticle(self.x, self.y, 0.05, "-" + str(int(amount)), 130+amount,[1,0,0])
        if self.health<0:
            cause.kills+=1
            particles.addParticle(self.x, self.y, 0.4, "blood.png", 3.9, 15)
            self.die()
            if cause == self:
              self.kills-=2
            particles.addTextParticle(cause.x, cause.y, 0.05, str(cause.kills), 300,[1,1,0])
            #print self.name, self.kills, self.damagedealt
            print(self.name, "has", self.kills, " kills and has caused ", self.damagedealt, "damage")
            print(cause.name, "has", cause.kills, " kills and has caused ", cause.damagedealt, "damage")
            print(cause.name, "killed", self.name)
        #print("")


    #def packnet(self):
    #    return [self.name, self.netdata, self.x, self.y, self.dnx, self.dny, self.xvel, self.yvel, self.onground, self.wasonground, self.runanim]

    def changegun(self, dist):
        self.unshoot()
        self.gunid=(self.gunid+dist)%len(self.guns)
        self.gun = self.guns[self.gunid]
        #print self.gunid
    def fixpos(self, xm=0, ym=0):
        'called when the player is inside some land while moving'
        #self.x-=self.xn
        #self.y-=self.yn
        tn = terrain.getnormal(int(self.x)+xm, int(self.y)+ym)
        self.landcolour = terrain.getcolour(self.x,self.y)
        self.tnx = tn[0]
        self.tny = tn[1]
        impx = tn[0]*self.xvel
        impy = tn[1]*self.yvel
        impd = impx*impx+impy*impy
        if impd>(23*23):
          #print impd/100
          brad = int(impd/100)
          if brad > 30: brad = 30
          terrain.explode(self.x,self.y,brad)
          self.damage(impd/100,self)
          particles.addParticle(self.x, self.y, 0.4, "blood.png", 1.5, 3)
        #print self.tnx,self.tny
        if self.tny < 0.1:
            self.onground = 1
            self.canjump = 1

        self.x += self.tnx/2
        self.y += self.tny/2

        dp = self.xn*(-self.tny)+self.yn*self.tnx
        self.xn = -self.tny*dp
        self.yn = self.tnx*dp
        #else:
        self.xvel = self.xn*self.vel
        self.yvel = self.yn*self.vel
        if self.crouchkey == 1:
            self.xvel += -self.tnx#*self.vel wtf? FIXME whossis do
            self.yvel += -self.tny#*self.vel
        if self.digkey and self.lastdig+20 < timer.totaltime:
            terrain.explode(int(self.x), int(self.y), 30, 20)
            self.dugg = 1
            self.lastdig = timer.totaltime

        #terrain.explode(int(self.x), int(self.y), 4, 128)
    def reaim(self):
        self.camx, self.camy=display.camlimit((self.x+self.gmx)/2, (self.y+self.gmy)/2)
        self.gmx = self.camx + self.msinx-display.sw/2
        self.gmy = self.camy + self.msiny-display.sh/2
        self.mx = self.gmx-self.x
        self.my = self.gmy-self.y
    def getnearplayer(self):
        neard = 1000000
        nearp = self
        for other in self.gamestate.clients:
            xd = self.x-other.x
            yd = self.y-other.y
            td = xd*xd+yd*yd
            if td < neard and other != self:
                neard = td
                nearp = other
        return nearp
    def beabot(self):
        if random()>0.97 and self.isbot:
            self.msinx = random()*display.sw
            self.msiny = random()*display.sh
            targetp = self.getnearplayer()
            self.msinx = (targetp.x- self.x)+display.sw/2
            self.msiny = (targetp.y-self.y)+display.sh/2
            self.shoot()
        if random()>0.997 and self.isbot:
            self.unshoot()
        if random()>0.99 and self.isbot:
          self.changegun(int(random()*5))
        if self.y > terrain.y2 and random()>0.9:
            self.altshoot()
    def update(self):
        self.updatebullets()
        if self.resetcount > 0:
          if self.resetcount == 1:
            self.reset()
          self.resetcount-=1
          return
        self.yvel+=0.4#grav
        if self.vel > 5 and self.onground:
          particles.addParticle(self.x, self.y, 0.3, "smoke.png", 0.8, 2,self.landcolour)
        self.reaim()
        if self.isbot:
          self.beabot()
        self.wasonground = self.onground
        self.gun.update()
        self.altgun.update()
        if terrain.getalpha(int(self.x), int(self.y)) > 128:
            terrain.explode(int(self.x), int(self.y)-19, 20)



        #input
        self.dugg = 0
        self.jumpwait -= 1
        if self.jumpkey and self.canjump and self.jumpwait<0:
            particles.addParticle(self.x, self.y, 1, "smoke.png", 1.5, 3)
            self.canjump = self.onground
            self.jumpwait=5
            self.yvel-=3
            self.yvel+=self.tny*3
            self.xvel+=self.tnx*3
            #self.jumpsound.play()
        #if self.crouchkey == 1 and self.onground == 1:
        #    pass
        #else:
        '''if self.crouchkey == 0 or self.onground == 0:
            self.yvel+=0.225
            if self.onground == 0:
                self.yvel+=0.125
        '''
        movmult = 0.8-self.crouchkey*0.08
        if self.upkey:self.yvel-=0.12
        if self.dnkey:self.yvel+=0.4
        if self.ltkey:
            self.xvel-=movmult
            #self.yvel-=self.tnx*movmult
            #self.xvel+=self.tny*movmult
        if self.rtkey:
            self.xvel+=movmult
            #self.yvel+=self.tnx*movmult
            #self.xvel-=self.tny*movmult

        #figure some rotation
        #if self.tny> 0.5:self.tnx = 0.5
        self.dnx = self.dnx*0.9+self.tnx*0.1
        self.dny = self.dny*0.9+self.tny*0.1
        mag = hypot(self.dnx, self.dny)
        self.dnx/=mag
        self.dny/=mag


        self.tnx *=0.8
        self.tny = self.tny*0.8-0.2
        mag = hypot(self.tnx, self.tny)
        self.tnx/=mag
        self.tny/=mag
        turntime = timer.turntime
        #print turntime
        #self.xvel*=timer.turntime
        #self.yvel*=timer.turntime
        #phys
        self.yvel*=0.99#*timer.turntime
        self.xvel*=0.99#*timer.turntime
        self.vel = hypot(self.xvel, self.yvel)
        if self.vel < 1:
            self.xn = self.xvel
            self.yn = self.yvel
            self.movesleft = 1
        else:
            self.xn = self.xvel/self.vel
            self.yn = self.yvel/self.vel
            self.movesleft = self.vel
        self.onground = 0
        maxcol = 10
        while self.movesleft > 0 and maxcol > 0:
            self.x+=self.xn
            self.y+=self.yn
            self.checkbounds()
            self.movesleft-=1
            if terrain.getalpha(int(self.x), int(self.y)) > 128:
                self.fixpos()
                self.movesleft+=1
                maxcol-=1
            '''elif terrain.getalpha(int(self.x+3), int(self.y)) > 128:
                self.fixpos(3, 0)
                self.movesleft+=1
                maxcol-=1
            elif terrain.getalpha(int(self.x-3), int(self.y)) > 128:
                self.fixpos(-3, 0)
                self.movesleft+=1
                maxcol-=1
            elif terrain.getalpha(int(self.x), int(self.y-3)) > 128:
                self.fixpos(0, -3)
                self.movesleft+=1
                maxcol-=1
            elif terrain.getalpha(int(self.x), int(self.y-6)) > 128:
                self.fixpos(0, -6)
                self.movesleft+=1
                maxcol-=1'''

        self.cx = self.x+self.dnx*16
        self.cy = self.y+self.dny*16
        self.angle = -atan2(self.dnx, self.dny)/3.141573*180
        self.aimgle = -atan2(self.mx, self.my)/3.141573*180
    def updatebullets(self):
        for b in self.bullets:
            b.move()
        for b in self.bullets:
            if b.dead:
                self.bullets.remove(b)
        #return 0

    def movev(self, vx, vy):
        vel = hypot(vx, vy)+0.000000001
        #if vel < 1:
        #    xn = vx
        #    yn = vy
        #    movesleft = 1
        #else:
        xn = vx/vel
        yn = vy/vel
        movesleft = int(vel)
        #self.onground = 0
        maxcol = 10
        while movesleft > 0 and maxcol > 0:
            self.x+=xn
            self.y+=yn
            self.checkbounds()
            movesleft-=1
            if terrain.getalpha(int(self.x), int(self.y)) > 128:
                self.fixpos()

                xn = self.xn
                yn = self.yn
                movesleft+=1
                maxcol-=1
    def shoot(self):
        self.gun.shoot(self.x+self.mx, self.y+self.my)
    def unshoot(self):
        self.gun.unshoot()
    def altshoot(self):
        self.altgun.shoot(self.x+self.mx, self.y+self.my)
    def altunshoot(self):
        self.altgun.unshoot()
    def checkbounds(self):
        if self.y > terrain.y2*3:
          pass
          self.damage(self.health+1,self)
        if self.x>terrain.x2-10:
            pass
            #self.x=terrain.x2-10
            #self.x-=terrain.x2-20
            #self.altgun.on = 0
            #self.onground = 1
            #self.xvel = 0
            #self.canjump = 1
        if self.y>terrain.y2-10:
            pass
            #self.y-=terrain.y2-20
            #self.altgun.on = 0
            #self.yvel*=1.01
            #self.y=terrain.y2-10
            #self.onground = 1
            #self.canjump = 1
            #self.yvel = 0
        if self.x<10:
            pass
            #self.x+=terrain.x2-20
            #self.altgun.on = 0
            #self.x=10
            #self.onground = 1
            #self.xvel = 0
            #self.canjump = 1
        if self.y<10:
            pass
            #self.y+=terrain.y2-20
            #self.altgun.on = 0
            #self.y=10
            #self.yvel = 0

    def drawradar(self):
        GL.glLineWidth(2)
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glColor4f(0.1, 0.95, 0.05, 0.3)
        for i in self.gamestate.clients:
          if i != self:
            xd = (self.x-i.x)*0.003
            yd = (self.y-i.y)*0.003
            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(0,0, 0.0)
            GL.glVertex3f(-xd,-yd, 0.0)
            GL.glEnd()
        GL.glEnable(GL.GL_TEXTURE_2D)

    def draw(self):
        for b in self.bullets:
            b.draw()
        if self.health < 0:
          return
        GL.glPushMatrix()

        angle = -atan2(self.dnx, self.dny)/3.141573*180
        if self.mx <0:
            xscale = -1
        else:
            xscale = 1
        GL.glTranslatef(self.x+xscale*2, self.y, 0.0)
        GL.glScalef(16, 16, 16)
        #self.drawradar()
        self.healthscale = self.health/200+0.5
        GL.glScalef(self.healthscale, self.healthscale, 1)
        GL.glRotatef(angle, 0, 0, 1)
        GL.glScalef(xscale, 1, 1)
        xs2=1
        if self.xvel>0:xs2=-1
        if self.onground or self.wasonground or self.yvel>5:
            self.runanim+=self.vel*0.05*-xscale*xs2
            self.runanim = self.runanim%len(self.runs)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.runs[int(self.runanim)])#int(random()*3)])
        else:
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.jumps[self.yvel>0])
        #GL.glBindTexture(GL.GL_TEXTURE_2D, self.image)
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0.0, 1.0)
        GL.glVertex3f(1.0, 2.0, 0.0)

        GL.glTexCoord2f(1.0, 1.0)
        GL.glVertex3f(-1.0, 2.0, 0.0)

        GL.glTexCoord2f(1.0, 0.0)
        GL.glVertex3f(-1.0, 0.0, 0.0)

        GL.glTexCoord2f(0.0, 0.0)
        GL.glVertex3f(1.0, 0.0, 0.0)
        GL.glEnd()
        GL.glPopMatrix()
        self.altgun.draw()
        self.gun.draw()
        display.drawWord(pos=[self.x-len(self.name)*4,self.y-35,0], string=self.name, color=[0,1,255], size=100)
