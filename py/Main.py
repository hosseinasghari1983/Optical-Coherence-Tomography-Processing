import numpy as np

import py.Collect as Col

scales = [.02, 1, 1, 1]  # set on scope
y_pos = [0, 0, 0, 0]  # set on scope
sample_rate = 100e9
config = {'ip': '10.5.97.239', 'channels': [1, 0, 1, 0], 'settings': [scales, y_pos, sample_rate, 0],
          'recordLength': 1e3, 'samp_clk_ch': 2, 'data_ch': 1, 'laser_ref_ch': 3, 'frame_count': 100}

np.set_printoptions(threshold=np.inf)
print('Running.')
collector = Col.Collection(config)

for i in range(1):
    worker = Col.Thread(target=collector.run())
    worker.setDaemon(True)
    worker.start()

worker2 = Col.Thread(target=collector.print_data(collector.wave_queue))

print(f'signal: {collector.osc_sig} with shape {len(collector.osc_sig)} \n'
      f'time: {collector.osc_time}\n')
if collector.connect:
    np.savetxt('lastData.txt', np.array(collector.osc_sig))
