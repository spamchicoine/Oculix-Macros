import time
import sys

s = Screen(1)
m = True

d = 10 #standard wait time

Settings.MinSimilarity = 0.8
Settings.MoveMouseDelay = 0.5
Settings.ObserveScanRate = 3

Stop_Distance = 0
Dungeon_Entered = False
Region_Clear = False
Stayed_Inn = False
Exiting_Inn = False

MC_Map_Icons = ["MC_Map_Icon_0.png", "MC_Map_Icon_1.png", "MC_Map_Icon_2.png", "MC_Map_Icon_3.png"]

#--- Functions ---

def GOTO_World_Map_Target(target):    # Try to find and click on the target location in world map
    print("Going to world map target")
    jcon = s.exists(target, 2)
    if jcon != None:
        print("Found world map target")
        jcon.highlight(1).click()
        
    else:
        print("Exiting World Map")
        s.click(Location(m*s.x+1190, 1040-100*m))    # Location of exit button used because it could be obscured by game cursor
        
    return

def Open_World_Map(icon):    # Click the open map button provided
    print("Opening world map")
    icon.highlight(1).click()
    return

def Network_Retry():
    icon = s.exists("Retry_icon.png",1)
    while icon != None:
        icon.highlight(1).click()
        icon = s.exists("Retry_icon.png", 1)
    return

def Open_Map():
    icon = s.exists("In_Dungeon_Icon.png",2)
    if icon != None:
        click(Location(icon.x, icon.y - 100))
        time.sleep(1)
    return

def In_Dungeon():
    Settings.MinSimilarity = 0.9    
    In_Dungeon = False
    s.exists("In_Dungeon_Icon.png", d*3)
    
    for i in range(2):
        time.sleep(1)
        icon = s.exists("In_Dungeon_Icon.png",0)

        if icon != None:
            icon.highlight(1)
            In_Dungeon = icon
        else:
            In_Dungeon = None
            break
    if In_Dungeon:
        Open_Map()
            
    print("In Dungeon", In_Dungeon)
    Settings.MinSimilarity = 0.8
    return In_Dungeon
    
def Check_Chest():
    Settings.MinSimilarity = 0.8
    checked = False
    
    Open_Chest_Icon = s.exists("Open_Chest_Icon.png",d*4)
    if Open_Chest_Icon != None:
        Open_Chest_Icon.highlight(1).click()
        checked = True
        print("Found Chest")
            
    Afraid_of_Traps_Icon = s.exists("Afraid_of_Traps_Icon.png",d)
    if Afraid_of_Traps_Icon != None:    # If not afraid of tresure chests open with MC
        Afraid_of_Traps_Icon.highlight(1)
        checked = False
        print("MC afraid of traps")
        icon = s.exists("Close_Chest_Icon.png",d)
        if icon != None:
            icon.highlight(1).click()
    else:
        Settings.MinSimilarity = 0.9
        icon = s.exists("MC_icon.png",d)
        if icon != None:
            icon.highlight(1).click()    # By default use MC to open chest
        Settings.MinSimilarity = 0.8

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

def Check_Afflictions(s):
    return

def Dungeon_Entrance(icon):    # Handle setting flags and states to exit Clear_Dungeon()
    global Region_Clear
    global Dungeon_Entered

    if not Dungeon_Entered:
        icon.highlight(1).click()
        Dungeon_Entered = True
        
    else:
        Region_Clear = True
    return

def Clear_Dungeon():
    global State
    global Region_Clear
    global Dungeon_Entered

    print("Clearing Dungeon")
    Dungeon_Entered = False

    for i, reg in enumerate(Regions):    # Iterate over distinct regions within the dungeon
        Region_Clear = False
        
        while not Region_Clear:    # Iterate over possible scenarios and respond accordingly with the respective function
            for j, (func, args) in Clearing_Dungeon.items():
                Settings.MinSimilarity = 0.8
                icon = s.exists(j,0)
                if icon != None:    # Check if scenario is present
                    icon.highlight(1)
                    print("Found",j)
                    func(*args(o=i, jcon = icon))    # *args handles passes in an abritrary number of arguments to abritrary functions

