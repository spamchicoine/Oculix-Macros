import time

s = Screen(1) #run on monitor 0 or 1
Settings.MinSimilarity = 0.8
d = 10 #standard wait time

#Stay at inn
s.wait("Northern_Hollow_Inn-1.png",d).highlight(1).click()
s.wait("Inn_Stay.png",d).highlight(1).click()
s.wait("Economy_Room.png",d).highlight(1).click()
s.wait("OK_option.png",d).highlight(1).click()
s.wait("Refilled.png",d*2).highlight(1).click()
s.wait("Inn_Exit.png",d).highlight(1).click()