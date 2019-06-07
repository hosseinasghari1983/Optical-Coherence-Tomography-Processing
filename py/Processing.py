import numpy as np
from threading import Thread
import threading


class Processing(Thread):

    def __init__(self, config, raw_queue, proc_queue):
        Thread.__init__(self)
        self.raw_queue = raw_queue
        self.proc_queue = proc_queue
        self.config = config
        self._stopevent = threading.Event()


        #init with frames per second, resolution, etc

    def run(self):
        # not self._stopevent.isSet()
        while True:
            waveform = np.reshape(self.raw_queue.get(), (int(self.config['frame_count']), int(self.config['record_length'])))
            y_time = waveform.copy()
            print(y_time.shape)
            y_time = np.transpose(np.array(list(map(lambda row: np.real(np.fft.fftshift(np.fft.ifft(row))), y_time))))
            #y_time = np.transpose(np.array(list(map(lambda row: np.fft.fftshift(np.fft.ifft(row)), y_time))))
            self.proc_queue.put(y_time)
            
        #query last read data from Collect
        #frame it according to sample size, resolution
        #perform ifft on each pulse
        #arrange it nicely
        #broadcast result

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