def Nav_Map(o):
    global Region_Clear

    Settings.MinSimilarity = 0.7
    print("Checking for region", o)
    Reg = s.exists(Regions[o], 2).highlight(1)
    
    if Reg != None:
        
        Settings.MinSimilarity = 0.9
        print("Checking for chests in region", o)
        Chest_icon = Reg.exists("Chest_Icon.png",2)
        Settings.MinSimilarity = 0.7

        if Chest_icon != None:
            print("Found chest in region", o)
            Chest_icon.click()
            click(Location(Chest_icon.getCenter().x, Chest_icon.getCenter().y -80))
            time.sleep(10)
        
        else:
            # Go to region park position
            Settings.MinSimilarity = 0.9
            for i in MC_Map_Icons:
                icon = s.exists(i,1)
                        
                if icon != None:
                    icon.highlight(1)
                    
                    if icon.contains(Location(Reg.getCenter().x + Region_Offset[o][0], Reg.getCenter().y + Region_Offset[o][1])):
                        print("Already at park position")
                        
                        if Ore_Deposits[o] != None:
                            print("Going to ore deposit")
                            
                            if icon.contains(Location(Reg.x + Ore_Offset[o][0], Reg.y + Ore_Offset[o][1])):
                                print("Already at ore deposit")
                            else:
                                click(Location(Reg.x + Ore_Offset[o][0], Reg.y + Ore_Offset[o][1]))
                                click(Location(Reg.x + Ore_Offset[o][0], Reg.y + Ore_Offset[o][1] - 80))
                                time.sleep(5)
                            
                            if Check_Ore(o):
                                print("Region", o, "Clear")
                                Region_Clear = True
                        else:
                            print("Region", o, "Clear")
                            Region_Clear = True
                            
                    else:
                        click(Location(Reg.getCenter().x + Region_Offset[o][0], Reg.getCenter().y + Region_Offset[o][1]))
                        click(Location(Reg.getCenter().x + Region_Offset[o][0], Reg.getCenter().y + Region_Offset[o][1] - 80))
                    break

            else:
                print("No ore deposit")
               
    return

def Combat_Loop(i):
    Settings.MinSimilarity = 0.85
    #Check for combat r number of times
    for j in range(r):
        Combat_icon = s.exists("Combat_Icon.png",d*6)    # Flee icon tells us we are in combat
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
    
        
        if Check_Chest():
            time.sleep(1)
            Disarm_Chest()
        #Check_Afflictions():
    
        if In_Dungeon() is None:
            sys.exit("Not in dungeon")
            
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

    icon = Disarms_Left_Region.exists("3_Disarms_Left.png", 2)
    if icon != None:
    
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
                    
    icon = Disarms_Left_Region.exists("2_Disarms_Left.png",2)
    jcon = Disarms_Left_Region.exists("1_Disarms_Left.png", 2)
    if icon != None or jcon != None:
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

def Check_Ore(i):
    Deposit_Cleared = False
    while True:

        Settings.MinSimilarity = 0.8
        Ore_Deposit = s.exists(Ore_Deposits[i],4)
    
        if Ore_Deposit is None:
            print("Ore deposit not detected")
            Ore_Socket = s.exists("Ore_Socket.png",4)
            if Ore_Socket != None:
                Ore_Socket.highlight(1)
                print("Ore Socket Detected")
                Deposit_Cleared = True
                
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
                
    return Deposit_Cleared

def GOTO_Stay_Inn():
    global State
    global Exited_Inn
    global Stayed_Inn

    print("Staying at Inn")
    
    Exited_Inn = False
    Stayed_Inn = False
    
    while not Exited_Inn:    # Iterate over possible scenarios and respond accordingly with the respective function
        for j, (func, args) in Stay_Inn.items():
            Settings.MinSimilarity = 0.8
            icon = s.exists(j,0)
            if icon != None:    # Check if scenario is present
                icon.highlight(1)
                print("Found",j)
                func(*args(jcon=icon))     # *args handles passes in an abritrary number of arguments to abritrary functions
    
    return

def At_Inn(icon):
    global State
    global Exited_Inn
    global Stayed_Inn

    if Stayed_Inn:
        Exited_Inn = True
        
    else:
        icon.highlight(1).click()
    
    return

def Inn_Menu(icon):
    global Stayed_Inn
    global State

    if Stayed_Inn:
        jcon = s.exists("Inn_Exit_icon.png", 2)
        if jcon != None:
            jcon.highlight(1).click()
            
    else:
        icon.highlight(1).click()
        
    return

def Staying_Inn(icon):
    global Stayed_Inn

    Stayed_Inn = True
    icon.highlight(1).click()

    return