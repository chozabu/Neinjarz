# -*- coding: utf-8 -*-
#try:
import pygame#, sys
import os
#import Numeric as N
from pygame.locals import *
surfarray = pygame.surfarray
if not surfarray: raise ImportError
#except ImportError:
#    raise ImportError, 'Error Importing Pygame/surfarray or Numeric'

import OpenGL.GL as GL
#from OpenGL.GLU import *
import simplenet

import display

from math import hypot
import particles

destructable = True
#destructable = False

tilesize = 64
bounding = 1
rescale = 1
levelloaded = False

imgalpha = []
imgpixels = []

global data
data = None

def prime():
    global imgalpha, imgpixels, data
    #data.lock()
    imgalpha = surfarray.pixels_alpha(data)
    imgpixels = surfarray.pixels3d(data)
def unprime():
    global imgalpha, imgpixels, data
    del imgalpha
    del imgpixels
    #data.unlock()

def resettex(x, y):
    GL.glBindTexture(GL.GL_TEXTURE_2D, tidl[y][x])
    unprime()
    textureSurface = data.subsurface(x*tilesize, y*tilesize, tilesize, tilesize)
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    GL.glTexSubImage2D(GL.GL_TEXTURE_2D,  0,   0 , 0 ,   tilesize ,  tilesize , GL.GL_RGBA ,   GL.GL_UNSIGNED_BYTE  ,  textureData)
    prime()
    #tidl[y][x] = settexi(x, y, tidl[y][x])

def settexi(x, y, tex):
    textureSurface = data.subsurface(x*tilesize, y*tilesize, tilesize, tilesize)
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    texid = tex
    GL.glBindTexture(GL.GL_TEXTURE_2D, texid)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, textureSurface.get_width(),
            textureSurface.get_height(), 0,
            GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, textureData)
    return texid

def settex(x, y):
    return settexi(x, y, GL.glGenTextures(1))

def loadimg(imgname):
    global levelloaded
    imgname = os.path.join("levels", imgname)
    matimgname = os.path.join(imgname, "njmaterial.png")#todo material file thing
    imgname = os.path.join(imgname, "njlandscape.png")
    global data, imgrect, tidl
    global x2, y2, xw, yw
    data = pygame.image.load(imgname)
    rescale = 0.5
    if rescale != 1:
      data = pygame.transform.rotozoom(data, 0, rescale)
    imgrect = data.get_rect()
    x, y, x2, y2 = imgrect
    display.setmaxs(x2, y2)
    xw = int(x2/tilesize)
    yw = int(y2/tilesize)
    if levelloaded:
      for xdel in tidl:
        for ydel in xdel:
          GL.glDeleteTextures(ydel)
    tidl = [[-1 for i in list(range(0, xw, 1))] for r in list(range(0, yw, 1))]
    y = 0
    for xp in list(range(0, yw)):
        x = 0
        for yp in list(range(0, xw)):
            #if not levelloaded:
            tidl[y][x] = settex(x, y)
            #else:
            #  resettex(x, y):
            x += 1
        y += 1
    #if not levelloaded:
    genterrainlist()
    prime()
    levelloaded = True

toupdate = []
def updatelist(x, y):
    #x= int(x/tilesize)
    #y= int(y/tilesize)
    if x < 0:return
    if y < 0: return
    if x >= xw:return
    if y >= yw: return
    for i in toupdate:
        if i == [x, y]:
            return
    toupdate.append([x, y])
def getTile(x, y):
    return int(x/tilesize), int(y/tilesize)
def getTileOffs(x, y):
    return x-(int(x/tilesize)*tilesize), y-(int(y/tilesize)*tilesize)

def pastesurfID(pixID, x, y, ang, scale):
    simplenet.sendall("pastetex", [pixID, x, y, ang, scale])
    pix = pygame.transform.rotozoom(display.lookuppixID(pixID), ang, scale)
    x = x-pix.get_width()/2
    y = y-pix.get_height()/2
    pastesurf(pix, x, y)




def pastesurf(surf, x, y):
    #global data
    unprime()
    surf.unlock()
    data.unlock()
    #print( data.get_locked() )
    #while(data.get_locked()):
    #    print "unlocking"
    #    print data.unlock()
    #    print data.get_locked()
    data.blit(surf, (x, y))
    prime()
    tx, ty = getTile(x, y)
    updatelist(tx, ty)

    updatelist(tx+1, ty+1)
    updatelist(tx-1, ty+1)
    updatelist(tx, ty+1)
    updatelist(tx+1, ty-1)
    updatelist(tx-1, ty-1)
    updatelist(tx, ty-1)
    updatelist(tx+1, ty)
    updatelist(tx-1, ty)

def updaterad(x, y,radius):
    radius/=tilesize
    x-=radius+1
    y-=radius+1
    for xp in list(range(int(x),int(x+radius*2+3))):
      for yp in list(range(int(y),int(y+radius*2+3))):
        updatelist(xp,yp)
    #return int(x/tilesize), int(y/tilesize)

