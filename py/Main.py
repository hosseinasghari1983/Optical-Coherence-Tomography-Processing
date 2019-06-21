import queue
import Collect as col
import Processing as proc
import Visualize as vis
# import DumbCollect as dumb
import time

scales = [.02, 1, 1, 1]  # set on scope
y_pos = [0, 0, 0, 0]  # set on scope
sample_rate = 25e6
#'10.5.97.239'
config = {'ip': '192.168.0.2', 'channels': [1, 0, 0, 1], 'settings': [scales, y_pos, sample_rate, 0],
          'record_length': 2e6, 'frame_count': 1, 'samp_clk_ch': 2, 'data_ch': 1,
          'interp_factor': 1, 'win_ard': 'COM5', 'period_guess': 210, 'debug_framing': True}
# frame length is record_length / frame_count

# LIFO VS FIFO?
raw_queue = queue.LifoQueue()
framed_queue = queue.LifoQueue()
proc_queue = queue.Queue()

collect = col.Collection(config, raw_queue)
processing = proc.Processing(config, raw_queue, proc_queue, framed_queue)
visualize = vis.Visualize(config, proc_queue, framed_queue)

collect.start()
# dumb_col.start()
time.sleep(3)
processing.start()
visualize.run()

# collect.join()
