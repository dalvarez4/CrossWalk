#!/usr/bin/env python3

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    car1=car.car(20)
    print(car1.carLength)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

    #check arguments
    if len(sys.argv) != 5:
        exit("most supply 4 arguments, number of arrivals, and 3 trace files of Uniform(0,1) distributions")
    try:
        arrivals = int(sys.argv[1])
    except:
        exit("Invalid number of arrivals")
    try:
        auto_dist = open(sys.argv[3], 'r')
    except:
        exit("Invalid auto file path")
    try:
        ped_dist = open(sys.argv[4], 'r')
    except:
        exit("Invalid pedestrian file path")
    try:
        button_dist = open(sys.argv[5], 'r')
    except:
        exit("Invalid button press file path")

    
    car_arr, car_speed = map(float, auto_dist.readline().split(' '))
    ped_arr, ped_speed = map(float, ped_dist.readline().split(' '))

    '''loop idea'''
    ped_delay_mu = 0
    car_delay = 0
    max_cars = 200
    cars_passed = 0
    event_list = events.event_list()
    #spawn cars and first ped
    event_list.insert(events.event("ped_spawn", ped.Exponential(2 * lambda_p, x = ped_arr)))
    peds = {}
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
        sec_until_green_exp = sec_until_green_exp - (time - last_time)
        if event.name == 'ped_spawn':
            curr_ped = ped.ped(time, event, event_list, total_peds, ped.Uniform(x = ped_speed))
            event_list.insert(events.ped_event("at_button", curr_ped.button_time, curr_ped.id))
            peds[total_peds] = curr_ped
            total_peds += 1
            if total_peds < arrivals:
                ped_arr, ped_speed = map(float, ped_dist.readline().split(' '))
                event_list.insert(events.event("ped_spawn", ped.Exponential(lambda_p / 60 / 2, x = ped_arr) + time))
        elif event.name == "ped_exit":
            peds_crossed += 1
            new_delay = peds.pop(event.id).update(event.name, time, event_list)
            ped_delay_mu = ped_delay_mu + (1/(peds_crossed)) * (new_delay - ped_delay_mu)
        elif event.name == "r_exp":
            sec_until_green_exp = 35
        elif event.name == "y_exp":
            #stranded peds are waiting for the next red not the current one
            sec_until_green_exp == 18 + 35
        elif event.name == "g_exp":
            #pushed button during yellow light
            sec_until_green_exp == 0
        #check if its a single ped event otherwise
        #update peds in the order they arrived
        if isinstance(event, events.ped_event):
            if peds.has_key(event.id):
                peds[event.id].update(event.name, time, event_list, signal_left = sec_until_green_exp)
        else:
            for key in peds.keys.sort():
                event_list = peds[key].update(event.name, time, event_list, signal_left = sec_until_green_exp)
    print(ped_delay_mu)
    exit(0)