def explode(x, y, radius = 50, setto = 0):
    if not destructable: return
    simplenet.sendall("boom", [x, y, radius, setto])
    #game.explode(x, y, radius, setto)
    radp1 = radius+1
    rad2 = radius*radius
    x = int(x)
    y = int(y)
    tilex, tiley = getTile(x, y)

    updatelist(tilex, tiley)

    l = x-radius
    r = x+radp1
    t = y-radius
    b = y+radp1
    if l < 0: l = 0
    if t < 0: t = 0
    if b >= y2-1: b = y2-2
    if r >= x2-1: r = x2-2
    if radius > 6:
        #particles.addParticle(x, y, 0.5, "smoke.png", radius/10, int((radius-5)*0.15+1))
        #particles.addParticle(x, y, 0.5, "fire.png", radius/10, int((radius-5)*0.05+1))
        updaterad(tilex,tiley,radius)
        '''updatelist(tilex+1, tiley+1)
        updatelist(tilex-1, tiley+1)
        updatelist(tilex, tiley+1)
        updatelist(tilex+1, tiley)
        updatelist(tilex-1, tiley)
        updatelist(tilex+1, tiley-1)
        updatelist(tilex, tiley-1)
        updatelist(tilex-1, tiley-1)'''
    for xp in list(range(int(l), int(r))):
        for yp in list(range(int(t), int(b))):
            xd = xp-x
            yd = yp-y
            #if imgalpha[xp][yp] > setto:
            if xd * xd + yd * yd < rad2:
                imgalpha[xp][yp] = setto

def traceline(x, y, dirx, diry, movesleft = 250):
    mag = hypot(dirx, diry)
    dirx /= mag
    diry /= mag
    while movesleft > 0:
        movesleft -= 1
        x += dirx
        y += diry
        '''if x > x2 - 10:
            return x, y
        if y > y2 - 10:
            return x, y
        if x < 10:
            return x, y
        if y < 10:
            return x, y'''
        if getalpha(int(x), int(y)) > 128:
            return x, y
    return None

def getalpha(x, y):
    if x < 1:return 0
    if x > x2-5:return 0
    if y < 1:return 0
    if y > y2-5:return 0
    retval = imgalpha[x][y]
    return retval

def getcolour(x, y):
    retval = imgpixels[int(x)][int(y)]
    rv2=[float(retval[0])/255.0,float(retval[1])/255.0,float(retval[2])/255.0]
    return rv2
def getnormal(x, y, rad=1):
    xa = 0.000000001
    ya = 0.000000001

    for xp in list(range(-rad, rad+1)):
        for yp in list(range(-rad, rad+1)):
            #if imgalpha[xp+x][yp+y] > 128:
            #    xa-=xp
            #    ya-=yp
            xa -= xp * imgalpha[xp + x][yp + y]
            ya -= yp * imgalpha[xp + x][yp + y]
    mag = hypot(xa, ya)
    return (xa / mag, ya / mag)

listid = 1

def genterrainlist():
    global listid
    if levelloaded:
      GL.glDeleteLists(listid,1)
    listid = GL.glGenLists(1)
    GL.glNewList(listid, GL.GL_COMPILE)

    l = 0
    r = xw
    t = 0
    b = yw

    xpos = 0
    ypos = 0
    xpos2 = tilesize
    ypos2 = tilesize
    y = t
    for xp in list(range(t, b)):
        x = l
        ypos = y*tilesize
        ypos2 = ypos+tilesize
        for yp in list(range(l, r)):
            xpos = x*tilesize
            xpos2 = xpos+tilesize
            GL.glBindTexture(GL.GL_TEXTURE_2D, tidl[y][x])
            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0.0, 1)
            GL.glVertex3f(xpos, ypos, 0)
            GL.glTexCoord2f(1, 1)
            GL.glVertex3f(xpos2, ypos, 0)
            GL.glTexCoord2f(1, 0.0)
            GL.glVertex3f(xpos2, ypos2, 0)
            GL.glTexCoord2f(0.0, 0.0)
            GL.glVertex3f(xpos, ypos2, 0)
            GL.glEnd()
            x += 1
        y += 1
    GL.glEndList()

def draw(cx,cy):
    global toupdate,x2,y2
    if len(toupdate) > 0:
        for i in toupdate:
            resettex(i[0], i[1])
        toupdate = []



    GL.glColor4f(1.0, 1.0, 1.0,1.0)
    GL.glCallLists([listid])
    #GL.glTranslatef(0,0,-1000)
    '''cx = int(display.camx/tilesize)
    cy = int(display.camy/tilesize)
    l = cx-3*3-1
    r = cx+4*3
    t = cy-3*3
    b = cy+4*3
    if l<0:l=0
    if t<0: t=0
    if r>xw:r=xw
    if b > yw: b = yw
    '''
