import time

#Num_Screens = Screen.getNumberScreens()    # Number of total monitors detected
#Active_Screen = 0    # Screen which holds application

#Screens = []
#for i in range(Num_Screens):
    #Screens.append(Screen(i))

s = Screen(1)
m = True

d = 10 #standard wait time

Settings.MinSimilarity = 0.8
Settings.MoveMouseDelay = 0.5
Settings.ObserveScanRate = 3

Last_icon = None
Last_d = None

#--- Oculix Wrapper ---
def safe_wait(icon, delay):
    while True:
        try:
            icon = s.wait(icon, delay)
            break
    
        except FindFailed:
            while True:
                icon = s.exists("Retry_icon.png",d)
                if icon != None:
                    icon.click()
                else:
                    break
                
    return icon        

#--- Functions ---

def GOTO_Ghost_Castle():
    Settings.MinSimilarity = 0.8
    while True:
        icon = s.exists("Ghost_Castle_Entrance_icon.png",4)
        if icon != None:
            break
        
        Settings.MoveMouseDelay = 0
        icon = s.exists("World_Map_icon.png",d*3)
        if icon != None:
            icon.highlight(1).click()


        time.sleep(4)
        icon = s.exists("Ghost_Castle_Icon.png",d)
        if icon != None:
            icon.highlight(1).click()
            
        else:
            s.click(Location(m*s.x+1190, 1040-100*m))
    return

def GOTO_Northern_Hollow():
    Settings.MinSimilarity = 0.8
    while True:
        icon = s.exists("Inn_Icon.png",d)
        if icon != None:
            print("found inn")
            break
        
        Settings.MoveMouseDelay = 0
        icon = s.exists("Open_World_Map_Icon.png",d*3)
        if icon != None:
            icon.click()

        time.sleep(4)
        icon = s.exists("Northern_Hollow_Icon.png",d)
        if icon != None:
            icon.highlight(1).click()
            
        else:
            print("gotis")           
            s.click(Location(m*s.x+1190, 1040-100*m))
    return

def Open_Map():
    In_Dungeon_icon = In_Dungeon()
    click(Location(In_Dungeon_icon.x, In_Dungeon_icon.y - 100))    # Open Map
    icon = s.exists("Close_Map_Icon.png",d)
    while icon is None:
        click(Location(In_Dungeon_icon.x, In_Dungeon_icon.y - 100))    # Open Map
        icon = s.exists("Close_Map_Icon.png",d)
        
    time.sleep(1)
    return

def In_Dungeon():
    Settings.MinSimilarity = 0.9    
    In_Dungeon_icon = s.wait("In_Dungeon_Icon.png",d*3)    # Make sure we return to dungeon
    In_Dungeon_icon.highlight(1)
    print("In Dungeon")
    Settings.MinSimilarity = 0.8
    return In_Dungeon_icon
    
def Check_Chest():
    Settings.MinSimilarity = 0.8
    checked = True
    Open_Chest_Icon = s.exists("Open_Chest_Icon.png",d*4)
    if Open_Chest_Icon != None:
        Open_Chest_Icon.highlight(1).click()
        print("Found Chest")
            
        Afraid_of_Traps_Icon = s.exists("Afraid_of_Traps_Icon.png",d)
        
        if not Afraid_of_Traps_Icon:    # If not afraid of tresure chests open with MC
            Settings.MinSimilarity = 0.9
            s.wait("MC_icon.png",d).highlight(1).click()    # By default use MC to open chest
            Settings.MinSimilarity = 0.8

            Chest_Trapped_Icon = s.exists("Chest_Trapped_Icon.png",d) # Exit chest if its trapped, not worth it
        
            if Chest_Trapped_Icon != None:
                Chest_Trapped_Icon.highlight(1)
                print("Found Trap")
                Disarm_Chest()
            else:
                print("No Trap")
            
        else:    # If MC is afraid just skip the chest not worth burning fortitude
            Afraid_of_Traps_Icon.highlight(1)
            checked = False
            print("MC afraid of traps")
            s.wait("Close_Icon.png",d).highlight(1).click()
            

        In_Dungeon()
        
        Check_Chest_Fear()
    
    return checked

# If MC is afraid of chests attempt to clear
def Check_Chest_Fear():
    Afraid_of_Traps_icon = s.exists("Afraid_of_Traps_Icon.png",4)
    Settings.MinSimilarity = 0.9
    if Afraid_of_Traps_icon != None:
        Afraid_of_Traps_icon.highlight(1)
        s.wait("MC_icon.png", d).highlight(1).click()    # Open MC char menu
        Paid_Gem_icon = s.wait("Paid_Gem_icon.png",d).highlight(1)    # Wait for menu to load
        s.click(Location(Paid_Gem_icon.x + 520, Paid_Gem_icon.y + 450))    # Open inventory
        Treasure_Fever = s.exists("Treasure_Fever.png",d)    # Check if we have a treasure fever
        
        if Treasure_Fever != None:
            Treasure_Fever.highlight(1).click()
            s.wait("MC_icon.png",d).highlight(1).click()
            s.wait("Item_List_icon.png",d).highlight(1)
            s.click(Location(Paid_Gem_icon.x + 30, Paid_Gem_icon.y + 450))    # Close MC char menu

    Settings.MinSimilarity = 0.8
    return

