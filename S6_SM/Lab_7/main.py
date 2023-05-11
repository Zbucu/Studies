import numpy as np
import matplotlib.pyplot as plt
import scipy
import soundfile as sf
import sounddevice as sd

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

def ALaw_encode(data):
    A = 87.6
    out_data = data.copy()
    idx1 = np.abs(data) < 1/A
    idx2 = np.logical_not(idx1)
    out_data[idx1] = A*np.abs(data[idx1])/(1+np.log(A))*np.sign(data[idx1])
    out_data[idx2] = (1+np.log(A*np.abs(data[idx2])))/(1+np.log(A))*np.sign(data[idx2])
    return out_data

def ALaw_decode(data):
    A = 87.6
    out_data = data.copy()
    idx1 = np.abs(data) < 1 /(1+np.log(A))
    idx2 = np.logical_not(idx1)
    out_data[idx1] = np.abs(data[idx1])*(1+np.log(A))/A*np.sign(data[idx1])
    out_data[idx2] = np.exp(np.abs(data[idx2])*(1+np.log(A))-1)/A*np.sign(data[idx2])
    return out_data

def MuLaw_encode(data):
    mu = 255
    out_data = data.copy()
    out_data = np.sign(data)*np.log(1+mu*np.abs(data))/np.log(1+mu)
    return out_data

def MuLaw_decode(data):
    mu = 255
    out_data = data.copy()
    out_data = np.sign(data)*1/mu*(np.power(1+mu,np.abs(data))-1)
    return out_data

def DPCM_compress(x,bit):
    y=np.zeros(x.shape)
    e=0
    for i in range(0,x.shape[0]):
        y[i]=kwant(x[i]-e,bit)
        e+=y[i]
    return y

def DPCM_decompress(y):
    x = np.zeros(y.shape)
    e=0
    for i in range(0,y.shape[0]):
        x[i] = y[i] +e
        e= x[i]
    return x

def DPCM_compress_predict(x,bit,predictor,n):
    y=np.zeros(x.shape)
    xp=np.zeros(x.shape)
    e=0
    for i in range(1,x.shape[0]):
        y[i]=kwant(x[i]-e,bit)
        xp[i]=y[i]+e
        idx=(np.arange(i-n,i,1,dtype=int)+1)
        idx=np.delete(idx,idx<0)
        e=predictor(xp[idx])
    return y

def DPCM_decompress_predict(y,predictor,n):
    x = np.zeros(y.shape)
    e=0
    for i in range(0,y.shape[0]):
        x[i] = y[i] +e
        e= x[i]
        idx = (np.arange(i - n, i, 1, dtype=int) + 1)
        idx = np.delete(idx, idx < 0)
        e = predictor(x[idx])
    return x

x=np.linspace(-1,1,1000)
y=0.9*np.sin(np.pi*x*4)

# plt.subplot(2,1,1)
# plt.plot(x, y)
# plt.subplot(2,1,2)
# plt.plot(x, ALaw_decode(kwant(ALaw_encode(y),8)))
# plt.show()
#
# plt.subplot(2,1,1)
# plt.plot(x, y)
# plt.subplot(2,1,2)
# plt.plot(x, MuLaw_decode(kwant(MuLaw_encode(y),8)))
# plt.show()
#
# plt.subplot(2,1,1)
# plt.plot(x, y)
# plt.subplot(2,1,2)
# plt.plot(x, DPCM_decompress(DPCM_compress(y,8)))
# plt.show()
#
# plt.subplot(2,1,1)
# plt.plot(x, DPCM_compress(y,8))
# plt.subplot(2,1,2)
# plt.plot(x, DPCM_decompress_predict(DPCM_compress_predict(y,8,np.mean,3),np.mean,3))
# plt.show()


data, Fs = sf.read('sing_medium1.wav', dtype='float32')

sd.play(data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,8,np.mean,3)
sd.play(post_data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,7,np.mean,3)
sd.play(post_data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,6,np.mean,3)
sd.play(post_data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,5,np.mean,3)
sd.play(post_data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,4,np.mean,3)
sd.play(post_data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,3,np.mean,3)
sd.play(post_data, Fs)
sd.wait()

post_data = DPCM_compress_predict(data,2,np.mean,3)
sd.play(post_data, Fs)
sd.wait()