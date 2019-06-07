class Processing:

    def __init__(self, config, raw_queue, proc_queue):
        self.raw_queue = raw_queue
        self.proc_queue = proc_queue
        self.config = config


        #init with frames per second, resolution, etc

    def run():

        while not self._stopevent.isSet():
            waveform = np.reshape(raw_queue.get(), self.config['frame_count'],self.config['record_length'])
            y_time = waveform.copy()
            y_time = np.transpose(np.array(list(map(lambda row: np.real(np.fft.fftshift(np.fft.ifft(row))), y_time))))
            self.proc_queue.put(y_time)
            
        #query last read data from Collect
        #frame it according to sample size, resolution
        #perform ifft on each pulse
        #arrange it nicely
        #broadcast result


    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
