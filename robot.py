#!/usr/bin/env pybricks-micropython


# from ucollections import namedtuple
# import urandom

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, ColorSensor

from time import sleep



# from pybricks.nxtdevices import LightSensor


# ls = LightSensor(Port.S1)       # access light sensor connected to 1


import time

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A)  
right_motor = Motor(Port.D) 

# Initialize the color sensor.
line_sensor_right = ColorSensor(Port.S4) #højre
line_sensor_left = ColorSensor(Port.S3) #venstre

intersect_sensor = ColorSensor(Port.S1) #forreste



# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)


#ofsets RIGHT SENSOR
BLACK_RIGHT = 6
WHITE_RIGHT = 31
threshold_RIGHT = (BLACK_RIGHT + WHITE_RIGHT) / 2  

#ofsets LEFT SENSOR
BLACK_LEFT = 6
WHITE_LEFT = 34
threshold_LEFT = (BLACK_LEFT + WHITE_LEFT) / 2  

# #ofsets intersect sensor
BLACK_FRONT = 5
WHITE_FRONT = 52
threshold_FRONT = (BLACK_FRONT + WHITE_FRONT) / 2  

DRIVE_SPEED = 200
PROPORTIONAL_GAIN = 5 #standard 5


 




def lineFollow(intersect, direc, direc_prev):
    
    

    #sæt hastighed
    if (direc == "u" or direc == "U"):

        if path[0] == "u":
            if direc_prev == "d":
                DRIVE_SPEED = 200
                PROPORTIONAL_GAIN = 6 
            else: 
                DRIVE_SPEED = 500
                PROPORTIONAL_GAIN = 2 #2 er standard

        elif path[0] == "U":
            if direc_prev == "d":
                DRIVE_SPEED = 200
                PROPORTIONAL_GAIN = 6 
            else: 
                DRIVE_SPEED = 500
                PROPORTIONAL_GAIN = 1.5

        else:
            DRIVE_SPEED = 250 #standard 300
            PROPORTIONAL_GAIN = 5
    ## hvis vi lige har drejet
    elif (direc == "d"):
        DRIVE_SPEED = 75 #75
        PROPORTIONAL_GAIN = 7 #6-8
    else:
        DRIVE_SPEED = 200 #standard 200
        PROPORTIONAL_GAIN = 6  #6
        


    while True:
        
        deviation_LEFT = threshold_LEFT - line_sensor_left.reflection() 
        deviation_RIGHT = threshold_RIGHT - line_sensor_right.reflection()  


        #hvis venstre sensor er drejet ind mod linjen - dvs. der er drejet mod højre
        if (deviation_LEFT < 0 and deviation_RIGHT >0):
            
            #drej venstre
            turn_rate = PROPORTIONAL_GAIN * (- deviation_LEFT)

        #hvis højre sensor er drejet mod venstre - dvs. der er drejet mod venstre
        elif (deviation_LEFT > 0 and deviation_RIGHT < 0):
            
            #drej højre
            turn_rate = PROPORTIONAL_GAIN * deviation_RIGHT

        else:
            turn_rate = 0
        
        # Set the drive base speed and turn rate.
        robot.drive(DRIVE_SPEED, turn_rate)
        
        margin = 0 
        #state-machine
        if intersect == False:
           
            if intersect_sensor.reflection() < threshold_FRONT+margin:
                intersect = True
                if direc.isupper() and path[0] != "U":
                    
                    intersect = push(intersect)
                    
                    return intersect

                #hvis næste er "U" så returnerer vi intersect som sædvanligt    
                else:
                    return intersect
        
        if intersect == True:
            if intersect_sensor.reflection() > threshold_FRONT+margin:
                intersect = False      

def push(intersect):

    DRIVE_SPEED = 250 #200 normal
    PROPORTIONAL_GAIN = 5
    margin = 0

    while True:
        
        deviation_LEFT = threshold_LEFT - line_sensor_left.reflection() 
        deviation_RIGHT = threshold_RIGHT - line_sensor_right.reflection()  


        #hvis venstre sensor er drejet ind mod linjen - dvs. der er drejet mod højre
        if (deviation_LEFT < 0 and deviation_RIGHT >0):
            
            #drej venstre
            turn_rate = PROPORTIONAL_GAIN * (- deviation_LEFT)

        #hvis højre sensor er drejet mod venstre - dvs. der er drejet mod venstre
        elif (deviation_LEFT > 0 and deviation_RIGHT < 0):
            
            #drej højre
            turn_rate = PROPORTIONAL_GAIN * deviation_RIGHT

        else:
            turn_rate = 0
        
        # Set the drive base speed and turn rate.
        robot.drive(DRIVE_SPEED, turn_rate)
        
        
        #state-machine
        if intersect == False:
            
            if intersect_sensor.reflection() < threshold_FRONT+margin:
                intersect = True
                intersect = reverse(intersect)
                return intersect
        
        if intersect == True:
            if intersect_sensor.reflection() > threshold_FRONT+margin:
                intersect = False      


