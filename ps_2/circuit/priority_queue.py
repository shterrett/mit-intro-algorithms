import pdb

class PriorityQueue:
  """Array-based priority queue implementation."""
  def __init__(self):
    """Initially empty priority queue."""
    self.queue = []
    self.heap_size = 0

  def __len__(self):
    # Number of elements in the queue.
    return len(self.queue)

  def __heap_index(self, i):
    return i + 1

  def __array_index(self, i):
    return i - 1

  def __heap_parent(self, i):
    return int(i / 2)

  def __heap_left(self, i):
    return 2 * i

  def __heap_right(self, i):
    return 2 * i + 1

  def __heap_exchange(self, loc_1, loc_2):
    loc_1_value = self.__heap_value(loc_1)
    loc_2_value = self.__heap_value(loc_2)
    self.__set_heap_value(loc_1, loc_2_value)
    self.__set_heap_value(loc_2, loc_1_value)

  def __heap_value(self, heap_index):
    return self.queue[self.__array_index(heap_index)]

  def __set_heap_value(self, heap_index, heap_value):
    self.queue[self.__array_index(heap_index)] = heap_value

  def __min_heapify(self, heap_index):
    """Restores min heap property at array-index i"""
    def smaller_than(first, second):
      return self.__heap_value(first) < self.__heap_value(second)

    smallest = heap_index
    while True:
      current = smallest
      left = self.__heap_left(current)
      right = self.__heap_right(current)
      if left <= self.heap_size and smaller_than(left, current):
        smallest = left
      if right <= self.heap_size and smaller_than(right, smallest):
        smallest = right
      if smallest != current:
        self.__heap_exchange(smallest, current)
      else:
        break


  def __heap_decrease_key(self, heap_index):
    current = heap_index
    parent = self.__heap_parent(current)
    while current > 1 and self.__heap_value(parent) > self.__heap_value(current):
      self.__heap_exchange(current, parent)
      current = parent
      parent = self.__heap_parent(current)

  def append(self, key):
    """Inserts an element in the priority queue."""
    self.heap_size += 1
    self.queue.append(key)
    self.__heap_decrease_key(self.heap_size)

  def min(self):
    """The smallest element in the queue."""
    return self.queue[0]

  def pop(self):
    """Removes the minimum element in the queue.

    Returns:
        The value of the removed element.
    """
    if self.heap_size < 1:
      raise Exception('Heap Underflow')
    min_val = self.queue[0]
    self.__set_heap_value(1, self.__heap_value(self.heap_size))
    self.heap_size -= 1
    self.queue.pop()
    self.__min_heapify(self.__heap_index(0))
    return min_val
