import page_ref_str
import logging as log
from dataclasses import dataclass

@dataclass
class Frame:
    page: int
    valid: bool

class FrameTable:
    frames = []

    #Constructor
    def __init__(self, num_frames: int):
        self.num_frames = num_frames
        self.__load()

    def __repr__(self):
        temp = []
        for i in self.frames:
            temp.append(i.page)
        return f'Frame Table: {temp}'

    #object reset for this 
    def reload(self):
        self.frames = []
        self.__load()

    #
    def __load(self):
        for i in range(self.num_frames):
            temp_frame = Frame(-1, False)
            self.frames.append(temp_frame)
            

class Simulator:
    replacement_alg: str
    #Constructor
    def __init__(self, num_frames: int, replacement_alg: int, rand_seed = page_ref_str.DEFAULT_SEED, debug = False):
        if replacement_alg == 1:
            self.replacement_alg = "FCFS"
        elif replacement_alg == 2:
            self.replacement_alg = "LRU"
        elif replacement_alg == 3:
            self.replacement_alg = "OPT"
        else:
            raise ValueError("Replacement algorithm represented by ", replacement_alg ," not implemented.")

        #Creating dictionary of replacement algorithms
        self.replace = {"FCFS": self.__fcfs_replace, "LRU": self.__lru_replace, "OPT": self.__opt_replace}

        self.num_frames = num_frames                                # Number of frames in physical memory
        self.ft = FrameTable(self.num_frames)                       # Frame table of physical memory
        self.prs = page_ref_str.PageRefStr(seed = rand_seed)        # Page reference string
        self.page_faults = 0                                        # Number of page faults initialized to 0
        self.next_fcfs_repl = 0                                     # Next frame to be replaced in fcfs
        self.clock = 0                                              # Time, for purposes of lru
        self.lru_table = {}                                         # Table of when each page number was last used
        self.debug = debug                                          # If true, the state of the system will be logged    
        
        log.basicConfig(filename=f'{self.replacement_alg}_{self.num_frames}_debug.log',  
            level=log.INFO, filemode='w', 
            format='%(levelname)s -\n%(message)s\n-------------------\n')     # Setup for logging
        
    def run(self):

        if self.debug:
            self.__log_state()
            log.info(f'Beginning Simulation using {self.replacement_alg} algorithm...') if self.debug else ''

        while(self.prs.current_index < self.prs.size):
            current_page = self.prs.ref_str[self.prs.current_index]
            replaced = False

            for i in range(self.num_frames):
                current_frame = self.ft.frames[i]
                if current_frame.valid:
                    if current_frame.page == current_page:
                        log.info('Page hit') if self.debug else ''
                        if self.replacement_alg == 'LRU':
                            self.lru_table[self.ft.frames[i].page] = self.clock
                        replaced = True
                        break
                else:
                    self.ft.frames[i].valid = True
                    self.ft.frames[i].page = current_page
                    self.page_faults += 1
                    if self.replacement_alg == 'LRU':
                        self.lru_table[self.ft.frames[i].page] = self.clock
                    replaced = True
                    log.info('Cold start page fault') if self.debug else ''
                    break
                

            if not replaced:
                log.info('Page fault') if self.debug else ''
                self.replace[self.replacement_alg]()
                replaced = True

            if self.debug:
                self.__log_state()

            self.clock += 1
            self.prs.current_index += 1

    # Method for handling fcfs replacement
    def __fcfs_replace(self):
        self.ft.frames[self.next_fcfs_repl].page = self.prs.ref_str[self.prs.current_index]
        self.next_fcfs_repl = (self.next_fcfs_repl + 1) % self.num_frames
        self.page_faults += 1
    
    # Method for handling lru replacement
    def __lru_replace(self):
        least_recent = -1
        lru_index = -1
        replaced = False

        for i in range(self.num_frames):
            if self.ft.frames[i].page in self.lru_table:
                current_length = self.lru_table[self.ft.frames[i].page]
                if current_length < least_recent or least_recent == -1:
                    least_recent = current_length
                    lru_index = i
            else:
                lru_index = i
                break
        
        self.lru_table[self.prs.ref_str[self.prs.current_index]] = self.clock
        self.ft.frames[lru_index].page = self.prs.ref_str[self.prs.current_index]
        self.page_faults += 1
    
    # Method for handling opt replacement
    def __opt_replace(self):
        farthest_distance = -1
        farthest_i = -1 

        for i in range(self.num_frames):
            current_distance = self.prs.find_distance(self.ft.frames[i].page)

            # Break from loop & choose this frame for replacement if not found
            if current_distance == 0:
                farthest_i = i
                break
            if current_distance > farthest_distance or farthest_distance == -1:
                farthest_distance = current_distance
                farthest_i = i
        
        self.ft.frames[farthest_i].page = self.prs.ref_str[self.prs.current_index]
        self.page_faults += 1
        
    # Method for logging the state of the system    
    def __log_state(self):
        message = f'{repr(self.prs)}\n{repr(self.ft)}\nPage Faults: {self.page_faults}'
        if self.replacement_alg == 'LRU':
            message += f'\nLRU Table: {self.lru_table}'
        log.info(message)

sim = Simulator(5, 3, debug = True)
sim.run()