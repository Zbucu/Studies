import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy
import soundfile as sf
import sounddevice as sd
import time

def kwant(data,bit):
    d = (2**bit)- 1
    if np.issubdtype(data.dtype,np.floating):
        m = -1
        n = 1
    else:
        m = np.iinfo(data.dtype).min
        n = np.iinfo(data.dtype).max
    data_f = data.astype(float)
    data_f -= m
    data_f /= (n-m)
    data_f *= d
    data_f = np.round(data_f)
    data_f /= d
    data_f *= (n-m)
    data_f += m
    return data_f.astype(data.dtype)


def decymacja(data, n, fs):
    data_d = data[::n]

    return data_d, fs/n

def interpolacja(data, Fs, new_size, metode="non_lin"):
    tm = data.size/Fs
    t = np.arange(0,tm,1/Fs)
    t1 = np.arange(0,tm,1/new_size)
    # t = np.linspace(0, 1/Fs, tm)
    # t1 = np.linspace(0, 1/new_size, tm)

    if metode=="lin":
        metode_lin=interp1d(t,data, fill_value="extrapolate")
        y_lin = metode_lin(t1).astype(data.dtype)
        return y_lin, new_size, tm
    else:
        metode_nonlin = interp1d(t, data, kind='cubic', fill_value="extrapolate")
        y_nonlin = metode_nonlin(t1).astype(data.dtype)
        return y_nonlin, new_size, tm

def plotAudio(Signal,Fs,Name,TimeMargin=[0,0.02]):
    fsize=2**16
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.xlim(TimeMargin)
    plt.tight_layout(rect=[0, 0.03, 1, 1],h_pad=2)
    plt.title(Name)
    plt.xlabel('t')
    plt.plot(np.arange(0, Signal.shape[0]) / Fs, Signal)
    plt.subplot(2, 1, 2)
    plt.title('widmo')
    plt.xlabel('fs')
    plt.ylabel('dB')
    yf = scipy.fftpack.fft(Signal, fsize)
    plt.plot(np.arange(0, Fs / 2, Fs / fsize), 20 * np.log10(np.abs(yf[:fsize // 2])))
    plt.show()


data = np.round(np.linspace(0,255,255,dtype=np.uint8))
# data = np.round(np.linspace(np.iinfo(np.int32).min,np.iinfo(np.int32).max,1000,dtype=np.int32))
# data = np.linspace(-1,1,10000)
post_data = kwant(data,2)
print(data)
print(post_data)

# plt.plot(data,post_data)
# plt.show()

# print(decymacja(data,10))

# pliki
# data1, Fs = sf.read('SM_Lab05/sin_8000Hz.wav', dtype='float32')
# tm=[0,0.03]
# tm_kwant=[0,0.002]
# suf = "sin_8000Hz"

# data1, Fs = sf.read('SM_Lab05/sin_440Hz.wav', dtype='float32')
# tm=[0,0.01]
# tm_kwant=[0,0.006]
# suf = "sin_440Hz"

# data1, Fs = sf.read('SM_Lab05/sin_60Hz.wav', dtype='float32')
# tm=[0,0.04]
# tm_kwant=[0,0.05]
# suf = "sin_60Hz"

data1, Fs = sf.read('SM_Lab05/sin_combined.wav', dtype='float32')
tm=[0,0.02]
tm_kwant=[0,0.01]
suf = "sin_combined"

# name = "kwantyzacja " + suf
# bit = 4
# post_data = kwant(data1,bit)
# name1 = name + " bit=" + str(bit)
# plotAudio(post_data,Fs,name1,tm_kwant)
#
# bit = 8
# post_data = kwant(data1,bit)
# name1 = name + " bit=" + str(bit)
# plotAudio(post_data,Fs,name1,tm_kwant)
#
# bit = 16
# post_data = kwant(data1,bit)
# name1 = name + " bit=" + str(bit)
# plotAudio(post_data,Fs,name1,tm_kwant)
#
# bit = 24
# post_data = kwant(data1,bit)
# name1 = name + " bit=" + str(bit)
# plotAudio(post_data,Fs,name1,tm_kwant)

# name = "decymacja " + suf
# out_data, fs = decymacja(data1,24,Fs)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# out_data, fs = decymacja(data1,12,Fs)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# out_data, fs = decymacja(data1,6,Fs)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# out_data, fs = decymacja(data1,3,Fs)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# out_data, fs = decymacja(data1,2,Fs)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# out_data, fs = decymacja(data1,1,Fs)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)


# name = "interpolacja lin " + suf
# out_data, fs ,t1 = interpolacja(data1,Fs,2000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,2000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs ,t1= interpolacja(data1,Fs,4000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs ,t1= interpolacja(data1,Fs,4000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,8000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,8000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,16000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,16000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,24000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,24000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,41000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,41000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,16950,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs,t1 = interpolacja(data1,Fs,16950)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja lin " + suf
# out_data, fs ,t1= interpolacja(data1,Fs,48000,"lin")
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)
#
# name = "interpolacja non_lin " + suf
# out_data, fs ,t1= interpolacja(data1,Fs,48000)
# name1 = name + " fs=" + str(fs) + " Hz"
# plotAudio(out_data,fs,name1,tm)

# data2, Fs = sf.read('SM_Lab05/sing_high1.wav', dtype='float32')
# data2, Fs = sf.read('SM_Lab05/sing_medium1.wav', dtype='float32')
data2, Fs = sf.read('SM_Lab05/sing_low1.wav', dtype='float32')

sd.play(data2, Fs)
sd.wait()
time.sleep(0.5)

# bit=4
# post_data = kwant(data2,bit)
# sd.play(post_data, Fs)
# sd.wait()
# time.sleep(0.5)
#
# bit=8
# post_data = kwant(data2,bit)
# sd.play(post_data, Fs)
# sd.wait()
# time.sleep(0.5)
#
# bit=16
# post_data = kwant(data2,bit)
# sd.play(post_data, Fs)
# sd.wait()
# time.sleep(0.5)
#
# bit=24
# post_data = kwant(data2,bit)
# sd.play(post_data, Fs)
# sd.wait()
# time.sleep(0.5)


# out_data, fs = decymacja(data2,24,Fs)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs = decymacja(data2,12,Fs)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs = decymacja(data2,6,Fs)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs = decymacja(data2,3,Fs)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs = decymacja(data2,2,Fs)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)



# out_data, fs,t1 = interpolacja(data2,Fs,2000)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,2000,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,4000)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,4000,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,8000)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,8000,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,16000)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,16000,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,24000)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,24000,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,41000)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,41000,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,16950)
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
#
# out_data, fs,t1 = interpolacja(data2,Fs,16950,"lin")
# sd.play(out_data, fs)
# sd.wait()
# time.sleep(0.5)
















