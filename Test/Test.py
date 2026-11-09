Regions = ["Region_0.png", "Region_1.png", "Region_2.png", "Region_3.png", "Region_4.png"]

Region_Offset = [[-20, 50], [0, 30], [-35, -20], [35, -20], [0, 0]]

Ore_Deposits  = ["Ore_Deposit_0.png", None, None, None, None]

Ore_Offset = [[200, 160], None, None]    #Offset from corner of Region to ore location

States = ["Stay_Inn", "GOTO_Ghost_Castle", "GOTO_Northern_Hollow", "Clearing_Dungeon"]    #Possible States
State = States[0] # Starting state

In_NH = False
In_GC = False

def New_GOTO_NH():
    global State
    global In_NH

    print("Going to NH")
    
    In_NH = False
    while not In_NH:    # Iterate over possible scenarios and respond accordingly with the respective function
        for j, (func, args) in GOTO_NH.items():
            Settings.MinSimilarity = 0.8
            icon = s.exists(j,0)
            if icon != None:    # Check if scenario is present
                icon.highlight(1)
                print("Found",j)
                func(*args(jcon=icon, target="Northern_Hollow_Icon.png"))     # *args handles passes in an abritrary number of arguments to abritrary functions
                
    return

def At_NH():    # Handle setting flags and states to exit GOTO_Northern_Hollow()
    print("In Northern Hollow")
    global In_NH
    
    In_NH = True
    return

def At_GC():    # Handle setting flags and states to exit GOTO_Ghost_Castle()
    print("In Ghost Castle")
    global In_GC
    
    In_GC = True
    return

def New_GOTO_GC():
    global State
    global In_GC

    print("Going to GC")
    
    In_GC = False
    while not In_GC:    # Iterate over possible scenarios and respond accordingly with the respective function
        for j, (func, args) in GOTO_GC.items():
            Settings.MinSimilarity = 0.8
            icon = s.exists(j,0)
            if icon != None:    # Check if scenario is present
                icon.highlight(1)
                print("Found",j)
                func(*args(jcon=icon, target="Ghost_Castle_Icon.png"))     # *args handles passes in an abritrary number of arguments to abritrary functions
    
    return

# Possible scenarios when clearing dungeon
Clearing_Dungeon = {"Retry_icon.png" : (Network_Retry, lambda **kwargs: ()),    # **kwargs using get to pass specific args to the function
        "In_Dungeon_Icon.png" : (In_Dungeon, lambda **kwargs: ()),
        "Map_Open_Icon.png" : (Nav_Map, lambda **kwargs: (kwargs.get("o"),)),
        "Open_Chest_Icon.png" : (Check_Chest, lambda **kwargs: ()),
        "Chest_Trapped_Icon.png" : (Disarm_Chest, lambda **kwargs: ()),
        "Ghost_Castle_Entrance_Icon.png": (Dungeon_Entrance, lambda **kwargs: (kwargs.get("jcon"),))}

# Possible scenarios when going to Northern Hollow
GOTO_NH = {"Retry_icon.png" : (Network_Retry, lambda **kwargs: ()),    # **kwargs using get to pass specific args to the function
        "Open_World_Map_Icon.png": (Open_World_Map, lambda **kwargs: (kwargs.get("jcon"),)),
        "Zoom_In_Icon.png": (GOTO_World_Map_Target, lambda **kwargs: (kwargs.get("target"),)),
        "Inn_Icon.png": (At_NH, lambda **kwargs: ())}

GOTO_GC = {"Retry_icon.png" : (Network_Retry, lambda **kwargs: ()),    # **kwargs using get to pass specific args to the function
        "Ghost_Castle_Entrance_Icon.png": (At_GC, lambda **kwargs: ()),
        "Zoom_In_Icon.png": (GOTO_World_Map_Target, lambda **kwargs: (kwargs.get("target"),)),
        "World_Map_icon.png": (Open_World_Map, lambda **kwargs: (kwargs.get("jcon"),))}

Stay_Inn = {"Retry_icon.png" : (Network_Retry, lambda **kwargs: ()),    # **kwargs using get to pass specific args to the function
        "Inn_Icon.png": (At_Inn, lambda **kwargs: (kwargs.get("jcon"),)),
        "Inn_Stay_Icon.png": (Inn_Menu, lambda **kwargs: (kwargs.get("jcon"),)),
        "Inn_Eco_Room_icon.png": (click, lambda **kwargs: (kwargs.get("jcon"),)),
        "OK_icon.png": (click, lambda **kwargs: (kwargs.get("jcon"),)),
        "Refilled_Icon.png": (Staying_Inn, lambda **kwargs: (kwargs.get("jcon"),)),
        "Close_lvl_up.png": (click, lambda **kwargs: (kwargs.get("jcon"),)),
        "Level_Up_Next_Icon.png": (click, lambda **kwargs: (kwargs.get("jcon"),))}


flag = True
while flag:
    if State == States[0]:    # Stay at inn
        GOTO_Stay_Inn()
        State = States[1]
        
    elif State == States[1]:    # GOTO Ghost Castle
        New_GOTO_GC()
        State = States[3]

    elif State == States[2]:    # GOTO Northern Hollow
        New_GOTO_NH()
        State = States[0]
        
    elif State == States[3]:    # Clearing dungeon
        Clear_Dungeon()
        State = States[2]

    else:
        print("State not found")
        break