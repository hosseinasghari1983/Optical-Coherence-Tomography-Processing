from threading import Thread
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
            proc = self.proc_queue.get()
            plt.imshow(proc, aspect='auto', cmap='jet')
            plt.draw()
            plt.show()
            # print(proc)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
