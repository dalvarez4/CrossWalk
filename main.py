import car
import ped
import events
blockLength=330
crosswalkWidth=24
streetWidth=46




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    car1=car.car(20)
    print(car1.carLength)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''loop idea'''
ped_delay = 0
car_delay = 0
max_cars = 200
cars_passed = 0
event_list = events.event_list()
#spawn cars and first ped
event_list.insert(events.event("ped_spawn", ped.Uniform()))
peds = {}
time = 0
last_time = 0
#start on fresh green
last_signal = "R"
last_signal_time = 0
#when will the next green light end
sec_until_green_exp = 35
while cars_passed < max_cars:
    event = event_list.next()
    sec_until_green_exp = sec_until_green_exp - (time - last_time)
    if event.name == 'ped_spawn':
        curr_ped = ped.ped(time, event, event_list, len(peds))
        event_list.insert(events.ped_event("at_button", curr_ped.button_time, curr_ped.id))
        peds[len(peds) + 1] = curr_ped
        event_list.insert(events.event("ped_spawn", ped.Uniform() + time))
    elif event.name == "ped_exit":
        ped_delay += peds.pop(event.id).update(event.name, time, event_list)
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
    
    
    

