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
#test_event = event("test", 5)
#test_list = event_list()
#test_list.insert(test_event)
#print(test_list)
#events = [event("test", 20), event("test", 30), event("test", 60), event("test", 20), event("test", 1)]
#for event in events:
#    test_list.insert(event)
#    print(test_list)
#
#for event in events:
#    test_list.next()
#    print(test_list)
