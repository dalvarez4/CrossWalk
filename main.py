#!/usr/bin/env python3

import carNew
import ped
import events
import sys
from heapq import heapify, heappush, heappop


blockLength=330
crosswalkWidth=24
streetWidth=46

arrivals = 0
auto_dist = []
ped_dist = []
button_dist = []

lambda_p = 3
lambda_c = 4

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #meta events to keep track of
    ped_delay_mu = 0
    car_delay_mu = 0
    ped_delay_sigma = 0
    car_delay_sigma = 0
    #functions to help with sim

        #pass Standard deviation first then update the mean
    def updateMean(oldMean,newPoint,N):
        newMean=oldMean+1/(N+1)*(newPoint-oldMean)
        return newMean
    def updateSTD(oldMean,oldSTD,newPoint,N):
        newSTD=oldSTD+(N/(N+1))*(newPoint-oldMean)**2
        return newSTD











# See PyCharm help at https://www.jetbrains.com/help/pycharm/

    #check arguments
    if len(sys.argv) != 5:
        exit("most supply 4 arguments, number of arrivals, and 3 trace files of Uniform(0,1) distributions")
    try:
        arrivals = int(sys.argv[1])
    except:
        exit("Invalid number of arrivals")
    try:
        auto_dist = open(sys.argv[2], 'r')
    except:
        exit("Invalid auto file path")
    try:
        ped_dist = open(sys.argv[3], 'r')
    except:
        exit("Invalid pedestrian file path")
    try:
        button_dist = open(sys.argv[4], 'r')
    except:
        exit("Invalid button press file path")

    try:
        car_arr, car_speed = float(auto_dist.readline()), float(auto_dist.readline())
    except:
        exit("Auto trace ended prematurely")
    try:
        ped_arr, ped_speed = float(ped_dist.readline()), float(ped_dist.readline())
    except:
        exit("Pedestrian trace ended prematurely")

    '''loop idea'''


    max_cars = 200
    cars_passed = 0
    #event_list = events.event_list()
    #spawn cars and first ped
    #event_list.insert(events.event("ped_spawn", ped.Exponential(2 * lambda_p / 60, x = ped_arr)))
    #event_list.insert(events.event("car_spawn",ped.Exponential(2*lambda_c / 60, x = car_arr)))
    event_list = []
    heapify(event_list)
    heappush(event_list, events.event("ped_spawn", ped.Exponential(60/(2 * lambda_p), x = ped_arr)))
    heappush(event_list, events.event("car_spawn",ped.Exponential(60/(2 * lambda_c), x = car_arr)))
    peds = {}
    cars=[]
    time = 0
    last_time = 0
    #start on fresh green
    last_signal = "R"
    last_signal_time = 0
    #when will the next green light end
    sec_until_green_exp = 35
    peds_crossed = 0
    total_peds = 0
    total_cars = 0
    while cars_passed < arrivals and peds_crossed < arrivals:
        event = heappop(event_list)
        time = event.arrival_time
        sec_until_green_exp = sec_until_green_exp - (time - last_time)
        if event.name == 'ped_spawn':
            curr_ped = ped.ped(time, total_peds, ped.Uniform(x = ped_speed), button_dist)
            #print(curr_ped.speed)
            heappush(event_list, events.ped_event("at_button", curr_ped.button_time, curr_ped.id))
            #heappush(event_list, events.ped_event("impatient", curr_ped.button_time + 60, curr_ped.id))
            peds[total_peds] = curr_ped
            total_peds += 1
            if total_peds < arrivals:
                try:
                    ped_arr, ped_speed = float(ped_dist.readline()), float(ped_dist.readline())
                except:
                    exit("Pedestrian trace ended prematurely")
                heappush(event_list, events.event("ped_spawn", ped.Exponential(60 / (2*lambda_p), x = ped_arr) + time))

        #elif event.name == "ped_exit":
        #    peds_crossed += 1
        #    new_delay = peds.pop(event.id).update(event.name, time, event_list)
        #    #ped_delay_mu = ped_delay_mu + (1/(peds_crossed)) * (new_delay - ped_delay_mu)
        #    ped_delay_mu = updateMean(ped_delay_mu,new_delay, peds_crossed)
        elif event.name == "car_spawn":
            curr_car = carNew.car(ped.Uniform(25, 35, x=car_speed), time)

            #changes
            heappush(event_list, events.event("car_despawn", curr_car.getExitTime()))

            cars.append(curr_car)

            total_cars += 1
            if total_cars < arrivals:
                try:
                    car_arr, car_speed = float(auto_dist.readline()), float(auto_dist.readline())
                except:
                    exit("Auto trace ended prematurely")
                heappush(event_list, events.event("car_spawn", ped.Exponential(60 / (2*lambda_c), x = car_arr) + time))
                #changes
        elif event.name=="car_despawn":

            for carro in cars:
                if carro.getExitTime()<time+0.001 and carro.getExitTime()>time-0.001:
                    car_delay_sigma=updateSTD(car_delay_mu,car_delay_sigma,carro.checkDelay(),cars_passed)
                    car_delay_mu=updateMean(car_delay_mu,carro.checkDelay(),cars_passed)
                    cars_passed+=1
                    cars.remove(carro)


        elif event.name == "r_exp":
            ped.ped.last_sig = "Red"
            ped.ped.last_sig_end = time

            #reset the amount of peds crossing
            ped.ped.peds_crossing = 0
            #ready for a new signal press
            #ped.ped.pushed = False
            sec_until_green_exp = 35
            #changes
            for carro in cars:
                carro.runsRedLight(time)


        elif event.name == "y_exp":
            sec_until_green_exp = 18 + 35
            ped.ped.last_sig = "Yellow"
            ped.ped.last_sig_end = time



            #ready for a new signal press
            ped.ped.pushed = False
            #make a copy of the list so it isnt affected by changes to the heap made during the crossing
            waiting_peds = ped.ped.button_arrivals.copy()
            still_waiting = []
            for x in range(len(ped.ped.button_arrivals)):
                #print(pedestrian.id)
                pedestrian = heappop(waiting_peds)
                event_list = pedestrian.walk_signal(time, event_list, sec_until_green_exp)
                if pedestrian.walked:
                    #update the mean
                    ped_delay_mu = updateMean(ped_delay_mu, pedestrian.total_delay, peds_crossed)
                    #update the amount that have crossed
                    peds_crossed += 1
                    #remove from the dict of active peds
                    peds.pop(pedestrian.id)
                else:
                    #keep them in the list
                    still_waiting.append(pedestrian)
            #make new heap with remaining peds
            ped.ped.button_arrivals = still_waiting
            heapify(ped.ped.button_arrivals)

            #stranded peds are waiting for the next red not the current one
        elif event.name == "g_exp":
            ped.ped.last_sig = "Green"
            ped.ped.last_sig_end = time

            #pushed button during yellow light
            sec_until_green_exp = 35 + 18 + 8
        elif event.name == "at_button":
            if event.id in peds.keys():
                event_list = peds[event.id].at_signal(time, event_list, sec_until_green_exp)
        elif event.name == "impatient":
            if event.id in peds.keys():
                event_list = peds[event.id].impatient_press(time, event_list, sec_until_green_exp)
        last_time = time
        #check if its a single ped event otherwise
        #update peds in the order they arrived
        #if isinstance(event, events.ped_event):
        #    if event.id in peds.keys():
        #        peds[event.id].update(event.name, time, event_list, signal_left = sec_until_green_exp)
        #elif len(ped.ped.button_arrivals) > 0:
        #    '''need to check the order that they make it to the button, not spawn in '''
        #    #for key in keys:
            #    event_list = peds[key].update(event.name, time, event_list, signal_left = sec_until_green_exp)
        #    heap_copy = ped.ped.button_arrivals.copy()
        #    for pedestrian in heap_copy:
        #        event_list = pedestrian.update(event.name, time, event_list, signal_left = sec_until_green_exp)

    print(f"OUTPUT Average Car Delay {car_delay_mu} Car Delay Standard Deviation {car_delay_sigma/arrivals} Average Pedestrian Delay {ped_delay_mu}")
    #print("OUTPUT ",)
    exit(0)



