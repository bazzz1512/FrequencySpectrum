import scipy.io
from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt
import wfdb
import sys
import os

frequency_data = None
number_index = 1024
number = 7
fs = 360
total_index = 100000
#@title converts .mat data to numpy arrays
# mat = scipy.io.loadmat('ECGData.mat')


directory = "C:/Users/sebas/PycharmProjects/BAP/FrequencySpectrum/mit-bih-arrhythmia-database-1.0.0/"
ECGs = []
for ecgfilename in sorted(os.listdir(directory )):
    if ecgfilename.endswith(".dat"):
        ecg = wfdb.rdsamp(directory  + ecgfilename.split(".")[0])
        ECGs.append(ecg)
ECGs = np.asarray(ECGs)

# loading data and labels into x and y  numpy arrays
# x=mat['ECGData']['Data'].item()
# y=mat['ECGData']['Labels'].item()
total_data = []
for j in range(np.shape(ECGs)[0]):
# for j in range(0,10):
    raw_data = ECGs[j][0]
    x = [i[0] for i in raw_data]

    x = x[0:total_index]

    fft_orig = np.fft.fft(x)
    total_data.append(fft_orig)
    print(j)

summed_data = np.sum(total_data, axis=0)


x_size = len(summed_data)
print(x_size)

fft_value = summed_data

high_pass = int((0.5/fs)*x_size)    # High pass from 0.5 Hz onwards

band_low = int((59.5/fs)*x_size)
band_high = int((60.5/fs)*x_size)

fft_value[0:high_pass] = 0
fft_value[-high_pass:0] = 0

fft_value[-band_high:-band_low] = 0
fft_value[band_low:band_high] = 0

amp = np.abs(fft_value)
freq = np.linspace(0.0,1.0/(2.0 * (1/fs)), len(x)//2)

plt.figure(0, dpi=1200)
plt.title("Frequency domain")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.plot(freq, (2/len(amp)) * amp[0:len(amp)//2])
plt.savefig("Frequency_components_summed.png")
plt.show()


