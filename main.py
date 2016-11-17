#!/usr/bin/env python

#try:
#     import psyco
#     psyco.full()
# except ImportError:
#     print("Get psyco!")

#import os
from random import random
#try:
import pygame, sys
#import Numeric as N
#from pygame.locals import *
import pygame.locals as pgl
surfarray = pygame.surfarray
#if not surfarray:raise ImportError
#except ImportError:
#    raise ImportError, 'need pygame and numeric'

import settings

from math import hypot


pygame.init()

import display
display.loadtex("nothing.png")
import terrain
#import walker, ball, player #walker is like a lemming, and ball a simpler player
import player
import timer, time

import simplenet
import particles
import menu

#from cPickle import *
#import zlib
#from zlib import *
import OpenGL.GL as GL
pygame.display.set_caption("NeinJarz")

#i cant pickle events?
class netevent:
    def __init__(self):
        pass
#    pos = None
    pass


def bind(a, b, dist, stren=0.1):
    xd = a.x-b.x
    yd = a.y-b.y
    td = hypot(xd, yd)
    diffd = (dist-td)*stren
    xd /=td
    yd /=td
    a.xvel +=xd*diffd
    a.yvel +=yd*diffd
    b.xvel -=xd*diffd
    b.yvel -=yd*diffd

class gameStateClass:
    def __init__(self):
        self.walkers = []
        self.clients = self. walkers
        terrain.walkers = self.walkers #fixme i dont think i need or want this line
        #but should improve the gamestate class, give it some funcs
        #oh, and fix the freaking networking so its good!
        self.walkers.append(player.playerclass(self, "The server", None))


