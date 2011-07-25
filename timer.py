'''a simple timer'''
from pygame import time
import time as systime

turntime = 0.0
#steptime = 20.0
desiredfps = 20.0
maxturntime = int(1000/desiredfps)
fps = 0
totaltime = 0
totalturns = 0
clock = time.Clock()

def tick():
    global turntime, totaltime, totalturns, fps
    totalturns+=1
    turntime = clock.tick()# / steptime
    if turntime > maxturntime:turntime = maxturntime
    time.wait(maxturntime-turntime)
    totaltime = time.get_ticks()
    #fps = 1000/(fps*0.1+(totaltime/totalturns)*0.9)
    #print fps