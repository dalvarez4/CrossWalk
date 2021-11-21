import numpy as np

class event:
    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time
    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

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
        self.heap = np.empty(50, dtype=event)
        self.size_inc = 10
        self.to_insert = 0
    def child_l(self, i):
        return 2*i + 1
    def child_r(self, i):
        return 2*i + 2
    def parent(self, i):
        return np.floor((i - 1) / 2)

    def insert(self, event):
        #check first if array needs to padded
        if self.to_insert == self.heap.shape:
            self.heap = np.pad(self.heap, [(0, self.size_inc)], mode='constant', constant_values = None)
        self.heap[self.to_insert] = event
        index = self.to_insert
        self.to_insert += 1
        parent_index = self.parent(index)
        while self.heap[parent_index] < self.heap[index]:
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
        while self.heap[index] > self.heap[l] or self.heap[index] > self.heap[r]:
            to_swap = None
            if self.heap[l] < self.heap[r]:
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

#class event_list:
#    tail = None
#    def __init__(self, event):
#        self.head = node(event)
#        self.tail = self.head
#    def insert(self, event):
#        to_insert = node(event)
#
#
#
#    def next(self):
#        to_return = self.head.event
#        to_move = self.tail
#        #new_tail = self.tail.parent
#        #if new_tail.r != None:
#        #    self.tail = new_tail.l
#        #else:
#        #    self.tail = new_tail
#        to_move.parent = None
#        new_head = None
#        if self.head.l < self.head.r:
#            new_head = self.head.l
#            self.head.r.parent = new_head
#            to_move.l = new_head.l
#            to_move.r = new_head.r
#            to_move.parent = new_head
#            new_head.r = self.head.r
#            new_head.l = to_move
#        else:
#            new_head = self.head.r
#            self.head.l.parent = new_head
#            to_move.l = new_head.l
#            to_move.r = new_head.r
#            to_move.parent = new_head
#            new_head.l = self.head.l
#            new_head.r = to_move
#        self.head = new_head
#        while to_move.r < to_move or to_move.l < to_move:
#            new_parent = None
#            sibling = None
#            grandparent = None
#            grandchild_l = None
#            grandchild_r = None
#            sibling_side = None
#            if to_move.l < to_move.r:
#                new_parent = to_move.l
#                sibling = to_move.r
#                grandparent = to_move.parent
#                grandchild_l = new_parent.l
#                grandchild_r = new_parent.r
#                sibling_side = 'r'
#            else:
#                new_parent = to_move.r
#                sibling = to_move.l
#                grandparent = to_move.parent
#                grandchild_l = new_parent.l
#                grandchild_r = new_parent.r
#                sibling_side = 'l'
#            new_parent.parent = grandparent
#            to_move.parent = new_parent
#            sibling.parent = new_parent
#            if sibling_side == 'r':
#                new_parent.r = sibling
#                new_parent.l = to_move
#            else:
#                new_parent.r = to_move
#                new_parent.l = sibling
#            to_move.l = grandchild_l
#            to_move.r = grandchild_r
#            if to_move.r != None:
#                to_move.r.parent = to_move
#            if to_move.l != None:
#                to_move.l.parent = to_move
#        #find the new tail
#        '''Find the new tail'''
#
#        return to_return
#                

        #find the new tail
            

        


    
#test_event = event("test", 0)

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