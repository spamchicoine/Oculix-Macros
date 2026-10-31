import time
import sys

# Actions Specific to the start of this dungeon
# Start in Northern Village or Luknaria maybe

GOTO_Ghost_Castle(s)    # Go to Ghost Caslte on world map

s.wait("Zone_1_Baileys.png",d).highlight(1).click() # Enter baileys

s.wait("Move_To_Exit_Icon.png",d*3).highlight(1) # Wait until dungeon loads

# Turn Around
s.keyDown("d")
time.sleep(0.1)
s.keyUp("d")

time.sleep(1)
s.keyDown("d")
time.sleep(0.1)
s.keyUp("d")

Combat_Loop(s)

#