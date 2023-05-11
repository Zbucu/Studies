import sys
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj,np.ndarray):
        size=obj.nbytes
    elif isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def rozny(x,it,r_128):
    for i in range(it,len(x)):
        if r_128==True:
            if x[it]!=x[i] or i-it==128:
                return i
        else:
            if x[it]!=x[i]:
                return i
    return len(x)

def jednakowy(x,it,r_128):
    for i in range(it,len(x)-1):
        if r_128 == True:
            if x[i]==x[i+1] or i-it==128:
                return i
        else:
            if x[i]==x[i+1]:
                return i
    return len(x)



def RLE_encode(data):
    x = np.array([len(data.shape)])
    x = np.concatenate([x, data.shape])
    data = data.flatten()
    out_data = np.zeros(2*len(data))
    j = 0
    i=0
    # with tqdm(total=100) as pbar:
    while i in range(len(data)):
        new_i = rozny(data,i,False)
        out_data[j] = new_i - i
        out_data[j+1] = data[i]
        j+=2
        i = new_i
            # pbar.update(100/len(data))
    # pbar.close()

    out_data = out_data[:j+1]
    # for i in range(2,len(out_data)):
    #     if out_data[i]==0 and out_data[i+1] == 0:
    #         if data[-1]==0:
    #             out_data = out_data[:i+1]
    #         else:
    #             out_data = out_data[:i]
    #         break
    out_data = np.concatenate([x,out_data])
    return out_data.astype(int)

def RLE_decode(data):
    shape = data[1:int(data[0]+1)]
    i = data[0]+1
    out_data = np.zeros(shape)
    out_data = out_data.flatten()
    k=0
    with tqdm(total=100) as pbar:
        while i<len(data):
            for j in range(data[i]):
                out_data[k] = data[i+1]
                k+=1
            i+=2
            pbar.update(100/len(data)*2)
    pbar.close()
    out_data=out_data.reshape((shape))
    return out_data.astype(int)

def ByteRun_encode(data):
    x = np.array([len(data.shape)])
    x = np.concatenate([x, data.shape])
    data = data.flatten()
    out_data = np.zeros(2*len(data))
    j = 0
    i=0
    switch = jednakowy(data,i,False)<rozny(data,i,False)
    # with tqdm(total=100) as pbar:
    while i in range(len(data)):
        if switch:
            new_i = rozny(data,i,True)
            out_data[j]= -(new_i-i-1)
            out_data[j+1] = data[i]
            j += 2
        else:
            new_i = jednakowy(data,i,True)
            out_data[j] = new_i-i-1
            for k in range(new_i-i):
                out_data[j+k+1] = data[i+k]
            j += new_i-i+1
        i = new_i
        # pbar.update(100/len(data))
        switch = jednakowy(data, i,False) < rozny(data, i,False)
    # pbar.close()
    out_data = out_data[:j]
    # for i in range(2,len(out_data)):
    #     if data[-2] == data[-3] and data[-2]!=0 and data[-1] == 0:
    #         if out_data[i] == 0 and out_data[i + 1] == 0 and out_data[i + 2] == 0:
    #             out_data = out_data[:i+2]
    #             break
    #     else:
    #         if out_data[i] == 0 and out_data[i + 1] == 0:
    #             if data[-1] == 0:
    #                 out_data = out_data[:i + 1]
    #             else:
    #                 out_data = out_data[:i]
    #             break
    out_data = np.concatenate([x, out_data])
    return out_data.astype(int)

def ByteRun_decode(data):
    shape = data[1:int(data[0] + 1)]
    i = data[0] + 1
    out_data = np.zeros(shape)
    out_data = out_data.flatten()
    k=0
    with tqdm(total=100) as pbar:
        while i < len(data):
            if(data[i]<0):
                for j in range((-data[i])+1):
                    out_data[k] = data[i+1]
                    k+=1
                i+=2
                pbar.update(100 / len(data) * 2)
            else:
                for j in range(data[i]+1):
                    out_data[k]=data[i+j+1]
                    k+=1
                i+=data[i]+2

    pbar.close()
    out_data = out_data.reshape((shape))
    return out_data.astype(int)



