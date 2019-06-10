from threading import Thread
import queue
import numpy as np
import matplotlib.pyplot as plt
import threading
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


class Visualize(Thread):
    def __init__(self, config, proc_queue):
        Thread.__init__(self)
        self.proc_queue = proc_queue
        self.config = config
        self._stopevent = threading.Event()

        # init with frames per second, resolution, etc

    def run(self):
        # fig1 = plt.figure(1)
        # plt.title('Time domain')
        # plt.ion()
        
        proc = self.proc_queue.get(True)
        proc[0:5050, :] = 0
        max_val = np.amax(proc)
        proc = proc/max_val
        #  proc = np.amin(proc,axis=0)
        #  proc = np.reshape(proc,(50,50))
        # objj = plt.imshow(proc[:, :], aspect='auto', cmap='jet')


        # while True:
        #
        #     # query latest frame from Processing class
        #     # rearrange if needed
        #     # record it somewhere (for future playback?)
        #     # plot it!
        #     try:
        #         proc = self.proc_queue.get(False)
        #         #  self.proc_queue.queue.clear()
        #         print(self.proc_queue.qsize())
        #         #proc = np.amin(proc,axis=0)
        #         #  proc = np.reshape(proc,(50,50))
        #         proc[0:5050, :] = 0
        #         max_val = np.amax(proc)
        #         proc = proc/max_val
        #         objj.set_data(proc[:])
        #         plt.draw()
        #     except queue.Empty:
        #         pass
        #     plt.pause(0.1)
        #     #plt.show()
        #     # print(proc)


        X = np.arange(0, 50, 1)
        Y = np.arange(0, 50, 1)
        X, Y = np.meshgrid(X, Y)
        Z = np.zeros_like(X)
        fig3 = plt.figure(3)
        ax = fig3.gca(projection='3d')
        m = cm.ScalarMappable(cmap='jet')

        while True:
            # query latest frame from Processing class
            # rearrange if needed
            # record it somewhere (for future playback?)
            # plot it!
            try:
                proc = self.proc_queue.get(False)
                # ref_max = np.unravel_index(np.argmax(proc, axis=None), proc.shape)[0]
                # sliced = proc[ref_max + 2:ref_max + 20, :]
                sliced = proc[5051:, :]
                max_val = np.amax(sliced)
                sliced = sliced / max_val
                data_start = np.unravel_index(np.argmax(sliced, axis=None), sliced.shape)[0]
                count = 0
                for row in sliced[data_start:int(data_start + 4)]:
                    row = np.reshape(row, (50, 50))
                    ax.plot_surface(X, Y, Z+count*.1, rstride=1, cstride=1, facecolors=m.set_array(row))
                    count += 1

                plt.draw()

            except queue.Empty:
                pass
            plt.pause(0.1)


    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
