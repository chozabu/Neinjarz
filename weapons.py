#import pygame

import terrain
import display

from math import hypot


import OpenGL.GL as GL
from multilauncher import multilauncher
import projectiles
import random
import particles

class bazooka(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.shell,"bazooka.png")
        self.scale=1.4
    def shootcheck(self):
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "smoke.png", 3, 3)
class sword(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.shell,"sword.png")
        self.scale=1.4
    def shootabullet(self):
        xv = self.owner.gmx-self.owner.cx
        yv = self.owner.gmy-self.owner.cy
        self.length = hypot(xv,yv)
        if self.length == 0:self.length = 0.001
        xvn=xv/self.length
        yvn=yv/self.length
        poix = self.owner.cx+xvn*26
        poiy = self.owner.cy+yvn*26
        terrain.explode(poix,poiy,30,10)
        for c in self.owner.gamestate.clients:
            if c is self.owner: continue
            xd = c.cx - poix
            yd = c.cy - poiy
            td = xd * xd + yd * yd
            if td < 29*29:
                c.xvel+=xvn*20
                c.yvel+=yvn*20
                c.damage(30, self.owner)
        self.timetofire = self.firedelay
        particles.addParticle(poix, poiy, 0.5, "sword2.png", 3, 1)
    #def shootcheck(self):
    #    particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "smoke.png", 3, 3)
class uzi(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.bullet,"uzi.png")
        self.firedelay = 2
    def shootcheck(self):
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "emptyshell.png", 1.3, 1)
    def ammocheck(self, ammo):
        ammo.setVelocity(35)
        ammo.xvel+=random.random()-0.5
        ammo.yvel+=random.random()-0.5
class chaingun(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.chainbullet,"apple.png")
        self.firedelay = 0
    def shootcheck(self):
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "emptyshell.png", 1.3, 1)
    def ammocheck(self, ammo):
        ammo.setVelocity(35)
        ammo.xvel+=random.random()*10-5.0
        ammo.yvel+=random.random()*10-5.0
class shotgun(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.bulletshotgun,"shotgun.png")
        self.scale=1.6
        self.firedelay = 20
    def shootcheck(self):
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "smoke.png", 1, 2)
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "emptyshell2.png", 1.3, 2)
        for i in range(11):
          self.shootabullet()
    def ammocheck(self, ammo):
        ammo.setVelocity(35)
        ammo.xvel+=random.randrange(-3,3)
        ammo.yvel+=random.randrange(-3,3)
class redeemer(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.nuke,"BFG.png")
        self.scale=3.5
        self.firedelay = 120
    def shootcheck(self):
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "fire.png", 4, 5)
class gravgun(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.gravbullet,"smoke.png")
        self.firedelay = 25
class bow(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.arrow,"bow.png")
        self.scale=1.4
        self.firedelay = 5
class hominbow(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.hominarrow,"knife.png")
        self.firedelay = 5
        self.posmult = -0.04
class guidedbow(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.guidedknife,"grapple.png")
        self.firedelay = 5
        self.posmult = -0.04
class bridgegun(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.bridger,"bridger.png")
        self.scale=1.4
        self.firedelay = 50
    def ammocheck(self, ammo):
        ammo.setVelocity(12)
        ammo.y+=18
class dirtthrower(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.dirtcluster,"dirtclod.png")
        self.firedelay = 30
class dirtsprayer(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.dirtclod,"dirtsprayer.png")
        self.firedelay = 3
    def shootcheck(self):
        particles.addParticle(self.owner.cx, self.owner.cy, 0.5, "dirtclod.png", 2, 2)
    def ammocheck(self, ammo):
        ammo.xvel+=random.randrange(-3,3)
        ammo.yvel+=random.randrange(-3,3)
class digger(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.ripper,"drillgrenade.png")
        self.firedelay = 25
class grenadelauncher(multilauncher):
    def __init__(self, owner):
        multilauncher.__init__(self,owner,projectiles.grenade,"glauncher.png")
        self.firedelay = 11
