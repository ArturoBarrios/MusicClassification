import heapq

class Maxheap():
    """
    Python's standard library implementation of heap is a min-heap.
    This is a simple wrapper to convert it to max-heap, by changing the sign.
    """

    def __init__(self, items, values):
        """ Initialize the heap with a set of items and corresponding priorities. """
        self.heap = [(-val, i) for val, i in zip(values, items)]
        heapq.heapify(self.heap)

    def push(self, item, priority):
        """ Add a new item to the heap with priority. """
        heapq.heappush(self.heap, (-priority, item))

    def peekMaxItem(self):
        """ Look at the top item on the heap. """
        return self.heap[0][1]

    def peekMaxValue(self):
        """ Look at the top value on the heap. """
        return -self.heap[0][0]

    def pop(self):
        """ Remove and return top item on the heap. """
        return heapq.heappop(self.heap)[1]

    def allItems(self):
        """ Get a (not necessarily ordered) list of the items in the heap. """
        return [item for val, item in self.heap]

    def counts(self):
        """ Count the number of each item in the heap. """
        counts = {}
        for val, item in self.heap:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1

        # Return a list of pairs, with an item and the corresponding count
        # Note that sorting this will result in the most/least frequent items at the front
        return [(counts[item], item) for item in counts]

    def __len__(self):
        return len(self.heap)

