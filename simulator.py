import page_ref_str
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
    def __init__(self, num_frames: int, replacement_alg: int, rand_seed = page_ref_str.DEFAULT_SEED):
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
        #if 1 in lru_table:
        #   #If longer time, set longest time to this
        #else:
        #   #Replace this frame
        #   #self.lru_table[1] = clock

    def run(self):
        while(self.prs.current_index < self.prs.size):
            current_page = self.prs.ref_str[self.prs.current_index]
            replaced = False

            for i in range(self.num_frames):
                current_frame = self.ft.frames[i]
                if current_frame.valid:
                    if current_frame.page == current_page:
                        replaced = True
                else:
                    self.ft.frames[i].valid = True
                    self.ft.frames[i].page = current_page
                    replaced = True
                

            if not replaced:
                self.replace[self.replacement_alg]()
                replaced = True

            self.prs.current_index += 1


    def __fcfs_replace(self):
        self.ft.frames[self.next_fcfs_repl].page = self.prs.ref_str[self.prs.current_index]
        self.next_fcfs_repl = (self.next_fcfs_repl + 1) % self.num_frames
        print("FCFS Replacement")                    # Placeholder until implemented and tested
    def __lru_replace(self):
        print("LRU Replacement")                     # Placeholder until implemented and tested
    def __opt_replace(self):
        print("OPT Replacement")                     # Placeholder until implemented and tested

sim = Simulator(5, 1)
sim.run()