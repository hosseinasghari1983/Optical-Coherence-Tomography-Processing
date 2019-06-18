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


def cut_data(proc, layers):
    ref_max = np.unravel_index(np.argmax(proc, axis=None), proc.shape)[0]
    return proc[ref_max + 10:ref_max + 10 + layers, :]


class Visualize(Thread):
    def __init__(self, config, proc_queue):
        # matplotlib.use('Qt4Agg')
        # matplotlib.interactive(True)
        Thread.__init__(self)
        self.proc_queue = proc_queue
        self.config = config
        self._stopevent = threading.Event()

        # init with frames per second, resolution, etc

    def run(self):
        # proc = self.proc_queue.get(True)
        self.plot_4d()
        # After FFT PLOT
        # plt.figure(25)

    def after_fft(self):
        proc = self.proc_queue.get(True)[21:1000, :]
        # proc = cut_data(proc, 20)
        print(f'first proc is {proc.shape}')
        after_fft = plt.imshow(proc, aspect='auto', cmap='jet')
        while True:
            try:
                proc = self.proc_queue.get(False)[21:1000, :]
                # proc = cut_data(proc, 20)
                after_fft.set_data(proc)
                plt.draw()
            except queue.Empty:
                pass
            plt.pause(.05)

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

    def plot_4d(self):
        s = self.proc_queue.get(True)[:, :, 200:650]

        # s = cut_data(s, 20)
        plane = mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                                                 plane_orientation='z_axes',
                                                 slice_index=425,
                                                 )

        # mlab.volume_slice(s, plane_orientation='z_axes', slice_index=10)

        vol = mlab.pipeline.volume(mlab.pipeline.scalar_field(s))
        mlab.outline()

        @mlab.animate(delay=500)
        def anim():
            global s
            while True:
                try:
                    s = self.proc_queue.get(False)[:, :, 200:650]
                    # s = cut_data(s, 20)
                    plane.mlab_source.scalars = s
                    vol.mlab_source.scalars = s
                    yield
                except queue.Empty:
                    pass
                time.sleep(.5)
        anim()
        mlab.show()

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
