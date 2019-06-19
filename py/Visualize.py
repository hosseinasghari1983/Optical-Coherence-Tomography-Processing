import queue
import threading
from threading import Thread
import PyQt5
# import vtk
from mayavi import mlab
# import mayavi as may
# from mayavi import mlab
import matplotlib.pyplot as plt
# import matplotlib
import time
import numpy as np


class Visualize(Thread):
    def __init__(self, config, proc_queue, framed_queue):
        # matplotlib.use('Qt4Agg')
        # matplotlib.interactive(True)
        Thread.__init__(self)
        self.proc_queue = proc_queue
        self.framed_queue = framed_queue
        self.config = config
        self._stopevent = threading.Event()

        # init with frames per second, resolution, etc

    def run(self):
        # self.slices()
        # self.top_slice()
        fig1 = plt.figure(1)
        if self.config['debug_framing']:
            proc = self.framed_queue.get(True)
            after_fft = plt.imshow(proc[:, :], aspect='auto', cmap='jet')
            while True:
                try:
                    proc = self.framed_queue.get(False)
                    after_fft.set_data(proc[:, :])
                    plt.draw()
                except queue.Empty:
                    pass
                plt.pause(.2)
        else:
            proc = self.proc_queue.get(True)
            after_fft = plt.imshow(proc[:, :], aspect='auto', cmap='jet')
            while True:
                try:
                    proc = self.proc_queue.get(False)
                    after_fft.set_data(proc[:, :])
                    plt.draw()
                except queue.Empty:
                    pass
                plt.pause(.2)

        # mlab.test_contour3d()
        # mlab.show()
        # time.sleep(3)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)

    def top_slice(self):
        fig1 = plt.figure(1)
        plt.title('Top Level Plot')
        plt.ion()
        proc = self.proc_queue.get(True)
        proc[0:5050, :] = 0
        max_val = np.amax(proc)
        proc = proc / max_val
        proc = np.amax(proc, axis=0)
        proc = np.reshape(proc[-1:-2304], (48, 48))
        top_obj = plt.imshow(proc[:, :], aspect='auto', cmap='jet')
        run = True
        count = 0
        while run:
            # query latest frame from Processing class
            # rearrange if needed
            # record it somewhere (for future playback?)
            # plot it!
            try:
                im_name = 'top' + str(count)
                proc = self.proc_queue.get(False)
                proc = np.amax(proc, axis=0)
                proc = np.reshape(proc[:2304], (48, 48))
                proc[0:5050, :] = 0
                max_val = np.amax(proc)

                proc = proc / max_val
                print(f'with max_val {max_val}')
                top_obj.set_data(proc[:2304])
                # plt.savefig(f'temp/{im_name}', bbox_inches='tight')
                count += 1
                plt.draw()
            except queue.Empty:
                pass
            plt.pause(0.7)
            # run = False

    def slices(self):
        proc = self.proc_queue.get(True)
        proc = proc[5051:5072, :]
        proc = np.reshape(proc, (50, 50, 20))
        print(f'3d array: {proc}')
        mlab.volume_slice(proc)
        mlab.show()
        while True:
            try:
                proc = self.proc_queue.get(False)
                proc = proc[5051:5072, :]
                proc = np.reshape(proc, (50, 50, 20))
                mlab.volume_slice(proc)
                mlab.show()
            except queue.Empty:
                pass
            time.sleep(.05)

    def cut_data(self):
        proc = self.proc_queue.get(True)
        ref_max = np.unravel_index(np.argmax(proc, axis=None), proc.shape)[0]
        return proc[ref_max + 2:ref_max + 22, :]
