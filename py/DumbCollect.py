# This file will pull data from the oscilloscope
import threading
import time
from threading import Thread
import struct
import numpy as np
import queue
import matplotlib.pyplot as plt


class Collection(Thread):
    def __init__(self, config, raw_queue):
        Thread.__init__(self)
        self._stopevent = threading.Event()
        self.raw_queue = raw_queue
        self.config = config

    def run(self):
        time.sleep(0.2)
        run = True
        count = 0

        f = open('Waveform.wfm', 'rb')
        f.seek(488)
        f.seek(822)
        DataStartOffset = struct.unpack('i', f.read(4))[0]
        PostchargeStartOffset = struct.unpack('i', f.read(4))[0]
        record_length = PostchargeStartOffset - DataStartOffset
        f.seek(838)
        waveform = np.array(np.frombuffer(f.read(record_length), np.dtype(np.ubyte)))
        f.close()
        waveform = waveform + 80
        plt.plot(waveform)
        #
        # while run:
        #     # waveform = waveform[8:-1]  # Remove header information, first 8, last 1
        #
        #     self.raw_queue.put(waveform)
        #     count += 1
        #     run = True if count < 50 else False



    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)

if __name__ == '__main__':
    raw_queue = queue.LifoQueue()
    scales = [.02, 1, 1, 1]  # set on scope
    y_pos = [0, 0, 0, 0]  # set on scope
    sample_rate = 25e6
    # '10.5.97.239'
    config = {'ip': '192.168.0.2', 'channels': [1, 0, 1, 0], 'settings': [scales, y_pos, sample_rate, 0],
              'record_length': 5e5, 'samp_clk_ch': 2, 'data_ch': 1, 'laser_ref_ch': 3, 'frame_count': 2500,
              'interp_factor': 1, 'win_ard': 'COM5', 'frame_length': 200}
    dumb = Collection(config, raw_queue)
    dumb.run()

