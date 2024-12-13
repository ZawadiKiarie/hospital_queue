import heapq

class PriorityQueue:
  def __init__(self):
    self.data = [] #list to store the heap(priority, counter, data)
    self.counter = 0 # unique counter to ensure stability for equal priorities
    self.locators ={} #dicitionary to track elements by their identifier(e.g name)
    
  def add(self, priority, profile):
    self.counter += 1
    locator = (-priority, self.counter, profile)
    heapq.heappush(self.data, locator)
    self.locators[profile['name']] = locator
    
  def min(self):
    if not self.is_empty():
      return self.data[0][2]
    return None
  
  def remove_min(self):
    if not self.is_empty():
      _, _, profile = heapq.heappop(self.data)
      del self.locators[profile['name']]
      self._print_state()
      return profile
    return None
  
  def remove_by_name(self, name):
    if name in self.locators:
      locator = self.locators.pop(name)
      self.data.remove(locator)
      heapq.heapify(self.data) # reheapify the list to restore heap order
      self._print_state()
      return locator[2]#returns the profile
    return None
  
  def update(self, name, new_priority, new_profile):
    if name in self.locators:
      self.remove_by_name(name)
      self.add(new_priority, new_profile)
    else:
      raise ValueError(f"Profile with name '{name}' does not exist in the queue.")
    
  def is_empty(self):
    return len(self.data) == 0
  
  def __len__(self):
    return len(self.data)
  
  def _print_state(self):
    print("Current heap state:")
    sorted_data = sorted(self.data)
    for item in self.data:
      print(f"Priority: {item[0]}, counter: {item[1]}, Profile: {item[2]}")