# data = np.array([1,1,1,1,2,1,1,1,1,2,1,1,1,1])
# data = np.arange(0,521,1)
# data = np.array([[1,1,1,1,2,1,1],[1,1,2,1,1,1,1]])

# img = plt.imread('tech_draw_2.jpg')
# data=img.astype(int)
#
# rle_code = RLE_encode(data)
# rle_data = RLE_decode(rle_code)
#
#
# print("Identyczne:", np.array_equal(rle_data,data))
# print("stopien kompresji:", get_size(data)/get_size(rle_code))
# print("procent oryginalu:", get_size(rle_code)/get_size(data)*100, "%")
#
#
#
# plt.subplot(1,2,1)
# plt.title("Oryginal")
# plt.imshow(data)
#
# plt.subplot(1,2,2)
# plt.title("RLE po dekompresji")
# plt.imshow(rle_data)
# plt.show()
#
# img = plt.imread('dokument_2.jpg')
# data=img.astype(int)
#
# rle_code = RLE_encode(data)
# rle_data = RLE_decode(rle_code)
#
# print("Identyczne:", np.array_equal(rle_data,data))
# print("stopien kompresji:", get_size(data)/get_size(rle_code))
# print("procent oryginalu:", get_size(rle_code)/get_size(data)*100, "%")
#
# plt.subplot(1,2,1)
# plt.title("Oryginal")
# plt.imshow(data)
#
# plt.subplot(1,2,2)
# plt.title("RLE po dekompresji")
# plt.imshow(rle_data)
# plt.show()

# img = plt.imread('kolor.jpg')
# data=img.astype(int)
#
# rle_code = RLE_encode(data)
# rle_data = RLE_decode(rle_code)
#
# print("Identyczne:", np.array_equal(rle_data,data))
# print("stopien kompresji:", get_size(data)/get_size(rle_code))
# print("procent oryginalu:", get_size(rle_code)/get_size(data)*100, "%")
#
# plt.subplot(1,2,1)
# plt.title("Oryginal")
# plt.imshow(data)
#
# plt.subplot(1,2,2)
# plt.title("RLE po dekompresji")
# plt.imshow(rle_data)
# plt.show()
#
#
# img = plt.imread('tech_draw_2.jpg')
# data=img.astype(int)
#
# byterun_code = ByteRun_encode(data)
# byterun_data = ByteRun_decode(byterun_code)
#
# print("Identyczne:", np.array_equal(byterun_data,data))
# print("stopien kompresji:", get_size(data)/get_size(byterun_code))
# print("procent oryginalu:", get_size(byterun_code)/get_size(data)*100, "%")
#
# plt.subplot(1,2,1)
# plt.title("Oryginal")
# plt.imshow(data)
#
# plt.subplot(1,2,2)
# plt.title("ByteRun po dekompresji")
# plt.imshow(byterun_data)
# plt.show()

img = plt.imread('dokument.jpg')
data=img.astype(int)

byterun_code = ByteRun_encode(data)
byterun_data = ByteRun_decode(byterun_code)

print("Identyczne:", np.array_equal(byterun_data,data))
print("stopien kompresji:", get_size(data)/get_size(byterun_code))
print("procent oryginalu:", get_size(byterun_code)/get_size(data)*100, "%")

plt.subplot(1,2,1)
plt.title("Oryginal")
plt.imshow(data)

plt.subplot(1,2,2)
plt.title("ByteRun po dekompresji")
plt.imshow(byterun_data)
plt.show()

img = plt.imread('kolor.jpg')
data=img.astype(int)

byterun_code = ByteRun_encode(data)
byterun_data = ByteRun_decode(byterun_code)

print("Identyczne:", np.array_equal(byterun_data,data))
print("stopien kompresji:", get_size(data)/get_size(byterun_code))
print("procent oryginalu:", get_size(byterun_code)/get_size(data)*100, "%")

plt.subplot(1,2,1)
plt.title("Oryginal")
plt.imshow(data)

plt.subplot(1,2,2)
plt.title("ByteRun po dekompresji")
plt.imshow(byterun_data)
plt.show()

