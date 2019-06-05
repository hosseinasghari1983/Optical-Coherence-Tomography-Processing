# This file will pull data from the oscilloscope
import visa
import numpy as np
import struct


class Collection:
    def __init__(self):
        self.config = {'ip': '192.168.1.25', 'channels': [1, 0, 0, 0],
                       'settings': [[.02, 0, 0, 0], [0, 0, 0, 0], 20e9, 0], 'recordLength': 3e4}
        rm = visa.ResourceManager()
        for n in range(3):
            try:
                self.scope = rm.open_resource('TCPIP::' + self.config["ip"] + '::INSTR', open_timeout=1000)
                self.failure = False
            except Exception as e:
                print(f'{n}: Cannot connect to scope, error: {e}')
                self.failure = True
        self.osc_sig = []
        self.osc_time = []

    def setup_scope(self):
        if self.failure:
            return -1
        for ch in [1, 2, 3, 4]:
            active_ch = self.config["channels"][ch - 1]
            if active_ch:
                self.scope.write('SELECT:CH' + str(ch) + ' on')
                self.scope.write('CH' + str(ch) + ':SCALE ' + str(self.config['settings'][0][ch - 1]))
                self.scope.write('CH' + str(ch) + ':POSITION ' + str(self.config['settings'][1][ch - 1]))
            else:
                self.scope.write('SELECT:CH' + str(ch) + ' off')

        sample_rate = self.config['settings'][2]
        hor_pos = self.config['settings'][2]
        record_length = self.config['recordLength']

        self.scope.write('DATA:WIDTH 1')
        self.scope.write('DATA:ENC SFP')
        self.scope.write('HORIZONTAL:MAIN:SAMPLERate ' + str(sample_rate))
        self.scope.write('HORIZONTAL:RECORDLENGTH ' + str(record_length))
        record_length = self.scope.query("HORIZONTAL:RECORDLENGTH?")
        self.scope.write("data:start 1;stop " + str(record_length) + ";:data:encdg rpbinary;:DESE 1;:*ESE 1")
        self.scope.write('HORizontal:POSition ' + str(hor_pos))

    def read_data(self):
        if self.failure:
            return -1
        yMult = float(self.scope.query('WFMPRE:YMULT?'))
        yZero = float(self.scope.query('WFMPRE:YZERO?'))
        yOff = float(self.scope.query('WFMPRE:YOFF?'))
        x_incr = float(self.scope.query('WFMPRE:XINCR?'))

        #     single shot
        self.scope.write('ACQUIRE:STATE STOP')
        self.scope.write('ACQUIRE:MODE SAMPLE')
        self.scope.write('ACQUIRE:SAMPLINGMODE RT')
        self.scope.write('ACQUIRE:STOPAFTER SEQuence')

        self.scope.write('HORIZONTAL:FASTFRAME:STATE 1')
        self.scope.write('ACQUIRE:STATE RUN')

        # print('Rel WL process.')

        self.scope.write('DATA:SOU CH' + str(self.config["channels"][0]))
        self.scope.write('CURVE?')
        osc_data = self.scope.read_raw()
        header_len = 2 + int(osc_data[1])
        waveform = osc_data[header_len:-1]
        waveform = np.array(struct.unpack('%sB' % len(waveform), waveform))

        # print(f'ADC_wave is {ADC_wave} with shape {ADC_wave.shape}')

        sig = (waveform - yOff) * yMult + yZero
        time = np.linspace(0, x_incr * len(sig) * 1e9, len(sig))
        self.osc_sig = sig
        self.osc_time = time


if __name__ == '__main__':
    print('Running?')
    collector = Collection()
    collector.setup_scope()
    collector.read_data()
    print(f'signal: {collector.osc_sig} \n'
          f'time: {collector.osc_time}')
