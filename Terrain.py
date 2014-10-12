import random

class Terrain:

    def __init__(self, width, smoothness = 1, seed = None):

        self.generate_1d_map(width, smoothness, seed)

    def generate_1d_map(self, width, smoothness=1, seed=None):

        if seed is None:
            seed = random.random()

        # window smoothness value
        if(smoothness < 0):
            smoothness = 0
        if(smoothness > 1):
            smoothness = 1

        # width needs to be an odd i.e. 2^n+1
        if (is_power_of_two(width -1)):
            size = width
        else:
            size = largest_suitable_width(width)

        # init map
        self.height_map = [0] * size

        # setup
        random.seed(seed)
        self.height_map[0] = random.random()
        self.height_map[size-1] = random.random()

        to_process = []
        to_process.extend([0, size-1, smoothness])

        # process
        min_height = min([self.height_map[0], self.height_map[size-1]])
        max_height = max([self.height_map[0], self.height_map[size-1]])
        i=0
        while (len(to_process) != 0):
            low = to_process.pop(0)
            high = to_process.pop(0)
            offset = to_process.pop(0)
            mid_point = (low + high)/2

            self.height_map[mid_point] = ((self.height_map[low] + self.height_map[high])/2) + random.uniform(-offset, offset)
            min_height = min(self.height_map[mid_point], min_height)
            max_height = max(self.height_map[mid_point], max_height)

            # terminating condition
            if (high - mid_point !=1):
                to_process.extend([low, mid_point, offset / pow(2, smoothness)])
                to_process.extend([mid_point, high, offset / pow(2, smoothness)])

            i+=1

        # clip length
        self.height_map = self.height_map[0:width]

        # normalise
        height_range = max_height - min_height
        for i in xrange(0,len(self.height_map)):
            self.height_map[i] = (self.height_map[i] - min_height) / height_range

def is_power_of_two(val):
    return (val !=0) and ((val & val-1) == 0)

def largest_suitable_width(val):
    size = 2;
    while(size + 1 < val):
        size *= 2
    return size + 1


        
