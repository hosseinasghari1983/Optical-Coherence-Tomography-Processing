import numpy as np
import queue
import py.Collect as Col

scales = [.02, 1, 1, 1]  # set on scope
y_pos = [0, 0, 0, 0]  # set on scope
sample_rate = 100e9
config = {'ip': '10.5.97.239', 'channels': [1, 0, 1, 0], 'settings': [scales, y_pos, sample_rate, 0],
          'record_length': 1e3, 'samp_clk_ch': 2, 'data_ch': 1, 'laser_ref_ch': 3, 'frame_count': 100}

raw_queue = queue.LifoQueue()
proc_queue = queue.LifoQueue()

collect = Collection(config, raw_queue)
processing = Processing(config, raw_queue, proc_queue)
visualize = Visualize(config, proc_queue)

collect.start()
processing.start()
visualize.start()