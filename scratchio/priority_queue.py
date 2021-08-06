from collections import namedtuple

from .min_heap import MinHeap

PrioritizedItem = namedtuple("PrioritizedItem", ["priority", "sequence", "item"])



class PriorityQueue:
    sequence = 0

    def __init__(self):
        self.items = MinHeap()

    def is_empty(self):
        """Checks whether the queue has no items."""

        return self.items.is_empty()

    def peek(self):
        if not self.is_empty():
            return self.items[0]

    def insert_item_with_priority(self, item, priority):
        """Adds an item to the queue with an associated priority."""

        self.sequence += 1
        self.items.push(PrioritizedItem(priority, self.sequence, item))

    def pull_highest_pritority_item(self):
        """Removes the item from the queue that has the highest priority, and returns it."""

        hp_item = self.items.pop()
        return hp_item.item
