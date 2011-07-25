(ingame, press n to create a new bot at the mouse pointer)
---Neinjarz---
by chozabu@gmail.com (with art from ekib)

This is still in an early state of development, and has lots of missing bits
including  but not limited to:
  -more/better weapons
  -speed optimisations
  -proper networking
  -close range weapons(started)
  -text!(using GLUT for this at the min)
  -installer packages for various systems(an ubuntu deb for me, and an exe for the unwashed masses)

speed really is an issue here, due to a combination of python being a lil slow,
and my physics being very sloppy...


**important**
on startup you will have a single player test game
M opens the menu, but it aint done yet!

--menu-- (PRESS M TO OPEN)
's' starts a server
'c' joins a server
'w' switches to singleplayer
'r' resets the level
edit the servers ip in simplenet.py
also can change res and display options in display.py

--ingame controls--
n creates a new mario "bot" at the mouse position
the mousewheel changes weapon
Q and E change weapon
left click shoots, power is related to distance between a mario and the mouse
right click is ninja rope

WSAD are the keys used for movement
(holding)spacebar jumps
left control is croutch/climb(semi-disabled)
holding V digs

--weapons--
applechaingun - chaingun that looks like an apple
cheapsword - this will be a nice sword...
bow - fires arrows that stick in the ground
bazooka - you need to ask?
grenades - see above
digger - a bazooka that digs a little before exploding
bridge - used for making bridges!
nuke - big bazooka
uzi - small rapid fire gun
dirtcluster - .. fires a cluster of dirt
dirtsprayer - sprays dirt
homing knifes - arrows made of fish
guided darts - fly towards where you aim
shotgun - cluster of bullets
gravgun - fires a bullet that repels you and your enemies
... perhaps some others?

--secondary weapons--
rope - like an elastic ninja rope

--new stuff--
bots can use the rope a little - to help prevent falling off
bots aim at you
now on subversion: http://chozabu.net/neinjarzsvn/
lots of minor changes, speedups and fixes
New art!
can fall off the level
more guns
new art
boarderless levels
networking
nicer code
wrapping on edges of the level - no more!
fall damage
weapons
simple ai

--Known issues--
Arrows, knives, or anything that sticks into the terrain will crash the game if
it happens before an explosion that damages the terrain - needs a fix fo-sure