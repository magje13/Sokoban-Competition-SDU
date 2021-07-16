def newRoute(path):
    
    route=list(path)
    retur = ("") # empty string
    index =[] # empty list
    previous = 0
    current = 0
    theRealDeal = 0
    for x in range(len(route)-1): #last movement is excluded, as it will always
        #be superfluous
        
        # directions are turned into degrees to change
            #from universal coordinate to robot coordinate
        
        if route[x] == 'u' or route[x] == 'U': 
            current = 0
        elif route[x] == 'r' or route[x] == 'R':
            current = 90
        elif route[x] == 'd' or route[x] == 'D':
            current = 180
        elif route[x] == 'l' or route[x] == 'L':
            current = 270
        
        
        if route[x] != 'R' or route[x] != 'L' or route[x] != 'U' or route[x] != 'D':
            theRealDeal = current-previous #difference in degrees between
            #two adjacent movements
            previous = current
            if  theRealDeal == 0 or theRealDeal == 360:  #degree differences 
                #are translated back into new directions corresponding to the 
                #orientation of the robot
                retur = retur + 'u'
            elif theRealDeal == 90 or theRealDeal == -270:
                 retur = retur + 'r'
            elif theRealDeal == 180 or theRealDeal == -180:
                retur = retur + 'd'
            elif theRealDeal == -90 or theRealDeal ==270:
                retur = retur + 'l'
        else:
            theRealDeal = current-previous #difference in degrees between
            #two adjacent movements
            previous = current
            if  theRealDeal == 0 or theRealDeal == 360:  #degree differences 
                #are translated back into new directions corresponding to the 
                #orientation of the robot
                retur = retur + 'U'
            elif theRealDeal == 90 or theRealDeal == -270:
                 retur = retur + 'R'
            elif theRealDeal == 180 or theRealDeal == -180:
                retur = retur + 'D'
            elif theRealDeal == -90 or theRealDeal ==270:
                retur = retur + 'L'

    return retur