def reverse(intersect):
    margin = 0
    while True:
        
        if path[0] == "d": 
            turn_rate = -1
            DRIVE_SPEED = -200 #200 normal
            # Set the drive base speed and turn rate.
        else:
            turn_rate = -0.5
            DRIVE_SPEED = -300 #200 normal
            # Set the drive base speed and turn rate.
                
        robot.drive(DRIVE_SPEED, turn_rate)

        time.sleep(0.5) #0.5
        PROPORTIONAL_GAIN_R = 1

        while (intersect_sensor.reflection() > threshold_FRONT+margin): #while (line_sensor_left.reflection() > (BLACK_LEFT+5) or line_sensor_right.reflection() > (BLACK_RIGHT+5)): #while (intersect_sensor.reflection() > threshold_FRONT):
            ####################
            
            deviation_LEFT = threshold_LEFT - line_sensor_left.reflection() 
            deviation_RIGHT = threshold_RIGHT - line_sensor_right.reflection()  


            #hvis venstre sensor er drejet ind mod linjen - dvs. der er drejet mod højre
            if (deviation_LEFT < 0 and deviation_RIGHT >0):
                
                #drej venstre
                turn_rate = PROPORTIONAL_GAIN_R * (deviation_LEFT)

            #hvis højre sensor er drejet mod venstre - dvs. der er drejet mod venstre
            elif (deviation_LEFT > 0 and deviation_RIGHT < 0):
                
                #drej højre
                turn_rate = PROPORTIONAL_GAIN_R * (-deviation_RIGHT)

            else:
                turn_rate = 0
            
            # Set the drive base speed and turn rate.
            robot.drive(DRIVE_SPEED, turn_rate)

        #########################

        
        intersect = True
        return intersect



def turn(direc):
    
    while True:
        
        

        DRIVE_SPEED = 300 # 300 er liderligt
        turn_rate = 0
        robot.drive(DRIVE_SPEED, turn_rate)
        
        intersection = True
        margin = 5

        # while(True):
        #     #state-machine
        #     if intersection == False:

        #         if (line_sensor_left.reflection() < (threshold_LEFT+margin) and line_sensor_right.reflection() < (threshold_RIGHT+margin)):
        #             break #intersection = True - forlad loop og begynd at dreje

        #     else: #intersection == True
        #         if (line_sensor_left.reflection() > (threshold_LEFT+margin) and line_sensor_right.reflection() > (threshold_RIGHT+margin)):
        #             intersection = False      

        if (line_sensor_left.reflection() < (threshold_LEFT+margin) and line_sensor_right.reflection() < (threshold_RIGHT+margin)):

        # if (line_sensor_left.reflection() < threshold_LEFT and line_sensor_right.reflection() < threshold_RIGHT):

            if(direc =="l" or direc == "L"):
                                

                

                DRIVE_SPEED = 10 #10
                turn_rate = -150 #-160
                robot.drive(DRIVE_SPEED, turn_rate)        
                time.sleep(0.5) #0.5


#########################################
                DRIVE_SPEED = 10
                turn_rate = -100    #100 standard 
                robot.drive(DRIVE_SPEED, turn_rate)  
                check = False

                while True:
                    if check == False:
                        if (line_sensor_left.reflection() < threshold_LEFT):
                            check = True
                    else:
                        if(line_sensor_left.reflection() > threshold_LEFT):
                            
                            break
########################################

                intersect = False
                intersect = lineFollow(intersect, direc, direc_prev) 

                
                return intersect
            else:
                

                DRIVE_SPEED = 10 #10
                turn_rate = 160 #150-170
                robot.drive(DRIVE_SPEED, turn_rate)        
                time.sleep(0.5)
                intersect = False
                intersect = lineFollow(intersect, direc, direc_prev)        
                
                return intersect

def spin(intersect):
    DRIVE_SPEED = 0 
    turn_rate = -160    #180 standard 
    robot.drive(DRIVE_SPEED, turn_rate)        
    time.sleep(1)

    turn_rate = -120    #180 standard 
    robot.drive(DRIVE_SPEED, turn_rate)  
    check = False

    while True:
        if check == False:
            if (line_sensor_left.reflection() < threshold_LEFT):
                check = True
        else:
            if(line_sensor_left.reflection() > threshold_LEFT+2):
                break

        # turn_rate = -180 
        # robot.drive(DRIVE_SPEED, turn_rate) 
        # if(line_sensor_left.reflection() < BLACK_LEFT+5):    #if(line_sensor_left.reflection() < threshold_LEFT):
                   
        #     break

    
    intersect = False
    intersect = lineFollow(intersect, direc, direc_prev) 
    return intersect



#indsæt local path right heeeere"
path_string = "uuLrUUUUduulruuurRUUUUUrlLUlrRlluulrLduruuruurulrurlrRrLUUUrlLUlrululrLrlLUUUrlLdlL"#"uuLrUUUUduulruuurRUUUUUrlLUlrRlluulrLduruuruurulrurlrRrLUUUrlLUlrululrLrlLUUUrlLdlL"
           
path = list(path_string)
path.append("u")


# path = ["l","u","L","r","U","U","U","U"]
# path.append("u")

direc_prev = "u"
direc = "u"
intersect = False

if intersect_sensor.reflection() < threshold_FRONT:
    intersect = True  

else:
    intersect = False


while path:
    
    
    #intersection
    if(intersect):

        # ev3.speaker.beep()
        # ev3.speaker.beep()
        direc_prev = direc
        direc = path.pop(0)
        
        if direc == "l" or direc == "r" or direc == "L" or direc == "R":
            intersect = turn(direc)
        elif direc == "d":
            intersect = spin(intersect)    #intersect = reverse(intersect)
        else:
            intersect = lineFollow(intersect, direc, direc_prev)


    
    #NOT intersection
    else:
        intersect = lineFollow(intersect, direc, direc_prev)   