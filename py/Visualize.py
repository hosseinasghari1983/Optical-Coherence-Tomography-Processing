import queue
import threading
# import matplotlib
import time
from threading import Thread

# import mayavi as may
# from mayavi import mlab
import matplotlib.pyplot as plt
import numpy as np
# import vtk
from mayavi import mlab


def cut_data(proc, layers):
    ref_max = np.unravel_index(np.argmax(proc, axis=None), proc.shape)[0]
    return proc[ref_max + 10:ref_max + 10 + layers, :]


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
        # proc = self.proc_queue.get(True)
        self.plot_4d()
        # self.after_fft()
        # self.top_slice()
        # After FFT PLOT
        # plt.figure(25)

    def after_fft(self):
        proc = self.proc_queue.get(True)[0, :, 25:1000]
        # proc = cut_data(proc, 20)
        print(f'first proc is {proc.shape}')
        after_fft = plt.imshow(proc, aspect='auto', cmap='jet')
        slice = 0
        while True:
            try:
                proc = self.proc_queue.get(False)[slice, :, 25:1000]
                # proc = cut_data(proc, 20)
                after_fft.set_data(proc)
                plt.draw()
            except queue.Empty:
                pass
            plt.pause(.05)
            slice += 1
            slice = slice % 50

    def top_slice(self):
        fig1 = plt.figure(1)
        plt.title('Top Level Plot')
        plt.ion()
        proc = self.proc_queue.get(True)
        proc[:, :, 1000:] = 0
        proc[:, :, 0:25] = 0
        # max_val = np.amax(proc)
        # proc = proc / max_val
        proc = np.argmax(proc, axis=2)
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
                proc[:, :, 1000:] = 0
                proc[:, :, 0:25] = 0

                proc = np.argmax(proc, axis=2)

                # max_val = np.amax(proc)

                # proc = proc / max_val
                # print(f'with max_val {max_val}')
                top_obj.set_data(proc[:, :])
                # plt.savefig(f'temp/{im_name}', bbox_inches='tight')
                count += 1
                plt.draw()
            except queue.Empty:
                pass
            plt.pause(0.1)
            # run = False

    def plot_4d(self):
        s = self.proc_queue.get(True)[:, :, 10:150]

        # s = cut_data(s, 20)
        plane = mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                                                 plane_orientation='z_axes',
                                                 slice_index=15,
                                                 extent=[0, 1, 0, 1, 0, 1],
                                                 colormap='jet'
                                                 )

        plane_y = mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                                                   plane_orientation='y_axes',
                                                   slice_index=25,
                                                   extent=[0, 1, 0, 1, 0, 1],
                                                   colormap='jet'
                                                   )
        # mlab.volume_slice(s, plane_orientation='z_axes', slice_index=10)

        # vol = mlab.pipeline.volume(mlab.pipeline.scalar_field(s))

        # mlab.axes(extent=[0, 1, 0, 1, 0, 1])
        # plane.actor.actor.scale = (0.1, 1.0, 1.0)
        # plane_y.actor.actor.scale = (0.1, 1.0, 1.0)
        # vol.actor.actor.scale = (0.1, 1.0, 1.0)

        mlab.outline()

        @mlab.animate(delay=50)
        def anim():
            global s
            while True:
                try:
                    s = self.proc_queue.get(False)[:, :, 20:95]#20:150]
                    # s[:, :, 1000:] = 0
                    # s[:, :, 0:25] = 0
                    # s = cut_data(s, 20)
                    plane_y.mlab_source.scalars = s
                    plane.mlab_source.scalars = s
                    # vol.mlab_source.scalars = s
                    # mlab.axes(extent=[0, 1, 0, 1, 0, 1])
                    # plane.actor.actor.scale = (0.1, 1.0, 1.0)
                    # plane_y.actor.actor.scale = (0.1, 1.0, 1.0)
                    # vol.actor.actor.scale = (0.1, 1.0, 1.0)
                    yield
                except queue.Empty:
                    pass
                time.sleep(.075)
        anim()
        mlab.show()

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
