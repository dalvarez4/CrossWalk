import random
import numpy as np
import events
from heapq import heapify, heappush, heappop


def Uniform(a = 2.6,b = 4.1, x = random.random()):
    return a + (b - a) * x

def Exponential(mew, x = random.random()):
    return -mew * np.log(1 - x)

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
    #position of the button
    button_pos = B/2 + S + B/2

    def __init__(self, time, num_peds, speed, button_trace):
        #initialize the trace file to use for calculating button press probabilities, should be used regardless of whther or not a cycle is already queued I think
        if ped.button_trace == []:
            ped.button_trace = button_trace
            heapify(ped.button_arrivals)
        #the time the ped starts waiting at the button, stays None if they make an early cycle
        self.delay_start = None
        #speed of the pedestrian
        self.speed = speed
        #the last time the pedestrian moved
        self.last_time = time
        #whether or not the pedestrian is left behind during a cycle
        self.stranded = False
        #time the ped will reach the signal button
        self.button_time = (ped.button_pos / self.speed) + time
        #add them to the heap, should be sorted by their button press time
        heappush(ped.button_arrivals, self)
        #unique identifier for the current ped
        self.id = num_peds
        #whether or not the ped has already walked across the cross walk
        self.walked = False
        #whether or not the ped is at the button
        self.at_button = False
        #curent position of the ped, or at least current as of self.last_time
        self.pos = 0
        #the calculated total delay of the ped
        self.total_delay = 0
        #theoretical minimum crossing time
        self.theory_cross = (ped.button_pos + cw_peds) / self.speed + time
    
    def __lt__(self, other):
        return self.button_time < other.button_time

    def push_button(self, time, event_list, signal_left):
        #a ped has pushed of the button, don't want a bunch of stacked walked signals
        ped.pushed = True
        #assuming cross walk works instantanuosly on a stale green (with yellow delay)
        #negative signal time indicates the signal could have changed earlier in the simulation but had no reason to
        if(signal_left <= 0):
            heappush(event_list, events.event("g_exp", time))
            heappush(event_list, events.event("y_exp", time + 8))
            heappush(event_list, events.event("r_exp", time + 8 + 18))
        else: 
            heappush(event_list, events.event("g_exp", time + signal_left))
            heappush(event_list, events.event("y_exp", time + signal_left + 8))
            heappush(event_list, events.event("r_exp", time + signal_left + 18))
        return event_list
    

    def walk_signal(self, time, event_list, signal_left):
        #either crosses or is stranded
        '''should be called in order of arrival at the button'''
        #calculate new posistion of pedestrian if not already at the button
        if self.pos != ped.button_pos:
            self.pos = (time-self.last_time) * self.speed + self.pos
        self.last_time = time
        #were waiting and then crossed
        if ped.peds_crossing <= 20 and self.at_button:
            #cross
            self.crossing(time)
        #crossed before reaching the button
        elif ped.peds_crossing <= 20 and ((ped.button_pos - self.pos + cw_peds) / self.speed <= RED):
            #cross without getting to the button
            self.crossing(time)
        #strandedonly if at button
        #need to make sure I account for people that WILL be stranded ie, they will walk up to the light during the signal and not make it
        #this will not negate their normal button arrival chance at pressing, ie they will have to chances to press
        elif ped.peds_crossing > 20 and (((ped.button_pos - self.pos + cw_peds) / self.speed <= RED) or self.at_button):
            self.stranded = True
            #if they pushed the button make em push the button
            if self.will_press():
                event_list = self.push_button(time, event_list, signal_left)
        
        return event_list

    def impatient_press(self, time, event_list, signal_left):
        #if they already walked don't do anything
        if self.walked:
            return event_list
        #is just impatient, deal with it, push the damn button
        event_list = self.push_button(time, event_list, signal_left)
        return event_list
    
    def at_signal(self, time, event_list, signal_left):
        '''try to account for when they get there during signal plus additional press on being stranded? but also thats stupid like why would a pedestrian push the signal, which wouldnt do anything, if its already on'''
        #skipped the button entirely
        if self.walked:
            return event_list
        #is at the button
        #pedestrian is now not moving and is waiting
        self.delay_start = time
        ped.peds_waiting += 1
        self.at_button = True
        #if they push the button push the button
        if self.will_press():
            event_list = self.push_button(time, event_list, signal_left)

        return event_list

    def crossing(self, time):
        '''should only be called from within walk signal for peds who can make it across in the current cycle'''
        '''peds_crossing should be updated outside of class once all peds have been iterated through'''
        ped.peds_crossing += 1
        self.walked = True
        if self.at_button:
           ped.peds_waiting -= 1
        '''value to be grabbed'''
        #if they never waited they had no delay
        if self.delay_start == None:
            self.total_delay = 0
        #otherwise calculate the difference between when they started waiting and when they crossed
        else:
            self.total_delay = time - self.delay_start
        #if the ped crossed remove them from the waiting heap make sure they only pop themselves
        #assert heappop(ped.button_arrivals).id == self.id
        #alternate method for calculating delay although hypothetically the same
        distance_left = cw_peds
        #if not self.at_button:
        #    distance_left += (ped.button_pos - self.pos)
        #self.total_delay = (distance_left/self.speed) + time - self.theory_cross

        
        
         
        
    def will_press(self):
        '''never called directly'''
        if ped.pushed:
            return False
        x = float(ped.button_trace.readline())
        #peds waiting -1?
        if ped.peds_waiting == 0 or self.stranded:
            return Uniform(0, 16, x) <= 15
        else:
            return Uniform(0, ped.peds_waiting + 1, x) <= ped.peds_waiting