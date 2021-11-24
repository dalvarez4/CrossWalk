import random
import numpy as np
import events
from heapq import heapify, heappush, heappop


def Uniform(a = 2.6,b = 4.1, x = random.random()):
    return a + (b - a) * x

def Exponential(mew, x = random.random()):
    return -mew * np.log(1 - x)



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
def will_press(peds_waiting, pushed, trace, impatient = False, stranded = False):
    if pushed:
        return False
    if impatient:
        return True
    x = float(trace.readline())
    #peds waiting -1?
    if peds_waiting == 0 or stranded:
        return Uniform(0, 16, x) <= 15
    else:
        return Uniform(0, peds_waiting + 1, x) <= peds_waiting

class ped:

    #static class variable so we don't make an enourmous amount of crosswalk events, button will only actually be pressed if no one has pressed it yet for the current cycle
    pushed = False
    #shared amount of peds waiting
    peds_waiting = 0
    #shared amount of peds crossing
    peds_crossing = 0
    #trace values for button presses
    button_trace = []
    #order that peds arrive at button
    #sort by order they WILL arrive at button
    button_arrivals = []

    def __init__(self, time, event, event_list, num_peds, speed, button_trace):
        if ped.button_trace == []:
            ped.button_trace = button_trace
            heapify(ped.button_arrivals)
        #distance until they are at the button
        #unsure what the width of the side streets are, assume side streets are same width as the main street as only one street width is stated
        #have to cross a half block, side street, and another half block to reach the button
        self.button_pos = B/2 + S + B/2
        self.delay_start = None
        #self.speed = Uniform(2.6, 4.1)
        self.speed = speed
        #just gonna worry about spawning on one side for now since peds don't collide
        #might want to worry about the next spawn event in the main loop to ensure that ID's stay unique
        #self.next_ped = time + Exponential(2 * lambda_p)
        self.last_time = time
        #pedestrians spawn across one street and one half block, block width = B, width of street = S
        #calculate time for button event
        self.button_time = (self.button_pos / self.speed) + time
        heappush(ped.button_arrivals, self)
        #event_list.insert(events.ped_event("at_button", self.button_time, self.id))
        self.id = num_peds
        self.walked = False
        self.at_button = False
        self.pos = 0
        self.total_delay = 0
        #need to determine whther or not they will make the walk cycle if there is one
        #add ped_impatiant for one minute after arriving at button
        #newly spaned peds should still be considered for walking? Prolly impossible for them to cross the total distance in time.
        #event_list = self.update(event, time, event_list)
    
    def __lt__(self, other):
        return self.button_time < other.button_time

    def push_button(self, time, event_list, signal_left):
        #assuming cross walk works instantanuosly on a stale (with yellow delay)
        #print(signal_left)
        if(signal_left <= 0):
            heappush(event_list, events.event("g_exp", time))
            heappush(event_list, events.event("y_exp", time + 8))
            heappush(event_list, events.event("r_exp", time + 8 + 18))
        else: 
            heappush(event_list, events.event("g_exp", time + signal_left))
            heappush(event_list, events.event("y_exp", time + signal_left + 8))
            heappush(event_list, events.event("r_exp", time + signal_left + 18))
        return event_list
    
    def update(self, event, time, event_list, signal_left = 0):
        # AUTO_ARRIVAL, PED_ARRIVAL, PED_AT_BUTTON, PED_IMPATIENT, GREEN_EXPIRES, YELLOW_EXPIRES, RED_EXPIRES, AUTO_EXIT and PED_EXIT.
        if not self.at_button:
            self.pos = self.speed * (time - self.last_time) + self.pos
        #if self.pos >= self.button_pos:
        #    self.pos = self.button_pos
        if event == 'y_exp':
            #reset crosswalk status
            ped.pushed = False
            #should be allowed to walk even if not right at button, anywhere within that 24 foot width of the crosswalk
            '''only first 20 pedestrians that can make it will cross determine who is checked as available to cross in main loop'''
            #time they finished crossing if applicable
            crossed_at = None
            #check where the pedestrian currently is
            #button is in the middle of the crosswalk so they just need to be within twelve feet of the button to be at the crosswalk
            if ped.peds_crossing <=20 and (self.at_button or self.button_pos - self.pos <= 12):
                #anyone at the button or at the crosswalk should be allowed to walk
                self.walked = True
                crossed_at = (S / self.speed) + time
            elif ped.peds_crossing <=20 and (self.button_pos - self.pos - 12 + cw_peds) / self.speed <= RED:
                #if they can make it to the crosswalk and also cross within the signal time they can walk
                self.walked = True
                crossed_at = ((self.button_pos - self.pos - 12) / self.speed + S / self.speed) + time

            if self.walked:
                #for peds no longer waiting reduce the count
                ped.peds_waiting -= 1
                ped.peds_crossing += 1
                if ped.button_arrivals[0].id == self.id:
                    heappop(ped.button_arrivals)

                #if can walk add a ped exit event
                heappush(event_list, events.ped_event("ped_exit", crossed_at, self.id))

                #calculate delay if allowed to walk
                if self.delay_start != None:
                    self.total_delay = time - self.delay_start
            elif not self.walked and ped.peds_crossing > 20 and will_press(ped.peds_waiting, ped.pushed, trace = ped.button_trace, stranded=True):
                event_list = self.push_button(time, event_list, signal_left)

        if event == 'r_exp' or event == 'g_exp':
            '''this will be anytime the light is not red'''
            #reset the count of peds that have crossed
            ped.peds_crossing = 0


        if event == "at_button":
            if self.walked:
                #do nothing if already walked
                return event_list
            self.at_button = True
            self.delay_start = time
            #increment the amount of peds waiting
            #add the impatient event after a minute of at the button
            heappush(event_list, events.ped_event("impatient", time + 60, self.id))
            if will_press(ped.peds_waiting, ped.pushed, trace = ped.button_trace):
                event_list = self.push_button(time, event_list, signal_left)
            ped.peds_waiting += 1

        if event == "impatient":
            if self.walked:
                #do nothing if already walked
                return event_list
            if will_press(ped.peds_waiting, ped.pushed, trace = ped.button_trace, impatient=True):
                event_list = self.push_button(time, event_list, signal_left)
        if event == "ped_exit":
            #clear impatient event if it hasn't happened yet or just keep it in a skip it later if you want
            return self.total_delay
        self.last_time = time
        return event_list
#print("test")
#test_event = events.event("test", 5)
#print("worked")
#test_list = events.event_list()
#test_list.insert(test_event)
#print(test_list)
#events = [events.event("test", 20), events.event("test", 30), events.event("test", 60), events.event("test", 20), events.event("test", 1)]
#for event in events:
#    test_list.insert(event)
#    print(test_list)
#
#for event in events:
#    test_list.next()
#    print(test_list)


#test_list = events.event_list()
#test_ped = ped(0, 'spawn', test_list, 0, .5, 'filler')
#test_list = test_ped.update('y_exp', 100000, test_list, signal_left = 0)
#print(test_ped.speed, test_ped.pos, test_ped.button_pos)
#print(test_list)