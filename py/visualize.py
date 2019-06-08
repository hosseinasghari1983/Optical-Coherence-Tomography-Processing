from threading import Thread
import queue
import matplotlib.pyplot as plt
import threading


class Visualize(Thread):
    def __init__(self, config, proc_queue):
        Thread.__init__(self)
        self.proc_queue = proc_queue
        self.config = config
        self._stopevent = threading.Event()

        # init with frames per second, resolution, etc

    def run(self):
        fig1 = plt.figure(1)
        plt.title('Time domain')
        plt.ion()
        while True:
            # query latest frame from Processing class
            # rearrange if needed
            # record it somewhere (for future playback?)
            # plot it!
            try:
                proc = self.proc_queue.get(False)
                print(self.proc_queue.qsize())
                plt.imshow(proc[:,:], aspect='auto', cmap='jet')
            except queue.Empty:
                pass
            plt.pause(0.1)
            #plt.show()
            # print(proc)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
