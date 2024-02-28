from math import sqrt, log

class Node(object):
    def __init__(self, cell, parent):
        self.cell = cell
        self.parent = parent
        self.n = 0
        self.q = 0
        self.children = {}
        self.outcome = 0

    def add_child(self, child):
        self.children[child.cell] = child

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def calculate_value(self, exploration_factor):
        if self.n == 0:
            if exploration_factor == 0:
                return 0
            else:
                return float('inf')
        else:
            return self.q / self.n + exploration_factor * sqrt(log(self.parent.n) / self.n)
        
    def __eq__(self, other):
        if self.cell == other.cell:
            return True
        return False