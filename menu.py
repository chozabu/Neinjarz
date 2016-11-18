"""menu.py: Handles the User Interface."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

import pygame
import pygame.locals as pgl
import sys
from random import random


import display, simplenet, terrain, timer

log = []


def addLogText(*items):
    text = ""
    for i in items:
        text += str(i) + " "
    global log
    log.append(text)
    if len(log) > 10:
        log = log[1:]

class MainMenu():
    def handleEvent(self, event):
        if event.type == 2:#keypress
            if event.key == pgl.K_r:
                terrain.loadimg("clev")
            if event.key == pgl.K_w:
                simplenet.isServer = 0
                simplenet.isClient = 0
                return True
            if event.key == pgl.K_s:
                simplenet.isServer = 1
                simplenet.isClient = 0
                simplenet.initNet()
                return True
            if event.key == pgl.K_c:
                simplenet.isServer = 0
                simplenet.isClient = 1
                self.name = "nameless"+str(random()*1000)[0:3]
                simplenet.sendserv("join", self.name)
                return True
    def draw(self):
        displayratio = display.sh*0.01
        tx = -20*displayratio
        display.drawWord(pos=[-display.sw2+20,-display.sh2+200,0*displayratio], string="NeinJarz", color=[1,1,1],size=displayratio*40)
        display.drawWord(pos=[tx,0*displayratio,0], string="press W to do single player", color=[1,1,1],size=displayratio*20)
        display.drawWord(pos=[tx,5*displayratio,0], string="press S to Host a game", color=[1,1,1],size=displayratio*20)
        display.drawWord(pos=[tx,10*displayratio,0], string="press C to Join a game", color=[1,1,1],size=displayratio*20)
        display.drawWord(pos=[tx,15*displayratio,0], string="press R to Reset Level", color=[1,1,1],size=displayratio*20)

class Menu():
    def __init__(self):
        self.clearLog()
        self.mainMenu = MainMenu()
        self.currentMenu = self.mainMenu
    def clearLog(self):
        global log
        log = ["This is the log", "press m for the menu"]
    def runMenu(self):
        inmenu = 1
        while inmenu:
            self.drawMenu()
            #time.sleep(1.0/60.0)
            timer.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == 2:#keypress
                    if event.key == pgl.K_ESCAPE:
                        sys.exit()
                elif event.type == pgl.VIDEORESIZE:
                    print(event.dict['size'])
                    display.resize(event.dict['size'][0], event.dict['size'][1])
                    pygame.display.flip()
                if self.currentMenu.handleEvent(event):
                    inmenu = 0
    def drawMenu(self):
        display.clear()
        self.currentMenu.draw()
        #display.applycam()
        #terrain.draw(display.camx,display.camy)
        #for b in self.walkers:
        #    b.draw()
        #if not simplenet.isServer:
        #    particles.draw()
        pygame.display.flip()
    def addLogText(self, text):
        global log
        log.append(text)
        if len(log)>10:
            log = log[1:]
    def drawLog(self):
        displayratio = display.sh*0.01
        tx = -display.sw2+2*displayratio
        li=-1
        for l in log:
            li+=1
            ty = -display.sh2+2*displayratio+li*displayratio*2
            display.drawWord(pos=[tx+display.camx,ty+display.camy,0], string=l, color=[1,1,1],size=displayratio*20)

