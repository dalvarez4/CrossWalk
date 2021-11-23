import numpy as np

class event:
    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time
    def __lt__(self, other):
        return self.arrival_time < other.arrival_time
    def __gt__(self, other):
        return self.arrival_time > other.arrival_time

    def __str__(self):
        return f'({self.name}, {self.arrival_time})'

class ped_event(event):
    def __init__(self, name, arrival_time, id):
        super().__init__(name, arrival_time)
        self.id = id

class node:
    def __init__(self, event, l = None, r = None, parent = None):
        self.event = event
        self.l = l
        self.r = r
        self.parent = parent
    def add_l(self, node):
        self.l = node
    def add_r(self, node):
        self.r = node
    def __lt__(self, other):
        return self.event < other.event

class event_list:

    count_iter = 0

    def __init__(self):
        self.heap = np.empty(10, dtype=event)
        self.size_inc = 10
        self.to_insert = 0
    def child_l(self, i):
        return 2*i + 1
    def child_r(self, i):
        return 2*i + 2
    def parent(self, i):
        return int(np.floor((i - 1) / 2))

    def length(self):
        return len(self.heap)

    def insert(self, event):
        #check first if array needs to padded
        if self.to_insert == self.heap.shape[0]:
            self.heap = np.pad(self.heap, [(0, self.size_inc)], mode='constant', constant_values = None)
        self.heap[self.to_insert] = event
        index = self.to_insert
        self.to_insert += 1
        parent_index = self.parent(index)
        while parent_index >= 0 and self.heap[parent_index] > self.heap[index]:
            #print(self.heap[index], self.heap[parent_index])
            event_list.count_iter += 1
            #print(event_list.count_iter)
            to_swap = self.heap[parent_index]
            self.heap[parent_index] = self.heap[index]
            self.heap[index] = to_swap
            index = parent_index
            parent_index = self.parent(index)
    def next(self):
        to_return = self.heap[0]
        self.heap[0] = self.heap[self.to_insert - 1]
        self.to_insert -= 1
        self.heap[self.to_insert] = None
        index = 0
        r = self.child_r(index)
        l = self.child_l(index)
        while (l < len(self.heap) and self.heap[l] != None and self.heap[index] > self.heap[l]) or (r < len(self.heap) and self.heap[r] != None and self.heap[index] > self.heap[r]):
            event_list.count_iter += 1
            to_swap = None
            if self.heap[r] == None or self.heap[l] < self.heap[r]:
                to_swap = l
            else:
                to_swap = r
            temp = self.heap[to_swap]
            self.heap[to_swap] = self.heap[index]
            self.heap[index] = temp
            index = to_swap
            l = self.child_l(index)
            r = self.child_r(index)
        return to_return
    def __str__(self):
        s = '['
        for event in self.heap:
            s += f'{event.__str__()}, '
        s = s[:-2]
        s += ']'
        return s
            
    
#test_event = event("test", 5)

#orig = node(test_event, 'l', 'r', 'p')
#maybe_copy = orig
#maybe_copy.parent = None

#print(orig.parent, maybe_copy.parent)


#heap = np.empty(50, dtype=node)
#print(heap)

#print(np.floor((3 - 1) / 2))
#test_array = np.array([1,2,3,4,5])
#print(np.pad(test_array, [(0, 3)], mode = 'constant', constant_values = -1))

#event_array = np.array([test_event, test_event, test_event], dtype = event)
#print(np.pad(event_array, [(0, 3)], mode = 'constant', constant_values = None))

#test_event = event("test", Uniform(0, 50))
#test_list = event_list()
#test_list.insert(test_event)
#print(test_list)
#events = [event("test", 20), event("test", 30), event("test", 60), event("test", 20), event("test", 1)]

import random
def Uniform(a = 2.6,b = 4.1, x = -1):
    if x == -1:
        x = random.random()
    return a + (b - a) * x


num_runs = 1000


num = 500
avg_iter = 0

all_inserts = []
all_nexts = []

inserts = []
nexts = []
elements = []
#for event in events:
for run in range(5, num_runs):
    #elements.append(run)
    test_event = event("test", Uniform(0, 50))
    test_list = event_list()
    test_list.insert(test_event)
    print(run)
    inserts = []
    nexts = []
    for x in range(5, num):
        event_list.count_iter = 0
        test_list.insert(event("test", Uniform(0, 50)))
        #avg_iter = avg_iter + (1/(x + 1)) * (event_list.count_iter - avg_iter)        
        inserts.append(event_list.count_iter)
        #print(event_list.count_iter)
        #print(test_list)
    #
    all_inserts.append(inserts)

    avg_iter = 0
    for x in range(5, num):
        event_list.count_iter = 0
        test_list.next()
        #avg_iter = avg_iter + (1/(x + 1)) * (event_list.count_iter - avg_iter)
        nexts.append(event_list.count_iter)
    #    print(test_list)
    all_nexts.append(nexts)

#print(len(inserts), len(nexts), len(elements))
avg_inserts = []
avg_nexts = []

for x in range(5, num):
    x = x - 5
    avg_insert = 0
    avg_next = 0
    for i in range(len(all_inserts)):
        #print(all_inserts[i], x, all_inserts[i][x])
        avg_insert = avg_insert + (1/(i + 1)) * (all_inserts[i][x] - avg_insert)
        avg_next = avg_next + (1/(i + 1)) * (all_nexts[i][x] - avg_next)
    avg_inserts.append(avg_insert)
    avg_nexts.append(avg_next)


import matplotlib.pyplot as plt

elements = [x for x in range(5, num)]

plt.scatter(elements, avg_inserts)

plt.show()

plt.scatter(elements, avg_nexts)

plt.show()
