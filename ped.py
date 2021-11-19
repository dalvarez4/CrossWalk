import random
import numpy as np

def Uniform(a,b):
    return a + (b - a) * random.random()

def Exponential(mew):
    return -mew * np.log(1 - random.random())



traffic_signals = ['r', 'y', 'g']

ped_signals = ['w', 'nw']

#target values

d_a = 0

d_p = 0

#geometry constants

traffic_sources = 2
ped_sources = 2
#in feet
cw_traffic = 24
cw_peds = 46
ped_to_button = 12

B = 330
w = cw_traffic
S = cw_peds
L = 9

#in seconds
RED = 18
YELLOW = 8
GREEN = 35

#rate per minute
lambda_p = 3
lambda_a = 4

#mph
#auto speed
v_j = Uniform(25, 35)
#ft/s/s
#auto acceleration
a = 10
#ft/s
#ped speed
v_k = Uniform(2.6, 4.1)
#pedestrians accelerate instantly
#autos only accelerate if delayed

#state stuff
signal_clock_remainder = 0

def b_j(v_j, a):
    return v_j**2/(2*a)
def t_j(v_j, a):
    return v_j / a
def h_j(e_j, B, S, w, b_j, v_j, t_j):
    return e_j + ((7/2*B + 3*S - w/2 - b_j) / v_j) + t_j
def can_cross(speed, distance, crossed):
    if crossed >= 20:
        return False
    return (distance + cw_peds) / speed <= signal_clock_remainder
def will_press(waiting, waited_min, stranded):
    if waited_min:
        return True
    if waiting == 0 or stranded:
        return Uniform(0, 16) <= 15
    else:
        return Uniform(0, waiting + 1) <= waiting

class ped:
    last_time = 0
    speed = Uniform(2.6, 4.1)
    delay_start = 0

    def __init__(self, time, event, event_list, num_peds):
        self.last_time = time
        self.at_button = 'do'
        self.id = num_peds + 1
        self.walked = False
        #need to determine whther or not they will make the walk cycle if there is one
        #add ped_impatiant for one minute after arriving at button
    
    def update(event, time, event_list):
        # AUTO_ARRIVAL, PED_ARRIVAL, PED_AT_BUTTON, PED_IMPATIENT, GREEN_EXPIRES, YELLOW_EXPIRES, RED_EXPIRES, AUTO_EXIT and PED_EXIT.
        if event == 'walk':
            '''only first 20 pedestrians that can make it will cross'''
            #if can walk add a ped exit event
            print('sommin')
        if event == 'no walk':
            '''this will be anytime the light is not red'''
            print('sommin')
        if event == "at button":
            print("sommin")
        if event == "impatient":
            print("sommin")
        if event == "ped_exit":
            #clear impatient event if it hasn't happened yet or just keep it in a skip it later if you want
            print("sommin")
        
        
