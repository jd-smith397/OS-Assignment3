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
    def __init__(self, num_frames: int, replacement_alg: int, rand_seed = 42):
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

        self.num_frames = num_frames
        self.ft = FrameTable(self.num_frames)
        self.prs = page_ref_str.PageRefStr(seed = rand_seed)
        self.page_faults = 0

    def run(self):
        self.replace[self.replacement_alg]()


    def __fcfs_replace(self):
        print("FCFS Replacement")
    def __lru_replace(self):
        print("LRU Replacement")
    def __opt_replace(self):
        print("OPT Replacement")

sim = Simulator(5, 1)
sim.run()