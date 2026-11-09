Locations = [
        "Location_0.png","Location_1.png","Location_2.png","Location_12.png"]

Chest_Regions = [
        "Chest_Region_0.png","Chest_Region_1.png","Chest_Region_2.png"]

Ore_Deposits  = [None, "Ore_Deposit_0.png", None, None]

Ore_Regions = [None, Location(m*s.x+ 1140, 790 - 100*m), None, None]

C_Flags = [0, 0, 1, 0]


#R_Flags = [0, 0, 0, 1, 0, 0, 1, 0]    # Used to prevent searching for combat in next area

#O_Flags = [0, 0, 0, 0, 1, 0, 0, 1]    # Used to correct pathing to ore

r=1

while True:

    GOTO_Ghost_Castle()

    for f in range(3):
        s.wait("Ghost_Castle_Entrance_icon.png",d*2).highlight(1).click()

        Nav_Map()

    GOTO_Northern_Hollow()

    Inn_Stay()