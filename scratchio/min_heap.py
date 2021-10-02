from collections import deque


class MinHeap:
    """
    In computer science, a heap is a specialized tree-based data structure which is essentially a
    tree that satisfies the heap property: in a min heap, for any given node C, if P is a parent node of C,
    then the key (the value) of P is less than or equal to the key of C.

    The node at the "top" of the heap (with no parents) is called the root node.

    Heaps are usually implemented with an array, as follows:
    - Each element in the array represents a node of the heap, and
    - The parent / child relationship is defined implicitly by the elements' indices in the array.

    In the array, the first index contains the root element.
    The next two indices of the array contain the root's children.
    The next four indices contain the four children of the root's two child nodes, and so on.
    Therefore, given a node at index i, its children are at indices 2i + 1 and 2i + 2, and its parent is at index ⌊(i-1)/2⌋.

    After an element is inserted into or deleted from a heap, the heap property may be violated,
    and the heap must be re-balanced by swapping elements within the array.

    Balancing a heap is done by sift-up or sift-down operations (swapping elements which are out of order).

    Source: Wikipedia.
    """

    def __init__(self):
        self.items = deque()

    def __iter__(self):
        return (item for item in self.items)

    def __getitem__(self, item):
        return self.items[item]

    def is_empty(self):
        """Returns True if the heap is empty, False otherwise."""
        return not bool(self.items)

    def peek(self):
        """Finds the minimum item of the heap."""

        return self.items[0] if self.items else None

    def push(self, item):
        """Adds a new item to the heap."""

        self.items.append(item)

        new_item_pos = len(self.items) - 1
        parent_pos = (new_item_pos - 1) // 2
        while parent_pos >= 0 and self.items[new_item_pos] < self.items[parent_pos]:
            self.items[new_item_pos], self.items[parent_pos] = (
                self.items[parent_pos],
                self.items[new_item_pos],
            )
            new_item_pos = parent_pos
            parent_pos = (parent_pos - 1) // 2

    def pop(self):
        """Returns the node of  minimum value from a min heap after removing it from the heap"""

        popped = self.items.popleft()
        n = len(self.items)
        if n == 0:
            return popped

        self.items.appendleft(self.items.pop())

        last_item_pos = 0
        child_pos = 2 * last_item_pos + 1
        while child_pos < n:
            right_child_pos = child_pos + 1
            if (
                right_child_pos < n
                and self.items[right_child_pos] < self.items[child_pos]
            ):
                child_pos = right_child_pos

            if self.items[last_item_pos] <= self.items[child_pos]:
                break

            self.items[last_item_pos], self.items[child_pos] = (
                self.items[child_pos],
                self.items[last_item_pos],
            )

            last_item_pos = child_pos
            child_pos = 2 * child_pos + 1

        return popped
