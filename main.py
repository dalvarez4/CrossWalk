#!/usr/bin/env python3

import numpy as np
import car
import ped
import events
import sys
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
        newSTD=np.sqrt(oldSTD**2+(N*(oldMean-newPoint)**2-(N+1)*oldSTD**2)/(N+1)**2)
        return newSTD


    def setLight4Cars(time):
        for carro in cars:
            carro.updateYellowTime(time)
    def lightHandles(lightColor,time,car_delay_sigma,car_delay_mu,cars_passed):
        for carro in cars:
            carro.carStates(lightColor,time,cars_passed)
            if carro.carExit:
                car_delay_sigma = updateSTD(car_delay_mu, car_delay_sigma, carro.carExit, cars_passed)
                car_delay_mu = updateMean(car_delay_mu, carro.carExit, cars_passed)
                cars.remove(carro)
                cars_passed+=1
        return car_delay_mu,car_delay_sigma,cars_passed








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

    car_arr, car_speed = map(lambda x: float(x), auto_dist.readline().split(' '))
    ped_arr, ped_speed = map(lambda x: float(x), ped_dist.readline().split(' '))

    '''loop idea'''


    max_cars = 200
    cars_passed = 0
    event_list = events.event_list()
    #spawn cars and first ped
    event_list.insert(events.event("ped_spawn", ped.Exponential(2 * lambda_p, x = ped_arr)))
    event_list.insert(events.event("car_spawn",ped.Exponential(2*lambda_c, x = car_arr)))
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
        event = event_list.next()
        time = event.arrival_time
        sec_until_green_exp = sec_until_green_exp - (time - last_time)
        if event.name == 'ped_spawn':
            curr_ped = ped.ped(time, event, event_list, total_peds, ped.Uniform(x = ped_speed), button_dist)
            event_list.insert(events.ped_event("at_button", curr_ped.button_time, curr_ped.id))
            peds[total_peds] = curr_ped
            total_peds += 1
            if total_peds < arrivals:
                ped_arr, ped_speed = map(float, ped_dist.readline().split(' '))
                event_list.insert(events.event("ped_spawn", ped.Exponential(lambda_p / 60 / 2, x = ped_arr) + time))
        elif event.name == "ped_exit":
            peds_crossed += 1
            new_delay = peds.pop(event.id).update(event.name, time, event_list)
            #ped_delay_mu = ped_delay_mu + (1/(peds_crossed)) * (new_delay - ped_delay_mu)
            ped_delay_mu = updateMean(ped_delay_mu,new_delay, peds_crossed)
        elif event.name == "car_spawn":
            curr_car = car.car(ped.Uniform(25, 35, x=car_speed), time)
            cars.append(curr_car)
            total_cars += 1
            if total_cars < arrivals:
                car_arr, car_speed = map(float, auto_dist.readline().split(' '))
                event_list.insert(events.event("car_spawn", ped.Exponential(lambda_c / 60 / 2, x = car_arr) + time))
        elif event.name == "r_exp":
            sec_until_green_exp = 35
            car_delay_mu,car_delay_sigma,cars_passed=lightHandles("Red",time,car_delay_sigma,car_delay_mu,cars_passed)
        elif event.name == "y_exp":

            car_delay_mu,car_delay_sigma,cars_passed=lightHandles("Yellow",time,car_delay_sigma,car_delay_mu,cars_passed)
            #stranded peds are waiting for the next red not the current one
            sec_until_green_exp == 18 + 35
        elif event.name == "g_exp":
            setLight4Cars(time)
            car_delay_mu,car_delay_sigma,cars_passed=lightHandles("Green",time,car_delay_sigma,car_delay_mu,cars_passed)
            #pushed button during yellow light
            sec_until_green_exp == 0
        #check if its a single ped event otherwise
        #update peds in the order they arrived
        if isinstance(event, events.ped_event):
            if event.id in peds.keys():
                peds[event.id].update(event.name, time, event_list, signal_left = sec_until_green_exp)
        elif len(list(peds.keys())) > 0:
            keys = list(peds.keys())
            keys.sort()
            for key in keys:
                event_list = peds[key].update(event.name, time, event_list, signal_left = sec_until_green_exp)
    print(ped_delay_mu)
    #print("OUTPUT ",)
    exit(0)



