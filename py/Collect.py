# This file will pull data from the oscilloscope
import struct
import queue
from threading import Thread

import numpy as np
import visa

import serial

class Collection:
    def __init__(self, config):
        self.wave_queue = queue.LifoQueue()
        self.ard = serial.Serial('COM5', 115200)
        scales = [.02, 1, 1, 1]  # set on scope
        y_pos = [0, 0, 0, 0]  # set on scope
        sample_rate = 100e9
        self.config = config
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

        self.scope.write('TRIGger:SRCDEPENDENT;0.0000;0;1;AUTO;EDGE;100.0000E-3;100.0000E-3;100.0000E-3;100.0000E-3;100.0000E-3;2.0000;930.0001E-3;712.0000E-3;500.0000E-3;800.0000E-3;800.0000E-3;712.0000E-3;500.0000E-3;RANDOM;250.0000E-9;CH2;DC;DC;DC;DC;DC;RISE;RISE;RISE;RISE;RISE;RISE;OFF;PATTERN;AND;1.4000;930.0001E-3;712.0000E-3;500.0000E-3;HIGH;X;X;X;BINARY;"XXXXXXXXXXXXXXXX1XXX";X;TRUE;500.0000E-12;500.0000E-12;RISE;930.0001E-3;1.4000;930.0001E-3;712.0000E-3;500.0000E-3;CH2;1.4000;1.4000;930.0001E-3;712.0000E-3;500.0000E-3;CH1;500.0000E-12;1.0000E-9;OCCURS;RISE;TRUE;CH4;RISE;GLITCH;CH1;500.0000E-12;ACCEPT;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;OCCURS;OFF;ENTERSWINDOW;EITHER;EITHER;EITHER;EITHER;EITHER;600.0000E-12;2.0000;800.0000E-3;OCCURS;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;2.0000;800.0000E-3;OCCURS;500.0000E-12;OCCURS;500.0000E-12;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;2.0000;800.0000E-3;FASTERTHAN;OCCURS;500.0000E-12;500.0000E-12;WITHIN;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;OCCURS;OFF;500.0000E-12;500.0000E-12;GREATERTHAN;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;OCCURS;PERIOD;STAYSHIGH;STAYSHIGH;STAYSHIGH;STAYSHIGH;STAYSHIGH;500.0000E-12;OCCURS;OFF;0;SATA;BIT;"CJTPat";MANUAL;4;0;0;1;0;-1;60;ON;0;"0011111010";STOPPED;NOT_LOCKED;NOT_SYNC;NO_SIGNAL;MAX_AP_OK;0;0;0;0;"00111110101011011110110011101100";"00111110101011011010101110101011";1379029042;STOPPED;NOT_LOCKED;NO_SIGNAL;MAX_AP_OK;0;0;0;0;STOPPED;NOT_LOCKED;NO_SIGNAL;MAX_AP_OK;0;0;0;0;STOPPED;NOT_LOCKED;NO_SIGNAL;MAX_AP_OK;0;0;0;0;"1100000101";"0011111010";8;"00111101010100100101001011011110";OFF;"1100000101010101010101010101011101100011";OFF;"0011111010010101010101010101010010011100";"00111101010100100101001011011110";OFF;"1100000101110000010111000001011010101010";OFF;"0011111010001111101000111110101010101010";ON;155520000;NRZ;RECOVERED;0.0000;RISE;BINARY;"01";"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX0011111010";2640;0;CH1;OC3;PATTERN;CH2;1.4000;"XXXXXX01";0;DONTCARE;CH1;1.4000;START;BINARY;ADDR7;NONE;0;"XXXXX01";MOSI;CH3;0.0000;"01";HIGH;CH3;1.4000;"01";HIGH;0;CH1;1.4000;RISE;CH2;1.4000;LOW;BINARY;CH1;1.4000;"XXXXXX01";NONE;9.6000E+3;BINARY;OC3;NRZ;155520000;PLUSONE;2.0000;800.0000E-3;RISE;PLUSONE;CH1;DATA;B0;BINARY;"XXXXXXXXXXXXXXXXXX01";SS;1;"XXXXXX01";BINARY;START;DONTCARE;BINARY;1;"XXXXXX01";BINARY;ADDR7;NONE;"XXXXX01";START;BINARY;1;"XXXXXX01";PATTERN;SKP;"COM";"SKP";"SKP";"SKP";"1100000101";"0011110100";"0011110100";"0011110100";"0011111010";"1100001011";"1100001011";"1100001011";EITHER;CHARACTER;"1100000101";"0011111010";"K28.5";ORDEREDSET;SYNC;ANY;ANY;ANY;EQUAL;"XXXXXXXXXXX";BINARY;PID;"XXXXXXX";BINARY;"XXXXXXX";"XXXX";"XXXX";BINARY;ANY;1;DONTCARE;"XXXXXX01";"XXXXXX01";BINARY;SKP;"SKP";"SKP";"K28.5";"K28.5";"1100000110";"0011111001";"XXXXXXXXXX";"XXXXXXXXXX";"0011111001";"1100000110";"XXXXXXXXXX";"XXXXXXXXXX";2;EITHER;CHARACTER;"1100000101";"0011111010";"K28.5";ORDEREDSET;PATTERN;"K28.5";"K28.5";"K28.5";"K28.5";"1100000101";"0011111010";"1100000101";"0011111010";"0011111010";"1100000101";"0011111010";"1100000101";EITHER;CHARACTER;"1100000101";"0011111010";"K28.5";CHAR;SOF;DATA;"XXXXXXXX";BINARY;1;EQUAL;DONTCARE;"XXXXXXXXX01";BINARY;DONTCARE;STANDARD;SYNC;"XXXXXXXX";BINARY;1;EQUAL;"XXXXXX";BINARY;SYNC;SOF;NORMAL;"XXXXXXXXXXX";BINARY;EQUAL;"XXXXXXXX";BINARY;1;-1;EQUAL;"XXXXXX";BINARY;EQUAL;"XXXXXX";"XXXXX";"XXXXXXXXXXX";"XXXXXXX";"XXXXXXXXXXX";CRCHEADER;ALL;SYNC;"XXXXX";BINARY;EQUAL;X;"XXXXX";BINARY;"XXXXX";BINARY;X;"XXXXX";BINARY;EQUAL;X;X;X;X;X;X;X;X;X;"XXXXXXXXXXXXXXXX";BINARY;X;INRANGE;4.0000E-6;12.0000E-6;PARITY;SFD;EQUAL;"XXXXXXXXXXXX";HEX;"XXXXXXXXXXXX";HEX;"XXXX";HEX;1;-1;"XXXXXXXX";BINARY;"XX";HEX;"X.X.X.X";DECIMAL;"X.X.X.X";DECIMAL;"XXXX";HEX;"XXXX";HEX;"XXXXXXXX";HEX;"XXXXXXXX";HEX;"8100XXXX";HEX;1;EDGE;100.0000E-3;100.0000E-3;100.0000E-3;100.0000E-3;100.0000E-3;2.0000;930.0001E-3;712.0000E-3;500.0000E-3;800.0000E-3;800.0000E-3;712.0000E-3;500.0000E-3;TIME;OFF;SEQUENTIAL;1;8;1;CH3;DC;DC;DC;DC;DC;RISE;RISE;RISE;RISE;RISE;RISE;OFF;3.2000E-9;2;PATTERN;AND;1.4000;930.0001E-3;712.0000E-3;500.0000E-3;HIGH;X;X;X;BINARY;"XXXXXXXXXXXXXXXX1XXX";X;TRUE;500.0000E-12;500.0000E-12;RISE;930.0001E-3;1.4000;930.0001E-3;712.0000E-3;500.0000E-3;CH2;1.4000;1.4000;930.0001E-3;712.0000E-3;500.0000E-3;CH1;500.0000E-12;1.0000E-9;OCCURS;RISE;TRUE;CH4;RISE;GLITCH;CH1;500.0000E-12;ACCEPT;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;OCCURS;OFF;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;2.0000;800.0000E-3;OCCURS;500.0000E-12;OCCURS;ENTERSWINDOW;EITHER;EITHER;EITHER;EITHER;EITHER;600.0000E-12;2.0000;800.0000E-3;OCCURS;500.0000E-12;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;2.0000;800.0000E-3;FASTERTHAN;OCCURS;500.0000E-12;500.0000E-12;WITHIN;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;OCCURS;OFF;STAYSHIGH;STAYSHIGH;STAYSHIGH;STAYSHIGH;STAYSHIGH;500.0000E-12;OCCURS;OFF;500.0000E-12;500.0000E-12;GREATERTHAN;POSITIVE;POSITIVE;POSITIVE;POSITIVE;POSITIVE;OCCURS;PERIOD;NONE;1.0000E+6;1.0000E-3;100.0000E-9;4100;0;0;ON;0.0000;CH1;0.0000;HIGH;RISE;B0;BINARY;"XXXXXXXXXXXXXXXXXX01";1;')

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



        self.scope.write('ACQUIRE:STATE RUN')
        self.scope.write('ACQUIRE:SAMPLINGMODE RT')
        self.scope.write('ACQUIRE:STOPAFTER SEQuence')  # Single capture
        # self.scope.write('ACQUIRE:STOPAFTER RUNSTop')

        print('Rel WL process.')
        self.scope.write('DATa:SOUrce CH' + str(self.config["data_ch"]))
        self.scope.write('DISplay:WAVEform OFF')
        self.scope.write('CURVEStream?')




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
        # self.scope.write('CURVE?')
        self.ard.write(1)  # To trigger signal generator
        osc_data = self.scope.read_raw(101)
        # header_len = 2 + int(osc_data[1])
        # waveform = osc_data[header_len:-1]
        waveform = np.array(struct.unpack('%sB' % len(osc_data), osc_data))
        waveform = waveform[8:-1]  # Remove header information

        # print(f'ADC_wave is {ADC_wave} with shape {ADC_wave.shape}')

        # sig = (waveform - y_off) * y_mult + y_zero
        # time = np.linspace(0, x_incr * len(sig) * 1e9, len(sig))
        # sig =
        time = [1]
        self.osc_sig = np.array(waveform)
        self.osc_time = time

    def run(self):
        # Combine functions into a loop.
        #
        # get scope ready for acquisition
        #
        # loop:
        #   send trigger
        #   read data
        #   broadcast data
        collecting = True
        runner = Collection()
        runner.setup_scope()
        while collecting:
            runner.read_data()
            self.wave_queue.put(runner.osc_sig)
        return

    def print_data(self, q):
        while True:
            wave = q.get()
            print(wave)

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    print('Running.')
    collector = Collection()
    # collector.run()
    for i in range(1):
        worker = Thread(target=collector.run())
        worker.setDaemon(True)
        worker.start()
    worker2 = Thread(target=collector.print_data(collector.wave_queue))

    print(f'signal: {collector.osc_sig} with shape {len(collector.osc_sig)} \n'
          f'time: {collector.osc_time}\n')
    if collector.connect:
        np.savetxt('lastData.txt', np.array(collector.osc_sig))
        # file = open('lastData.txt', 'w+')
        # file.write(f'sig {collector.osc_sig} \r\n\r\n'
        #            f'time {collector.osc_time}\r\n\r\n')
        # file.close()
