# Author: Jessie Smith
# Created:
#
# Description: Provides simulator with a class for handling the page reference string
#
import random as rand
DEFAULT_SEED = 42
DEFAULT_STR_SIZE = 100   

class PageRefStr:
    ref_str = []

    # Constructor
    def __init__(self, seed = DEFAULT_SEED, end_num = 49, size = DEFAULT_STR_SIZE):
        rand.seed(seed)             # Seeds the rng with either the default or user defined value
        self.current_index = 0      # Current index in the reference string
        self.start_num = 0          # Value of the start number of the page numberspace
        self.end_num = end_num      # Value of the end number of the page numberspace
        self.size = size            # Size of the reference string

        self.__load_str()            #Loads the reference string with random variables
    
    #String representation of the page reference string for debugging
    def __repr__(self):
        temp = self.ref_str.copy()
        if self.current_index >= self.size:
            return f'Page Reference String:\n{temp}'
        temp[self.current_index] = f'***{temp[self.current_index]}***'
        return f'Page Reference String at index [{self.current_index}]:\n{temp}'

    # Reset ref_str with completely new values
    def reload_str(self):
        self.ref_str = []
        self. current_index = 0
        self.__load_str()

    # Utility method for use in the Optimal algorithm
    def find_distance(self, page_number: int):
        for i in range(self.current_index+1, self.size):
            if page_number == self.ref_str[i]:
                return i+1                      # Returns the distance if found
        return 0                                # Returns 0 indicating page number not found

    # Private support method meant to load ref_str assuming it's referencing an empty list
    def __load_str(self):
        for i in range(self.size):
            temp = rand.randint(0, 49)
            self.ref_str.append(temp)