def Nav_Map():
    
    for i, loc in enumerate(Locations):
        #i+=2
        
        Settings.MinSimilarity = 0.7
        if i == (len(Locations)-1):
            return

        print(C_Flags[i])
        if C_Flags[i]:
            Combat_Loop(i)
        else:
            time.sleep(4)

        # Clear out chests in current region
        Open_Map()
        flag = True
        while flag:
            flag = False

           
            Chest_Region = s.wait(Chest_Regions[i], 5).highlight(1)
            
            Settings.MinSimilarity = 0.9
            Chest_icon = s.findAll("Chest_Icon.png")
            Settings.MinSimilarity = 0.7
            
            for j in Chest_icon:
                j.highlight(1)

                if Chest_Region.contains(j):
                    flag = True
                    j.click()
                    s.click(Location(j.getCenter().x, j.getCenter().y -80))
                    
                    Check_Chest()
                    Open_Map()

                    Settings.MinSimilarity = 0.7
                    # This is to go back an extra region so pathing to the ore ensures facing it
                    #if O_Flags[i] == 1:
                        #icon = s.wait(Locations[i-1],d)
                    #else:
                    icon = s.wait(Locations[i],d)
                    
                    icon.highlight(1).click()
                    s.click(Location(icon.getCenter().x, icon.getCenter().y - 80))
                    time.sleep(5)
                    Open_Map()

        Check_Ore(i)
        Settings.MinSimilarity = 0.7
        icon = s.wait(Locations[i+1],d)
        icon.highlight(1).click()
        s.click(Location(icon.getCenter().x, icon.getCenter().y -80))  
        
        #i-=2
    
    return

def Check_Ore(i):
    
    if Ore_Regions[i] != None:
        s.click(Ore_Regions[i])
        time.sleep(1)
        s.click(Location(Ore_Regions[i].x, Ore_Regions[i].y - 80))
        time.sleep(5)
        
        while True:

            Settings.MinSimilarity = 0.8
            Ore_Deposit = s.exists(Ore_Deposits[i],4)
    
            if Ore_Deposit is None:
                break

            else:
                Ore_Deposit.highlight(1)
                s.click(s.getCenter())
                icon = s.exists("You_Received.png",d).highlight(1)
                if icon != None:
                    s.click(s.getCenter())
                    icon = s.exists("Pickaxe_Broken.png",3)
                    if icon != None:
                        time.sleep(3)
                
        Open_Map()
    return

def Check_Afflictions(s):
    return

def Combat_Loop(i):
    Settings.MinSimilarity = 0.85
    #Check for combat r number of times
    for j in range(r):
        Combat_icon = s.exists("Combat_Icon.png",d*16)    # Flee icon tells us we are in combat
        if not Combat_icon:
            print("combat not found")
            break
        else:
            Combat_icon.highlight(1)
            
            # Cancels searching for combat in next region
            #if R_Flags[i] == 1:
            #    print("Setting next C_Flag to 0")
            #    C_Flags[i+1] = 0
                
            print("combat found")
    
        
        Check_Chest()
        #Check_Afflictions():
    
        In_Dungeon()
    return  # No more combat found

def Disarm_Chest():
    Settings.WaitScanRate = 30
    Settings.MinSimilarity = 0.9
    Settings.MoveMouseDelay = 0
    Disarms_Left_Region = Region(m*s.x + 685, 160 - 100*m, 40, 40)
    Disarm_Region = Region(m*s.x + 650, 55 - 100*m, 632, 70)
    left = m*s.x + 670
    right = m*s.x + 1245
    center = m*s.x + 960
    disarm = m*s.x + 1110

    flag = True
    while flag:
        Disarm_Marker = Disarm_Region.exists("Disarm_Marker.png",0)
        if Disarm_Marker:
            print(Disarm_Marker)
            if Disarm_Marker.x <= left:
                print("At left", Disarm_Marker.x)
                flag = False
    
    flag = True
    while flag:
        Disarm_Marker = Disarm_Region.exists("Disarm_Marker.png",0)
        if Disarm_Marker:
            print(Disarm_Marker)
            if Disarm_Marker.x >= center:
                ncenter = Disarm_Marker.x
                print("At center", ncenter)
                s.click(Location(950+s.x*m, 650 - 100*m))
                flag =  False
                
                icon = Disarms_Left_Region.exists("2_Disarms_Left.png",2)
                if icon is None:
                    return
                
                Disarm_Marker = Disarm_Region.exists("Disarm_Marker.png",1)
                
                Stop_Distance = disarm - (Disarm_Marker.x - ncenter)
                print("Stop_Distance", Stop_Distance)

    flag = True
    while flag:
        Disarm_Marker = Disarm_Region.exists("Disarm_Marker.png",0)
        if Disarm_Marker:
            print(Disarm_Marker)
            if Disarm_Marker.x <= left:
                print("At left", Disarm_Marker.x)
                flag = False
                
    flag = True
    while flag:
        Disarm_Marker = Disarm_Region.exists("Disarm_Marker.png",0)
        if Disarm_Marker:
            print(Disarm_Marker)
            if Disarm_Marker.x >= Stop_Distance:
                s.click(Location(950+s.x*m, 650 - 100*m))
                print("At stop point", Disarm_Marker.x)
                flag =  False
                
    Settings.WaitScanRate = 3
    Settings.MoveMouseDelay = 0.3
    return