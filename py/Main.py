import queue
import Collect as col
import Processing as proc
import visualize as vis

scales = [.02, 1, 1, 1]  # set on scope
y_pos = [0, 0, 0, 0]  # set on scope
sample_rate = 100e9
config = {'ip': '10.5.97.239', 'channels': [1, 0, 1, 0], 'settings': [scales, y_pos, sample_rate, 0],
          'record_length': 1e3, 'samp_clk_ch': 2, 'data_ch': 1, 'laser_ref_ch': 3, 'frame_count': 100, 'interp_factor':1}

raw_queue = queue.LifoQueue()
proc_queue = queue.LifoQueue()

collect = col.Collection(config, raw_queue)
processing = proc.Processing(config, raw_queue, proc_queue)
visualize = vis.Visualize(config, proc_queue)

collect.start()
processing.start()
visualize.run()

# collect.join()
