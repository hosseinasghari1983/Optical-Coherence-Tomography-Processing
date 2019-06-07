import numpy as np

class Processing:

    def __init__(self, data, config):
        # init with frames per second, resolution, etc
        self.config = config
        self.sig = data.osc_sig
        self.frames = np.arange(0)

    def quick_frame(self):
        frame_array = np.zeros(self.config['frame_count', self.config['recordLength']])
        start = 0
        end = self.config['recordLength']
        for frame in frame_array:
            frame = frame_array[start:end]
            start = start + self.config['recordLength']
            end = start + self.config['recordLength']
        self.frames = np.array(frame_array)

    def run():
        #query last read data from Collect
        #frame it according to sample size, resolution
        #perform ifft on each pulse
        #arrange it nicely
        #broadcast result
