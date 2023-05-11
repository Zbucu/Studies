import numpy as np
import matplotlib.pyplot as plt

def imgToFloat(img):
    if np.issubdtype(img.dtype,np.floating):
        return img
    else:
        return img/255.0
def Paleta(N):
    paleta = np.linspace(0, 1, N).reshape(N, 1)
    return paleta




def colorFit(pixel,Pallet):
    return Pallet[np.argmin(np.linalg.norm(Pallet - pixel,axis=1))]

def kwant_colorFit(img, Pallet):
    out_img = img.copy()
    for w in range(out_img.shape[0]):
        for k in range(out_img.shape[1]):
            out_img[w, k] = colorFit(img[w, k], Pallet)
    return out_img

def dither_rand(img):
    out_img = img.copy()
    if (len(img.shape) < 3):
        r=np.random.rand(img.shape[0],img.shape[1])
    else:
        r = np.random.rand(img.shape[0], img.shape[1],3)
    # print(out_img>=r)
    out_img = out_img>=r
    out_img = out_img * 1.0
    return out_img
    # out_img = img.copy()
    # r = np.random.rand(img.shape[0], img.shape[1])
    # out_img = out_img >= r
    # return out_img * 1.0

def dither_organised(img, paleta):
    # M2 = (1/16) * np.matrix('0,8,2,10; 12,4,14,6; 3,11,1,9; 15,7,13,5')



    # M1 =  np.array([[0,2],[3,1]])
    M2 = np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])
    M_pre = ((M2+1) / ((2*2)**2)) - 0.5
    out_img = img.copy()
    for w in range(out_img.shape[0]):
        for k in range(out_img.shape[1]):
            out_img[w,k] = colorFit(img[w,k] + 1 * M_pre[w%(2*2), k%(2*2)],paleta)
    return out_img

def dither_Floyd_Steinberg(img,paleta):
    out_img = img.copy()
    for y in range(out_img.shape[1]):
        for x in range(out_img.shape[0]):
            oldpixel = out_img[x, y].copy()
            newpixel = colorFit(oldpixel,paleta)
            out_img[x, y] = newpixel
            quant_error = oldpixel - newpixel
            if x < out_img.shape[0] - 1 and y < out_img.shape[1] - 1:
                out_img[x + 1, y + 1] = out_img[x + 1, y + 1] + quant_error * 1 / 16
            if x < out_img.shape[0] - 1:
                out_img[x + 1, y] = out_img[x + 1, y] + quant_error * 7 / 16
            if y < out_img.shape[1] - 1:
                out_img[x - 1, y + 1] = out_img[x - 1, y + 1] + quant_error * 3 / 16
                out_img[x, y + 1] = out_img[x, y + 1] + quant_error * 5 / 16

    return out_img

paleta = Paleta(3)
print(colorFit(0.43,paleta)) # 0.5
print(colorFit(0.66,paleta)) # ?
print(colorFit(0.8,paleta)) # ?

pallet8 = np.array([
        [0.0, 0.0, 0.0,],
        [0.0, 0.0, 1.0,],
        [0.0, 1.0, 0.0,],
        [0.0, 1.0, 1.0,],
        [1.0, 0.0, 0.0,],
        [1.0, 0.0, 1.0,],
        [1.0, 1.0, 0.0,],
        [1.0, 1.0, 1.0,],
])

pallet16 =  np.array([
        [0.0, 0.0, 0.0,],
        [0.0, 1.0, 1.0,],
        [0.0, 0.0, 1.0,],
        [1.0, 0.0, 1.0,],
        [0.0, 0.5, 0.0,],
        [0.5, 0.5, 0.5,],
        [0.0, 1.0, 0.0,],
        [0.5, 0.0, 0.0,],
        [0.0, 0.0, 0.5,],
        [0.5, 0.5, 0.0,],
        [0.5, 0.0, 0.5,],
        [1.0, 0.0, 0.0,],
        [0.75, 0.75, 0.75,],
        [0.0, 0.5, 0.5,],
        [1.0, 1.0, 1.0,],
        [1.0, 1.0, 0.0,]
])


