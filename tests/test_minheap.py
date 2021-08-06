import random

from scratchio.min_heap import MinHeap


def check_invariant(heap):
    # Check the heap invariant.
    for pos, item in enumerate(heap):
        if pos:  # pos 0 has no parent
            parentpos = (pos - 1) // 2
            assert heap[parentpos] <= item


def test_push_pop():
    # 1) Push 256 random numbers and pop them off, verifying all's OK.
    heap = MinHeap()
    data = []
    check_invariant(heap)
    for i in range(256):
        item = random.random()
        data.append(item)
        heap.push(item)
        check_invariant(heap)

    results = []
    while not heap.is_empty():
        item = heap.pop()
        check_invariant(heap)
        results.append(item)

    data_sorted = data[:]
    data_sorted.sort()
    assert data_sorted == results

    # 2) Check that the invariant holds for a sorted array
    check_invariant(results)
