"""menu.py: Handles the User Interface."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

import pygame
import pygame.locals as pgl
import sys
from random import random


import display, simplenet, terrain, timer


class Menu():
    def runMenu(self):
        inmenu = 1
        while inmenu:
            self.drawMenu()
            #time.sleep(1.0/60.0)
            timer.tick()
            for event in pygame.event.get():
                if event.type == 2:#keypress
                    if event.key == pgl.K_ESCAPE:
                        sys.exit()
                    if event.key == pgl.K_r:
                        terrain.loadimg("clev")
                    if event.key == pgl.K_w:
                        simplenet.isServer = 0
                        simplenet.isClient = 0
                        inmenu = 0
                    if event.key == pgl.K_s:
                        simplenet.isServer = 1
                        simplenet.isClient = 0
                        inmenu = 0
                        simplenet.initNet()
                    if event.key == pgl.K_c:
                        simplenet.isServer = 0
                        simplenet.isClient = 1
                        inmenu = 0
                        self.name = "nameless"+str(random()*1000)[0:3]
                        simplenet.sendserv("join", self.name)
                elif event.type == pgl.VIDEORESIZE:
                    print(event.dict['size'])
                    display.resize(event.dict['size'][0], event.dict['size'][1])
                    pygame.display.flip()
    def drawMenu(self):
        display.clear()
        displayratio = display.sh*0.01
        tx = -20*displayratio
        display.drawWord(pos=[tx,0*displayratio,0], string="press W to do single player", color=[1,1,1],size=displayratio*20)
        display.drawWord(pos=[tx,5*displayratio,0], string="press S to Host a game", color=[1,1,1],size=displayratio*20)
        display.drawWord(pos=[tx,10*displayratio,0], string="press C to Join a game", color=[1,1,1],size=displayratio*20)
        display.drawWord(pos=[tx,15*displayratio,0], string="press R to Reset Level", color=[1,1,1],size=displayratio*20)
        #display.applycam()
        #terrain.draw(display.camx,display.camy)
        #for b in self.walkers:
        #    b.draw()
        #if not simplenet.isServer:
        #    particles.draw()
        pygame.display.flip()
