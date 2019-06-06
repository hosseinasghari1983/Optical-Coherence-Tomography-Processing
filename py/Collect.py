# This file will pull data from the oscilloscope
import struct
import sys


import numpy as np
import visa

import serial


class Collection:
    def __init__(self):
        self.ard = serial.Serial('COM5', 115200)
        scales = [.02, 1, 1, 1]  # set on scope
        y_pos = [0, 0, 0, 0]  # set on scope
        sample_rate = 100e9
        self.config = {'ip': '10.5.97.239', 'channels': [1, 0, 1, 0], 'settings': [scales, y_pos, sample_rate, 0],
                       'recordLength': 1e3, 'samp_clk_ch': 2, 'data_ch': 1, 'laser_ref_ch': 3, 'frame_count': 100}
        rm = visa.ResourceManager()
        self.connect = False
        for n in range(3):
            try:
                print(rm.list_resources())
                # print('TCPIP::' + self.config["ip"] + '::inst0::INSTR')
                self.scope = rm.open_resource('TCPIP::' + self.config["ip"] + '::INSTR', open_timeout=1000)
                self.connect = True
                break
            except Exception as e:
                print(f'{n}: Cannot connect to scope, error: {e}')
                self.connect = False
        self.osc_sig = []
        self.osc_time = []
        self.encoding = 'NA'

    def setup_scope(self):
        if not self.connect:
            return -1

        f = open("trigger_setup.txt", "a+")
        f.write(self.scope.query('TRIGger?'))
        f.write('\r\n ==== \r\n TRIGGER ABOVE \r\n ====')
        f.close()

        self.scope.chunk_size = 100 * self.config['recordLength'] * self.config['frame_count']

        for ch in [1, 2, 3, 4]:
            active_ch = self.config["channels"][ch - 1]
            if active_ch:  # Turns on enabled channels
                self.scope.write('SELect:CH' + str(ch) + ' ON')
                # self.scope.write('CH' + str(ch) + ':SCAle ' + str(self.config['settings'][0][ch - 1]))
                # self.scope.write('CH' + str(ch) + ':POSITION ' + str(self.config['settings'][1][ch - 1]))
            else:
                self.scope.write('SELECT:CH' + str(ch) + ' OFF')

        sample_rate = self.config['settings'][2]
        hor_pos = self.config['settings'][3]
        record_length = self.config['recordLength']

        self.scope.write('DATa:WIDTH 1')
        self.scope.write('DATa:ENCdg FAStest')
        # self.encoding = self.scope.query('DATa:ENCdg?')
        print(f'encoding data type is {self.encoding}')

        self.scope.write('HORizontal:MODE:SAMPLERate ' + str(sample_rate))  # Sets sample rate
        self.scope.write('HORizontal:MODE:RECOrdlength ' + str(record_length))  # Number of samples
        # self.config['recordLength'] = self.scope.query("HORizontal:MODE:RECOrdlength?")
        # self.scope.write("DATa:STARt 1;stop " + str(record_length) + ";:data:encdg rpbinary;:DESE 1;:*ESE 1")
        self.scope.write('DATa:STARt 1')
        self.scope.write('DATa:STOP ' + str(self.config['recordLength']))
        # self.scope.write('HORizontal:POSition ' + str(hor_pos))

        self.scope.write('HORizontal:FASTframe:STATE ON')
        self.scope.write('HORizontal:FASTframe:SELECTED: SOUrce CH' + str(self.config["data_ch"]))
        self.scope.write('HORizontal:FASTframe:COUNt ' + str(self.config['frame_count']))

    def read_data(self):
        if not self.connect:
            return -1

        # y_mult = float(self.scope.query('WFMPRE:YMULT?'))
        # y_zero = float(self.scope.query('WFMPRE:YZERO?'))
        # y_off = float(self.scope.query('WFMPRE:YOFF?'))
        # x_incr = float(self.scope.query('WFMPRE:XINCR?'))

        #     single shot
        # self.scope.write('ACQUIRE:STATE STOP')
        # self.scope.write('ACQUIRE:MODE SAMPLE')
        # self.scope.write('ACQUIRE:SAMPLINGMODE RT')
        # self.scope.write('ACQUIRE:STOPAFTER SEQuence')

        # self.scope.write('HORizontal[:MAIn]:DELay:MODe ON')
        # self.scope.write('HORizontal[:MAIn]:DELay:TIMe 100e-6')
        self.scope.write('ACQUIRE:STATE RUN')
        self.scope.write('ACQUIRE:SAMPLINGMODE RT')
        self.scope.write('ACQUIRE:STOPAFTER SEQuence')

        # print('Rel WL process.')
        self.scope.write('DATa:SOUrce CH' + str(self.config["data_ch"]))
        self.scope.write('DISplay:WAVEform ON')
        # self.scope.write('CURVEStream')
        self.scope.write('CURVE?')
        self.ard.write(1)  # To trigger signal generator
        osc_data = self.scope.read_raw(101)
        # header_len = 2 + int(osc_data[1])
        # waveform = osc_data[header_len:-1]
        waveform = np.array(struct.unpack('%sB' % len(osc_data), osc_data))

        # print(f'ADC_wave is {ADC_wave} with shape {ADC_wave.shape}')

        # sig = (waveform - y_off) * y_mult + y_zero
        # time = np.linspace(0, x_incr * len(sig) * 1e9, len(sig))
        sig = np.array(waveform)
        time = [1]
        self.osc_sig = sig
        self.osc_time = time


if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    print('Running.')
    collector = Collection()
    collector.setup_scope()
    collector.read_data()
    print(f'signal: {collector.osc_sig} with shape {len(collector.osc_sig)} \n'
          f'time: {collector.osc_time}\n')
    if collector.connect:
        file = open('lastData.txt', 'w+')
        file.write(f'sig {collector.osc_sig} \r\n\r\n'
                   f'time {collector.osc_time}\r\n\r\n')
        file.close()
