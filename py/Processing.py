import numpy as np
from threading import Thread
import threading
import multiprocessing
import time
import matplotlib.pyplot as plt
from scipy import interpolate

#GPU FFT STUFF
#from reikna.fft import FFT



class Processing(Thread):

    def __init__(self, config, raw_queue, proc_queue, framed_queue):
        Thread.__init__(self)
        # self.period = config['settings'][2] * 8000
        self.period = config['period_guess']
        self.raw_queue = raw_queue
        self.proc_queue = proc_queue
        self.framed_queue = framed_queue
        self.config = config
        self._stopevent = threading.Event()
        #init with frames per second, resolution, etc

    def run(self):
        # not self._stopevent.isSet()
        run = True
        while run:
            # waveform = np.reshape(self.raw_queue.get(), (int(self.config['frame_count']), int(self.config['record_length']*self.config['interp_factor'])))
            # waveform = np.reshape(self.raw_queue.get(), (int(self.config['frame_count']), int(self.config['frame_length']*self.config['interp_factor'])))

            print("Processing...")
            t = time.time()
            waveform = self.raw_queue.get()

            if self.config['interp_factor'] > 1:
                pts = self.config['record_length'] * self.config['frame_count']
                func = interpolate.interp1d(np.linspace(0, pts, pts), waveform, kind='cubic')
                waveform = func(np.linspace(0, pts, pts * self.config['interp_factor']))

            waveform = self.framing(waveform)

            self.framed_queue.put(waveform)
            # with self.raw_queue.mutex:
            #     self.raw_queue.queue.clear()
            # waveform = np.copy(waveform)
            # print(waveform.shape)
            #

            # waveform = list(map(lambda row: np.absolute(np.fft.fftshift(np.fft.ifft(row, n=10000))), waveform))
            waveform = np.array([[np.absolute(np.fft.ifft(pulse))] for pulse in waveform])

            elapsed = time.time() - t

            waveform = np.transpose(waveform)

            print("...Done!")

            print(f'\r\n Processing took {elapsed} seconds. \r\n')

            self.proc_queue.put(waveform)
            # run = False
        #query last read data from Collect
        #frame it according to sample size, resolution
        #perform ifft on each pulse
        #arrange it nicely
        #broadcast result

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)

    def framing(self, waveform):
        length = waveform.size
        # print(waveform.time[1] - waveform.time[0])

        # USING NANOSECONDS AS UNITS

        spns = self.config['settings'][2]  # 100Gs/s, or 100 samples per nanosecond
        period = self.period  # initial period guess, in sample units

        ahead = waveform[0:int(period * 4.5)]  # seek forward two and something periods

        # fig1 = plt.figure(22)
        # plt.clf()
        # plt.title("First Two")
        # plt.plot(ahead)

        max = np.argmax(ahead)
        min = np.argmin(ahead)

        span = ahead[max] - ahead[min]

        maxes = np.argwhere(ahead > (ahead[max] - span * 0.35))  # 20% tolerance for max, as fringes can change rapidly
        mins = np.argwhere(ahead < (ahead[min] + span * 0.25))  # 10% tolerance for mins, pulses expected to return to the same level each cycle

        initialMax = maxes[0,0]  # make sure we start from a peak, this guarantess that the next minimum is a full valley, not truncated at the beggining

        ffirstMin = mins[np.searchsorted(mins[:, 0], initialMax), 0]  # first of the first min group
        firstMax = maxes[np.searchsorted(maxes[:, 0], ffirstMin), 0]  # first max after this min group
        firstMinEnd = np.searchsorted(mins[:, 0], firstMax)  # now we know the end of the first min group
        lfirstMin = mins[firstMinEnd - 1, 0]

        fnextMin = mins[firstMinEnd, 0]  # first of the next min group
        nextMax = maxes[np.searchsorted(maxes[:, 0], fnextMin), 0]  # first max after the next min group
        nextMinEnd = np.searchsorted(mins[:, 0], nextMax)  # now we know the end of the next min group
        lnextMin = mins[nextMinEnd - 1, 0]

        # plt.plot(initialMax, ahead[initialMax], 'r*')
        #
        # plt.plot(ffirstMin, ahead[ffirstMin], 'g+')
        # plt.plot(lfirstMin, ahead[lfirstMin], 'g+')
        #
        # plt.plot(firstMax, ahead[firstMax], 'r*')
        #
        # plt.plot(fnextMin, ahead[fnextMin], 'g+')
        # plt.plot(lnextMin, ahead[lnextMin], 'g+')
        #
        # plt.plot(nextMax, ahead[nextMax], 'g+')

        # with the start and end of the first and second min groups, we can calculate the center for each and thus the slicing points (and period!)

        firstMin = int((ffirstMin + lfirstMin) / 2)
        nextMin = int((fnextMin + lnextMin) / 2)

        signal = waveform[firstMin:]
        length = signal.size

        period = nextMin - firstMin
        firstMin = 0

        # now jump ahead periods and recalculate, 2^n jumps

        n = 2
        jumping = True
        while jumping:
            jump = n * period
            areaStart = int(jump - period * 0.25)
            areaEnd = int(jump + period * 0.25)
            if (areaEnd > length):  # make sure to also align with last possible pulse
                n = int(length / period)
                jump = n * period
                areaStart = int(jump - period * 0.25)
                areaEnd = int(jump + period * 0.25)
                jumping = False

            area = signal[areaStart:areaEnd]
            nextMin = areaStart + self.seekMin(area, span)
            period = (nextMin - firstMin) / n
            self.period = period
            # print("Period:" + str(period))

            n += n

        # plt.pause(1)
        # # plt.savefig()
        # plt.show()

        # time_array = np.linspace(0, period / spns, period)

        nSlices = int(len(signal) / period)
        print(f'periods in wave {len(signal) / period}')
        intPeriod = int(period)
        y_array = np.zeros((nSlices, intPeriod))

        for i in range(nSlices):  # save each slice as row
            start = int(
                i * period)  # note that one value may be lost every now and then, as the period is not an integer number of samples. this is done to make sure all rows have the same number of columns
            y_array[i, :] = signal[start:(start + intPeriod)]

        return y_array

    def seekMin(self, area, span):
        min = np.argmin(area)
        mins = np.argwhere(area < (area[
                                       min] + span * 0.1))  # 10% tolerance for mins, pulses expected to return to the same level each cycle
        return int((mins[0] + mins[-1]) / 2)