class njgame:
    def __init__(self):
        terrain.loadimg("testlevel")
        #terrain.loadimg("clev")
        self.name = "damnidontcare"
        display.init()
        self.gamestate = gameStateClass()
        self.walkers = self.gamestate.walkers
        self.clients = self. walkers
        simplenet.clients = self.clients
        terrain.walkers = self.walkers
        display.lookat(0, 0)
        self.mx = 100
        self.my = 100
        self.mywalker = self.walkers[0]
        self.menu = menu.Menu()
        #terrain.explode(10,10,1000,0)

    def findclient(self, netdata):
        for c in self.clients:
            if c.netdata == None: continue
            found = False
            if netdata[0] == c.netdata[0] and netdata[1] == c.netdata[1]:
                found = True
            if found == True:
                #print c
                return c
    def addClient(self, cname, netdata):
        for c in self.clients:
            if c.netdata == None: continue
            if c.netdata[0] == netdata[0]:
                return None
        newplayer = player.playerclass(self.gamestate, cname, netdata)
        print( (cname, netdata), "joined")
        self.clients.append(newplayer)
        return newplayer
    def doNet(self):
        #if isServer:
        #	checktimeouts()
        while simplenet.checkdata():
            packet, peer = simplenet.nextpacket()
            if packet is None: break
            pType = packet[0]
            pData = packet[1]
            #print pType, pData
            if simplenet.isServer:
                cl = self.findclient(peer)
                if cl != None: cl.lastpackettime = 0
                if pType=="join":
                    cl = self.addClient(pData, peer)
                    if cl is None:
                        simplenet.sendto("joinfailed", "alreadyjoined?", peer)
                    else:
                        simplenet.sendto("yourein", "dosomethingcool", peer)
                elif cl is None:
                    simplenet.sendto("whoyou", "i didnt get join message", peer)
                elif pType == "event":
                    self.handleEvent(pData, cl)
            else:#client
                if pType=="gamestate":
                    self.gamestate = pData
                    self.clients = self.gamestate.clients
                    self.walkers = self.clients
                    for w in range(len(self.walkers)):
                        if self.walkers[w].name == self.name:
                            self.mywalker = self.walkers[w]
                elif pType=="boom":
                    terrain.explode(pData[0], pData[1], pData[2], pData[3])
                elif pType=="pastetex":
                    terrain.pastesurfID(pData[0], pData[1], pData[2], pData[3], pData[4])
                elif pType=="addtps":
                    particles.addTextParticle(pData[0], pData[1], pData[2], pData[3], pData[4], pData[5])
                elif pType=="addps":
                    particles.addParticle(pData[0], pData[1], pData[2], pData[3], pData[4], pData[5], pData[6])
                    #print pData
                elif pType=="msg":
                    #addmsg(pData[0], pData[1])
                    print(pData)
                elif pType=="whoyou":
                    simplenet.sendserv("join", self.name)
                elif pType=="wakeup":
                    simplenet.sendserv("keepalive", "dude")


    def run(self):
        #self.runMenu()
        #self.initNet()
        while 1:
            timer.tick()
            self.doNet()
            for event in pygame.event.get():
                self.handleEvent(event, self.mywalker)
            if not simplenet.isClient:
                self.mainloop()
            particles.update()
            if simplenet.isServer:
                self.drawstuff()
                simplenet.sendall("gamestate", self.gamestate)
            else:
                #particles.update()
                self.drawstuff()
                #self.mainloop()

    def handleEvent(self, event, cplayer):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pgl.VIDEORESIZE:
            print(event.dict['size'])
            display.resize(event.dict['size'][0], event.dict['size'][1])
            pygame.display.flip()
        elif simplenet.isClient:
            ne = netevent()
            ne.type = event.type
            if event.type == 2 or event.type == 3:
                if event.key == pgl.K_ESCAPE:
                    sys.exit()
                ne.key = event.key
                simplenet.sendserv("event", ne)
            elif event.type == pgl.MOUSEMOTION:
                ne.pos = [event.pos[0], event.pos[1]]
                simplenet.sendserv("event", ne)
            elif event.type == pgl.MOUSEBUTTONDOWN:
                ne.button = event.button
                ne.pos = [event.pos[0], event.pos[1]]
                simplenet.sendserv("event", ne)
            elif event.type == pgl.MOUSEBUTTONUP:
                ne.button = event.button
                ne.pos = [event.pos[0], event.pos[1]]
                simplenet.sendserv("event", ne)
            return
        if event.type == 2:#keypress
            if event.key == pgl.K_DELETE:
                if len(self.walkers) > 0:self.walkers.remove(self.walkers[0])
            if event.key == pgl.K_w:
                #for i in range(0, len(self.walkers)):self.walkers[i].upkey = 1
                cplayer.upkey = 1
            if event.key == pgl.K_ESCAPE:
                sys.exit()
            if event.key == pgl.K_m:
                self.menu.runMenu()
            if event.key == pgl.K_s:
                cplayer.dnkey = 1
            if event.key == pgl.K_a:
                cplayer.ltkey = 1
            if event.key == pgl.K_d:
                cplayer.rtkey = 1
            if event.key == pgl.K_SPACE:
                cplayer.jumpkey = 1
            if event.key == pgl.K_LCTRL:
                cplayer.crouchkey = 1
            if event.key == pgl.K_v:
                cplayer.digkey = 1
            if event.key == pgl.K_q:
                cplayer.changegun(1)
            if event.key == pgl.K_e:
                cplayer.changegun(-1)
        if event.type == 3:#keyrelease
            if event.key == pgl.K_n:
                newplayer = player.playerclass(self.gamestate, "A Bot " + str(len(self.gamestate.clients)), None)
                newplayer.isbot = 1#int(random()*2)
                newplayer.jumpkey = int(random()*2)
                newplayer.x = cplayer.gmx
                newplayer.y = cplayer.gmy
                self.walkers.append(newplayer)
            if event.key == pgl.K_w:
                cplayer.upkey = 0
            if event.key == pgl.K_s:
                cplayer.dnkey = 0
            if event.key == pgl.K_a:
                cplayer.ltkey = 0
            if event.key == pgl.K_d:
                cplayer.rtkey = 0
            if event.key == pgl.K_SPACE:
                cplayer.jumpkey = 0
            if event.key == pgl.K_LCTRL:
                cplayer.crouchkey = 0
            if event.key == pgl.K_v:
                cplayer.digkey = 0
        if event.type == pgl.MOUSEMOTION or event.type == pgl.MOUSEBUTTONUP or event.type == pgl.MOUSEBUTTONDOWN:
            cplayer.msinx = event.pos[0]
            cplayer.msiny = event.pos[1]
        #print event.type
        if event.type == pgl.MOUSEBUTTONUP:
            if event.button == 1:
                cplayer.unshoot()#jumpkey = 1
            if event.button == 3:
                cplayer.altunshoot()#jumpkey = 1
        if event.type == pgl.MOUSEBUTTONDOWN:
            #print event.button
            if event.button == 4:
                cplayer.changegun(1)
            if event.button == 5:
                cplayer.changegun(-1)
            if event.button == 3:
                cplayer.altshoot()
                #terrain.explode(cplayer.gmx, cplayer.gmy, 90, 255)
            if event.button == 1:
                cplayer.shoot()#jumpkey = 1
                #self.walkers.append(player.playerclass(mx, my))
                #self.ownid = len(self.walkers)-1
            #if event.button == 2:
            #	display.lookat(self.mx, self.my)

    def mainloop(self):
        #bind(self.walkers[4], self.walkers[5], 50)
        for b in self.walkers:
            b.update()
            if b.kills > 9:
              terrain.loadimg("clev")
              b.kills = 0
        remlist = []
        for i in range(0, len(self.walkers)-1):
            for r in range(i+1, len(self.walkers)):#FIXME
                dist = 25
                a=self.walkers[i]
                b=self.walkers[r]
                xd = a.x-b.x
                yd = a.y-b.y
                td = hypot(xd, yd)#+0.000000001
                if (0<td< dist):
                    diffd = (dist-td)*0.49
                    xd /=td
                    yd /=td
                    a.xvel +=xd*diffd
                    a.yvel +=yd*diffd
                    b.xvel -=xd*diffd
                    b.yvel -=yd*diffd
                    a.movev(xd *diffd, yd *diffd)
                    b.movev(-xd *diffd, -yd *diffd)
                    if a.y < b.y:
                      a.canjump = 1
                    else:
                      b.canjump = 1
                    #particles.addParticle(a.x, b.y, 5, 3, "smoke.png")
                    #a.x+=xd*diffd
                    #a.y+=yd*diffd
                    #b.x-=xd*diffd
                    #b.y-=yd*diffd
        for i in remlist:
            self.walkers.remove(i)
        #particles.update()

    def drawradar(self):
        GL.glLineWidth(2)
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glColor4f(0.1, 0.95, 0.05, 0.3)
        for i in self.clients:
          if i != self.mywalker:
            xd = (self.mywalker.x-i.x)*0.03
            yd = (self.mywalker.y-i.y)*0.03
            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(self.mywalker.x,self.mywalker.y, 0.0)
            GL.glVertex3f(self.mywalker.x-xd,self.mywalker.y-yd, 0.0)
            GL.glEnd()
        GL.glEnable(GL.GL_TEXTURE_2D)
    def drawstuff(self):
        if self.mywalker!=None:
            display.lookat((self.mywalker.x+self.mywalker.gmx)/2, (self.mywalker.y+self.mywalker.gmy)/2)
            self.drawradar()
        display.clear()
        display.applycam()
        terrain.draw(display.camx,display.camy)
        for b in self.walkers:
            b.draw()
        particles.draw()
        self.menu.drawLog()
        pygame.display.flip()

def startup():
    game = njgame()
    game.run()
if __name__ == '__main__':
    startup()
