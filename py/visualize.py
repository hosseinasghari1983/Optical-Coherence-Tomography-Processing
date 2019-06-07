import matplotlib.pyplot as plt
import numpy as np

class Visualize:
    def __init__(self, config, proc_queue):
        self.proc_queue = proc_queue
        self.config = config


        #init with frames per second, resolution, etc

    def run():

        fig1 = plt.figure(1)

        while not self._stopevent.isSet():
            #query latest frame from Processing class
            #rearrange if needed
            #record it somewhere (for future playback?)
            #plot it!
            proc = self.proc_queue.get()

            plt.imshow(proc, aspect='auto', cmap='jet')
            plt.title('Time domain')
            plt.draw()

            

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)       