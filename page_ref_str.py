# Author:
# Created:
#
# Description:
#
import random as rand
DEFAULT_SEED = 42

class PageRefString:
    ref_str = []

    # Constructor
    def __init__(self, seed = DEFAULT_SEED, size = 100, end_num = 49, str_size = 100):
        rand.seed(seed)             # Seeds the rng with either the default or user defined value
        self.current_index = 0      # Current index in the reference string
        self.size = size            #
        self.start_num = 0          # Holds the value of the start address of the page numberspace
        self.end_num = end_num      #
        self.str_size = str_size    #
    
    # Reset ref_str with completely new values
    def reload_str(self):
        self.ref_str = []
        self._load_str()

    # Private support method meant to load ref_str assuming it's referencing an empty list
    def _load_str(self):
        for i in range(self.size):
            temp = rand.randint(0, 49)
            self.ref_str.append(temp)
