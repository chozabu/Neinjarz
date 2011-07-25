#import baseparticle
import smokeparticle
import textparticle

import simplenet

particles = []
#display.loadtex("fire.png")

def addParticle(x, y, startspeed, img, scale, num,colour=[1,1,1]):
    global particles
    simplenet.sendall("addps", [x, y, startspeed, img, scale, num,colour])
    #if simplenet.isServer:
    #  return
    startspeed = num/25.0
    for i in range(num):
        particles.append(smokeparticle.smokeparticle(x,y,img,scale,startspeed,colour))

def addTextParticle(x, y, startspeed, img, scale, colour=[1,1,1]):
    global particles
    simplenet.sendall("addtps", [x, y, startspeed, img, scale, colour])
    #if simplenet.isServer:
    #  return
    particles.append(textparticle.textparticle(x,y,img,scale,1,colour))

def update():
    global particles
    remlist = []
    for i in particles:
        i.move()
        if i.dead:
            remlist.append(i)
    for i in remlist:
        particles.remove(i)
    

def draw():
    global particles
    for i in particles:
        i.draw()



