

import settings

import os
import sys
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
#from OpenGL.GLU import *

import pygame
from pygame.locals import OPENGL, DOUBLEBUF, RESIZABLE


theme = "nintenjo"

sw = settings.jdata['xres']
sh = settings.jdata['yres']
#sw = 300
#sh =200
sw2 = sw/2
sh2 = sh/2
#tilesize = 128
''''''
#screen = pygame.display.set_mode((sw,sh), OPENGL|DOUBLEBUF | FULLSCREEN | HWSURFACE, 32)
#screen = pygame.display.set_mode((sw,sh), OPENGL|DOUBLEBUF | FULLSCREEN)
screen = pygame.display.set_mode((sw,sh), OPENGL|DOUBLEBUF|RESIZABLE)


def resize(x,y):
    global sw, sh, sw2, sh2, screen
    screen = pygame.display.set_mode((x,y), DOUBLEBUF | RESIZABLE | OPENGL)
    sw=x
    sh=y
    sw2=x/2
    sh2=y/2
    GL.glViewport(0, 0, sw, sh)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    #gluPerspective(45, 1.0*sw/sh, 0.1, 2000.0)
    GL.glOrtho(-sw2,sw2,-sh2,sh2,-2000,2000)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()

    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glClearColor(0.5, 0.5, 0.5, 0.0)
    GL.glClearDepth(1.0)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glDepthFunc(GL.GL_LEQUAL)
    GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST)

    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

def init():
    GLUT.glutInit(sys.argv)
    resize(sw, sh)


camx = 100
camy = 100

maxx = sw
maxy = sh

def setmaxs(x,y):
    global maxx,maxy
    maxx = x-sw2
    maxy = y-sh2

def applycam():
    global camx, camy
    GL.glTranslatef(-camx,-camy, -1200.0)

def clear():
    #GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
    GL.glClear(GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glScalef(1,-1,1)
    GL.glPushMatrix()
    GL.glTranslatef(0,0,-1200)
    GL.glScalef(sw,sh,100)

    GL.glDisable(GL.GL_TEXTURE_2D)
    GL.glBegin(GL.GL_QUADS)
    GL.glColor4f(0.8, 0.8, 1.0,0.6)
    GL.glVertex3f(1.0, 1.0, 0.0)

    GL.glColor4f(0.8, 0.8, 1.0,0.6)
    GL.glVertex3f(-1.0, 1.0, 0.0)

    GL.glColor4f(0.0, 0.0, 1.0,0.6)
    GL.glVertex3f(-1.0, -1.0, 0.0)

    GL.glColor4f(0.0, 0.0, 1.0,0.6)
    GL.glVertex3f(1.0, -1.0, 0.0)
    GL.glEnd()
    #drawWord(pos=[0,0,0], string="hello world", color=[1,1,1])
    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glPopMatrix()

def lookat(x,y):
    global camx,camy
    camx = (x*0.5+camx*0.5)
    camy = (y*0.5+camy*0.5)
    camx,camy=camlimit(camx,camy)
def camlimit(camx,camy):
    #if camx < sw2: camx = sw2
    #if camy < sh2: camy = sh2
    #if camx > maxx: camx = maxx
    #if camy > maxy: camy = maxy
    return camx,camy

namelist = []
def loadtex(filename):
    #filename = os.path.join(theme, filename)
    #filename = os.path.join("images", filename)
    for i in namelist:
        if i[0] == filename:
            return i[1]
    textureSurface = loadpix(filename)
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    texid = GL.glGenTextures(1)
    if texid == 0:
        texid = GL.glGenTextures(1)
    if texid == 0:
        texid = 999
    namelist.append((filename,texid))
    GL.glBindTexture(GL.GL_TEXTURE_2D, texid)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, textureSurface.get_width(),
            textureSurface.get_height(), 0,
            GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, textureData)
    return texid

pixnamelist = []
def loadpix(filename):
    ofn = filename
    filename = os.path.join(theme, filename)
    filename = os.path.join("images", filename)
    #for i in pixnamelist:
    #    if i[0] == filename:
    #        return i[1]
    textureSurface = pygame.image.load(filename)
    #textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    print( "loaded: " + ofn + " as " + str(len(pixnamelist)) )
    pixnamelist.append((filename,textureSurface,len(pixnamelist)))
    return textureSurface

def loadpixID(filename):
    filename = os.path.join(theme, filename)
    filename = os.path.join("images", filename)
    for i in pixnamelist:
        if i[0] == filename:
            return i[2]
    textureSurface = pygame.image.load(filename)
    #textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    pixnamelist.append((filename,textureSurface,len(pixnamelist)))
    return len(pixnamelist)-1

def lookuppixID(number):
    return pixnamelist[number][1]

def drawWord(pos, string, color, size=1):
   #print pos,string,color
   #print string
   GL.glDisable(GL.GL_TEXTURE_2D)
   GL.glLineWidth(1.5)
   r, g, b = color
   GL.glPushMatrix()
   GL.glColor4f(r, g, b, .5)
   GL.glTranslatef(*pos)
   s = size*0.001
   GL.glScalef(s, -s, s)
   for char in string:
      GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, ord(char))
   GL.glPopMatrix()
   GL.glEnable(GL.GL_TEXTURE_2D)

def genquadlist():
    listid = GL.glGenLists(1)
    GL.glNewList(listid, GL.GL_COMPILE)
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
    GL.glEndList()
    return listid
def genquadlist2():
    listid = GL.glGenLists(1)
    GL.glNewList(listid, GL.GL_COMPILE)
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
    GL.glEndList()
    return listid

qid = genquadlist()
qid2 = genquadlist2()