print(colorFit(np.array([0.25,0.25,0.5]),pallet8))
print(colorFit(np.array([0.25,0.25,0.5]),pallet16))



# 08 - 1 bit

# img2 = plt.imread('SM_Lab04/0008.png')
# img2 = img2[:,:,0:3]
# img2 = imgToFloat(img2)
#
# plt.subplot(2,3,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(2,3,2)
# plt.title('Progowanie 1 bit')
# img2_kwant = kwant_colorFit(imgToFloat(img2),Paleta(2))
# plt.imshow(img2_kwant)
#
#
# plt.subplot(2,3,3)
# plt.title('1 bit - losowy')
# new_img2 = dither_rand(imgToFloat(img2[:,:,0]))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
#
# plt.subplot(2,3,4)
# plt.title('1 bit - zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),Paleta(2))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
# plt.subplot(2,3,5)
# plt.title('1 bit - Floyd-Steinberg')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Paleta(2))
# plt.imshow(new_img2,cmap=plt.cm.gray)
# plt.show()
#
# # 08 - 2 bity
#
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Progowanie 2 bity')
# img2_kwant = kwant_colorFit(imgToFloat(img2),Paleta(4))
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('2 bit - zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),Paleta(4))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
# plt.subplot(1,4,4)
# plt.title('2 bit - Floyd-Steinberg')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Paleta(4))
# plt.imshow(new_img2,cmap=plt.cm.gray)
# plt.show()
#
# # 08 - 4 bity
#
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Progowanie 4 bity')
# img2_kwant = kwant_colorFit(imgToFloat(img2),Paleta(16))
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('4 bit - zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),Paleta(16))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
# plt.subplot(1,4,4)
# plt.title('4 bit - Floyd-Steinberg')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Paleta(16))
# plt.imshow(new_img2,cmap=plt.cm.gray)
# plt.show()
#
# # 09 - 1 bit
#
# img2 = plt.imread('SM_Lab04/0009.png')
# img2 = img2[:,:,0:3]
# img2 = imgToFloat(img2)
#
# plt.subplot(2,3,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(2,3,2)
# plt.title('Progowanie 1 bit')
# img2_kwant = kwant_colorFit(imgToFloat(img2),Paleta(2))
# plt.imshow(img2_kwant)
#
#
# plt.subplot(2,3,3)
# plt.title('1 bit - losowy')
# new_img2 = dither_rand(imgToFloat(img2[:,:,0]))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
#
# plt.subplot(2,3,4)
# plt.title('1 bit - zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),Paleta(2))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
# plt.subplot(2,3,5)
# plt.title('1 bit - Floyd-Steinberg')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Paleta(2))
# plt.imshow(new_img2,cmap=plt.cm.gray)
# plt.show()
#
# # 09 - 2 bity
#
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Progowanie 2 bity')
# img2_kwant = kwant_colorFit(imgToFloat(img2),Paleta(4))
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('2 bit - zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),Paleta(4))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
# plt.subplot(1,4,4)
# plt.title('2 bit - Floyd-Steinberg')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Paleta(4))
# plt.imshow(new_img2,cmap=plt.cm.gray)
# plt.show()
#
# # 09 - 4 bity
#
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Progowanie 4 bity')
# img2_kwant = kwant_colorFit(imgToFloat(img2),Paleta(16))
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('4 bit - zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),Paleta(16))
# plt.imshow(new_img2,cmap=plt.cm.gray)
#
# plt.subplot(1,4,4)
# plt.title('4 bit - Floyd-Steinberg')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Paleta(16))
# plt.imshow(new_img2,cmap=plt.cm.gray)
# plt.show()
#
# # 11 - pallet 8
#
# img2 = plt.imread('SM_Lab04/0011.jpg')
# img2 = imgToFloat(img2)
#
# plt.suptitle('8 kolorow')
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Obraz z pikselami dopasowanymi do palety')
# img2_kwant = kwant_colorFit(imgToFloat(img2),pallet8)
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('dithering zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),pallet8)
# plt.imshow(new_img2)
#
# plt.subplot(1,4,4)
# plt.title('dithering Floyd-Steinberga')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),pallet8)
# plt.imshow(new_img2)
# plt.show()
#
# # 11 pallet 16
#
# plt.suptitle('16 kolorow')
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Obraz z pikselami dopasowanymi do palety')
# img2_kwant = kwant_colorFit(imgToFloat(img2),pallet16)
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('dithering zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),pallet16)
# plt.imshow(new_img2)
#
# plt.subplot(1,4,4)
# plt.title('dithering Floyd-Steinberga')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),pallet16)
# plt.imshow(new_img2)
# plt.show()
#
#
# # 16 - pallet 8
#
# img2 = plt.imread('SM_Lab04/0016.jpg')
# img2 = imgToFloat(img2)
#
# plt.suptitle('8 kolorow')
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Obraz z pikselami dopasowanymi do palety')
# img2_kwant = kwant_colorFit(imgToFloat(img2),pallet8)
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('dithering zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),pallet8)
# plt.imshow(new_img2)
#
# plt.subplot(1,4,4)
# plt.title('dithering Floyd-Steinberga')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),pallet8)
# plt.imshow(new_img2)
# plt.show()
#
# # 16 pallet 16
#
# plt.suptitle('16 kolorow')
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Obraz z pikselami dopasowanymi do palety')
# img2_kwant = kwant_colorFit(imgToFloat(img2),pallet16)
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('dithering zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),pallet16)
# plt.imshow(new_img2)
#
# plt.subplot(1,4,4)
# plt.title('dithering Floyd-Steinberga')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),pallet16)
# plt.imshow(new_img2)
# plt.show()
#
#
# # 13 - pallet 8
#
# img2 = plt.imread('SM_Lab04/0013.jpg')
# img2 = imgToFloat(img2)
#
# plt.suptitle('8 kolorow')
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Obraz z pikselami dopasowanymi do palety')
# img2_kwant = kwant_colorFit(imgToFloat(img2),pallet8)
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('dithering zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),pallet8)
# plt.imshow(new_img2)
#
# plt.subplot(1,4,4)
# plt.title('dithering Floyd-Steinberga')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),pallet8)
# plt.imshow(new_img2)
# plt.show()
#
# # 13 pallet 16
#
# plt.suptitle('16 kolorow')
# plt.subplot(1,4,1)
# plt.title('oryginal')
# plt.imshow(img2)
#
# plt.subplot(1,4,2)
# plt.title('Obraz z pikselami dopasowanymi do palety')
# img2_kwant = kwant_colorFit(imgToFloat(img2),pallet16)
# plt.imshow(img2_kwant)
#
#
# plt.subplot(1,4,3)
# plt.title('dithering zorganizowany')
# new_img2 = dither_organised(imgToFloat(img2),pallet16)
# plt.imshow(new_img2)
#
# plt.subplot(1,4,4)
# plt.title('dithering Floyd-Steinberga')
# new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),pallet16)
# plt.imshow(new_img2)
# plt.show()




Moja_paleta = np.array([[0.8745098 , 0.87843137, 0.90196078],
                        [0.45098039, 0.39607843, 0.39215686],
                        [0.59215686, 0.5372549 , 0.54509804],
                        [0.29411765, 0.24705882, 0.23921569],
                        [0.11372549, 0.0745098 , 0.07058824]])

img2 = plt.imread('SM_Lab04/0015.jpg')
img2 = imgToFloat(img2)

plt.suptitle('5 kolorow')
plt.subplot(1,4,1)
plt.title('oryginal')
plt.imshow(img2)

plt.subplot(1,4,2)
plt.title('Obraz z pikselami dopasowanymi do palety')
img2_kwant = kwant_colorFit(imgToFloat(img2),Moja_paleta)
plt.imshow(img2_kwant)


plt.subplot(1,4,3)
plt.title('dithering zorganizowany')
new_img2 = dither_organised(imgToFloat(img2),Moja_paleta)
plt.imshow(new_img2)

plt.subplot(1,4,4)
plt.title('dithering Floyd-Steinberga')
new_img2 = dither_Floyd_Steinberg(imgToFloat(img2),Moja_paleta)
plt.imshow(new_img2)
plt.show()