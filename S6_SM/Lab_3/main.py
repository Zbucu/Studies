import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

# img= np.zeros((3,3,3),dtype=np.uint8)
# img[1,1,:]=255

# plt.imshow(img)
# plt.show()

# x= np.array([1,2,1])
# x=np.array((x,x,x))
# print(x)
# y= np.array([2,1]).transpose()
# print(y)
# y=np.array((y,y,y))
# print(y.transpose())
# print(x.T*y)

# wx = np.array([1,2,3,4])
# wy = 4 - np.abs(np.arange(-3, 519 - 516))
# wxy = np.ix_(wx,wy)
# print(np.sum(wxy))
# print(wxy[0][0])

def imgToUInt8(img):
    if np.issubdtype(img.dtype,np.unsignedinteger):
        return img
    else:
        img*=255
        img = img.astype('uint8')
        return img

def imgToFloat(img):
    if np.issubdtype(img.dtype,np.floating):
        return img
    else:
        img/255.0
        return img

def scale_nn(img, scale):
    if (len(img.shape) < 3):
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int)))
    else:
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int),3))

    X = np.linspace(0, img.shape[0]-1, img_scaled.shape[0])
    Y = np.linspace(0, img.shape[1]-1, img_scaled.shape[1])
    for i in range(0, img_scaled.shape[0]-1):
        for j in range(0, img_scaled.shape[1]-1):
            img_scaled[i,j]=img[np.round(X[i]).astype(int), np.round(Y[j]).astype(int)]

    return img_scaled

def scale_interpolation(img, scale):
    if (len(img.shape) < 3):
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int)))
    else:
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int),3))

    X = np.linspace(0, img.shape[0]-1, img_scaled.shape[0])
    Y = np.linspace(0, img.shape[1]-1, img_scaled.shape[1])

    for i in range(0, img_scaled.shape[0]):
        for j in range(0, img_scaled.shape[1]):
            f00 = img[np.floor(X[i]).astype(int),np.floor(Y[j]).astype(int)]
            f01 = img[np.floor(X[i]).astype(int),np.ceil(Y[j]).astype(int)]
            f10 = img[np.ceil(X[i]).astype(int), np.floor(Y[j]).astype(int)]
            f11 = img[np.ceil(X[i]).astype(int),np.ceil(Y[j]).astype(int)]
            x = X[i] - np.floor(X[i])
            y = Y[j] - np.floor(Y[j])

            img_scaled[i,j] = f00*(1-x)*(1-y) + f10*x*(1-y) + f01*(1-x)*y + f11*x*y

    return img_scaled

def scale_mean(img, scale):
    if (len(img.shape) < 3):
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int)))
    else:
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int),3))

    X = np.linspace(0, img.shape[0]-1, img_scaled.shape[0])
    Y = np.linspace(0, img.shape[1] - 1, img_scaled.shape[1])
    print(X)
    print(Y)


    for i in range(0, img_scaled.shape[0]):
        for j in range(0, img_scaled.shape[1]):
            if i < 3:
                ix = np.round(X[i] + np.arange(-i, 4))
            elif i > img_scaled.shape[0]-4:
                ix = np.round(X[i] + np.arange(-3,  img_scaled.shape[0] - i))
            else:
                ix = np.round(X[i] + np.arange(-3, 4))

            if j < 3:
                iy = np.round(Y[j] + np.arange(-j, 4))
            elif j > img_scaled.shape[1] - 4:
                iy = np.round(Y[j] + np.arange(-3, img_scaled.shape[1] - j))
            else:
                iy = np.round(Y[j] + np.arange(-3, 4))

            # print(np.ix_(ix,iy))
            # img_scaled[i,j] = (img[np.round(np.mean(ix)).astype(int),np.round(np.mean(iy)).astype(int)])
            img_scaled[i,j]=np.mean(np.mean(img[np.ix_(np.round(ix).astype(int),np.round(iy).astype(int))],axis=0),axis=0)

    return img_scaled


def scale_median(img, scale):
    if (len(img.shape) < 3):
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int)))
    else:
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int),3))

    X = np.linspace(0, img.shape[0]-1, img_scaled.shape[0])
    Y = np.linspace(0, img.shape[1] - 1, img_scaled.shape[1])


    for i in range(0, img_scaled.shape[0]):
        for j in range(0, img_scaled.shape[1]):
            if i < 3:
                ix = np.round(X[i] + np.arange(-i, 4))
            elif i > img_scaled.shape[0]-4:
                ix = np.round(X[i] + np.arange(-3,  img_scaled.shape[0] - i))
            else:
                ix = np.round(X[i] + np.arange(-3, 4))

            if j < 3:
                iy = np.round(Y[j] + np.arange(-j, 4))
            elif j > img_scaled.shape[1] - 4:
                iy = np.round(Y[j] + np.arange(-3, img_scaled.shape[1] - j))
            else:
                iy = np.round(Y[j] + np.arange(-3, 4))

            img_scaled[i,j]=np.median(np.median(img[np.ix_(np.round(ix).astype(int),np.round(iy).astype(int))],axis=0),axis=0)

    return img_scaled

def scale_weight(img, scale):
    if (len(img.shape) < 3):
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int)))
    else:
        img_scaled = np.zeros((np.ceil(img.shape[0] * scale).astype(int), np.ceil(img.shape[1] * scale).astype(int),3))

    X = np.linspace(0, img.shape[0]-1, img_scaled.shape[0])
    Y = np.linspace(0, img.shape[1] - 1, img_scaled.shape[1])

    weights = np.array([0.8,1.2,0.9])

    for i in range(0, img_scaled.shape[0]):
        for j in range(0, img_scaled.shape[1]):
            if i < 3:
                ix = (np.round(X[i] + np.arange(-i, 4))).astype(int)
                wx = 4 - np.abs(np.arange(-i, 4))
            elif i > img_scaled.shape[0]-4:
                ix = (np.round(X[i] + np.arange(-3,  img_scaled.shape[0] - i))).astype(int)
                wx = 4 - np.abs(np.arange(-3,  img_scaled.shape[0] - i))
            else:
                ix = (np.round(X[i] + np.arange(-3, 4))).astype(int)
                wx = 4 - np.abs(np.arange(-3,4))

            if j < 3:
                iy = (np.round(Y[j] + np.arange(-j, 4))).astype(int)
                wy = 4 - np.abs(np.arange(-j, 4))
            elif j > img_scaled.shape[1] - 4:
                iy = (np.round(Y[j] + np.arange(-3, img_scaled.shape[1] - j))).astype(int)
                wy = 4 - np.abs(np.arange(-3, img_scaled.shape[1] - j))
            else:
                iy = (np.round(Y[j] + np.arange(-3, 4))).astype(int)
                wy = 4 - np.abs(np.arange(-3, 4))

            # xx = np.multiply(ix,wx)
            # yy = np.multiply(iy,wy)
            # wxy = np.ix_(wx,wy)
            # print(wxy)
            # print(img_scaled.shape[1])
            # print(j)

            sh = (len(wx),len(wy))
            temp = len(wx)
            wx = np.tile(wx,len(wy))
            wy = np.tile(wy,temp)

            wxy = np.reshape(wx*wy,sh)
            # aaaa = img[np.ix_(np.round(ix).astype(int), np.round(iy).astype(int))][:,:,0]

            if iy.size > ix.size:
                nrOfNeighbors = ix.size
            else:
                nrOfNeighbors = iy.size

            weights = np.random.rand(nrOfNeighbors)

            # img_scaled[i,j] = (img[np.round(np.sum(xx)/np.sum(wx)).astype(int),np.round(np.sum(yy)/np.sum(wy)).astype(int)])
            img_scaled[i, j][0] = (np.sum(np.multiply(img[np.ix_(np.round(ix).astype(int), np.round(iy).astype(int))][:,:,0], wxy)) / np.sum(wxy)).astype(int)
            img_scaled[i, j][1] = (np.sum(np.multiply(img[np.ix_(np.round(ix).astype(int), np.round(iy).astype(int))][:, :, 1], wxy)) / np.sum(wxy)).astype(int)
            img_scaled[i, j][2] = (np.sum(np.multiply(img[np.ix_(np.round(ix).astype(int), np.round(iy).astype(int))][:, :, 2], wxy)) / np.sum(wxy)).astype(int)
            # img_scaled[i, j][0] = (np.sum(np.multiply(img[ix[:nrOfNeighbors], iy[:nrOfNeighbors]][:,0], weights[:nrOfNeighbors]))/np.sum(weights[:nrOfNeighbors])).astype(int)
            # img_scaled[i, j] = np.mean(np.mean(img[np.ix_(np.round(ix).astype(int), np.round(iy).astype(int))], axis=0),axis=0)

    return img_scaled

# cv_img1 = cv.imread('SM_Lab03/0004.jpg')
img1 = plt.imread('SM_Lab03/0004.jpg')
img1_1 = plt.imread('SM_Lab03/0002.jpg')

# nn 1

# plt.subplot(2,3,1)
# plt.title("Oryginal")
# plt.xlim(right=30)
# plt.ylim(bottom=30)
# plt.imshow(img1)
#
# plt.subplot(2,3,4)
# e1 = cv.Canny(img1,100,200)
# plt.xlim(right=30)
# plt.ylim(bottom=30)
# plt.imshow(e1,cmap = 'gray')
#
# plt.subplot(2,3,2)
# plt.title("Najblizszy sasiad 500%")
# new_img1_1 = scale_nn(img1,5)
# plt.xlim(right=150)
# plt.ylim(bottom=150)
# plt.imshow(new_img1_1.astype(np.uint8))
# # plt.show()
#
# plt.subplot(2,3,5)
# e2 = cv.Canny(new_img1_1.astype(np.uint8),100,200)
# plt.xlim(right=150)
# plt.ylim(bottom=150)
# plt.imshow(e2,cmap = 'gray')
#
# plt.subplot(2,3,3)
# plt.title("Najblizszy sasiad 150%")
# new_img1_2 = scale_nn(img1,1.5)
# plt.xlim(right=45)
# plt.ylim(bottom=45)
# plt.imshow(new_img1_2.astype(np.uint8))
#
# plt.subplot(2,3,6)
# e3 = cv.Canny(new_img1_2.astype(np.uint8),100,200)
# plt.xlim(right=45)
# plt.ylim(bottom=45)
# plt.imshow(e3,cmap = 'gray')
# plt.show()
#
# # nn 2
#
# plt.subplot(2,3,1)
# plt.title("Oryginal")
# plt.xlim(left=60,right=90)
# plt.ylim(top=15,bottom=45)
# plt.imshow(img1_1)
#
# plt.subplot(2,3,4)
# e1 = cv.Canny(img1_1,100,200)
# plt.xlim(left=60,right=90)
# plt.ylim(top=15,bottom=45)
# plt.imshow(e1,cmap = 'gray')
#
# plt.subplot(2,3,2)
# plt.title("Najblizszy sasiad 500%")
# new_img1_1 = scale_nn(img1_1,5)
# plt.xlim(left=300,right=450)
# plt.ylim(top=75,bottom=225)
# plt.imshow(new_img1_1.astype(np.uint8))
# # plt.show()
#
# plt.subplot(2,3,5)
# e2 = cv.Canny(new_img1_1.astype(np.uint8),100,200)
# plt.xlim(left=300,right=450)
# plt.ylim(top=75,bottom=225)
# plt.imshow(e2,cmap = 'gray')
#
# plt.subplot(2,3,3)
# plt.title("Najblizszy sasiad 150%")
# new_img1_2 = scale_nn(img1_1,1.5)
# plt.xlim(left=90,right=135)
# plt.ylim(top=22.5,bottom=67.5)
# plt.imshow(new_img1_2.astype(np.uint8))
#
# plt.subplot(2,3,6)
# e3 = cv.Canny(new_img1_2.astype(np.uint8),100,200)
# plt.xlim(left=90,right=135)
# plt.ylim(top=22.5,bottom=67.5)
# plt.imshow(e3,cmap = 'gray')
# plt.show()
#
# #interpolacja 1
#
# plt.subplot(2,3,1)
# plt.title("Oryginal")
# plt.xlim(right=30)
# plt.ylim(bottom=30)
# plt.imshow(img1)
#
# plt.subplot(2,3,4)
# e1 = cv.Canny(img1,100,200)
# plt.xlim(right=30)
# plt.ylim(bottom=30)
# plt.imshow(e1,cmap = 'gray')
#
# plt.subplot(2,3,2)
# plt.title("Interpolacja 500%")
# new_img2_1 = scale_interpolation(img1,5)
# plt.xlim(right=150)
# plt.ylim(bottom=150)
# plt.imshow(new_img2_1.astype(np.uint8))
# # plt.show()
#
# plt.subplot(2,3,5)
# e2 = cv.Canny(new_img2_1.astype(np.uint8),100,200)
# plt.xlim(right=150)
# plt.ylim(bottom=150)
# plt.imshow(e2,cmap = 'gray')
#
# plt.subplot(2,3,3)
# plt.title("Interpolacja 150%")
# new_img2_2 = scale_interpolation(img1,1.5)
# plt.xlim(right=45)
# plt.ylim(bottom=45)
# plt.imshow(new_img2_2.astype(np.uint8))
#
# plt.subplot(2,3,6)
# e3 = cv.Canny(new_img2_2.astype(np.uint8),100,200)
# plt.xlim(right=45)
# plt.ylim(bottom=45)
# plt.imshow(e3,cmap = 'gray')
# plt.show()
#
# #interpolacja 2
#
# plt.subplot(2,3,1)
# plt.title("Oryginal")
# plt.xlim(left=60,right=90)
# plt.ylim(top=15,bottom=45)
# plt.imshow(img1_1)
#
# plt.subplot(2,3,4)
# e1 = cv.Canny(img1_1,100,200)
# plt.xlim(left=60,right=90)
# plt.ylim(top=15,bottom=45)
# plt.imshow(e1,cmap = 'gray')
#
# plt.subplot(2,3,2)
# plt.title("Interpolacja 500%")
# new_img2_1 = scale_interpolation(img1_1,5)
# plt.xlim(left=300,right=450)
# plt.ylim(top=75,bottom=225)
# plt.imshow(new_img2_1.astype(np.uint8))
# # plt.show()
#
# plt.subplot(2,3,5)
# e2 = cv.Canny(new_img2_1.astype(np.uint8),100,200)
# plt.xlim(left=300,right=450)
# plt.ylim(top=75,bottom=225)
# plt.imshow(e2,cmap = 'gray')
#
# plt.subplot(2,3,3)
# plt.title("Interpolacja 150%")
# new_img2_2 = scale_interpolation(img1_1,1.5)
# plt.xlim(left=90,right=135)
# plt.ylim(top=22.5,bottom=67.5)
# plt.imshow(new_img2_2.astype(np.uint8))
#
# plt.subplot(2,3,6)
# e3 = cv.Canny(new_img2_2.astype(np.uint8),100,200)
# plt.xlim(left=90,right=135)
# plt.ylim(top=22.5,bottom=67.5)
# plt.imshow(e3,cmap = 'gray')
# plt.show()




img2 = plt.imread('SM_Lab03/0005.jpg')
img2_2 = plt.imread('SM_Lab03/0007.jpg')

# srednia 1

# plt.subplot(2,3,1)
# plt.title("Oryginal")
# plt.xlim(right=500)
# plt.ylim(bottom=500)
# plt.imshow(img2)
# # plt.show()
#
# plt.subplot(2,3,4)
# e1 = cv.Canny(img2,100,200)
# plt.xlim(right=500)
# plt.ylim(bottom=500)
# plt.imshow(e1,cmap = 'gray')
#
# plt.subplot(2,3,2)
# plt.title("Srednia 5%")
# new_img3 = scale_mean(img2, 0.05)
# plt.xlim(right=25)
# plt.ylim(bottom=25)
# plt.imshow(new_img3.astype(np.uint8))
# # plt.show()
#
# plt.subplot(2,3,5)
# e2 = cv.Canny(new_img3.astype(np.uint8),100,200)
# plt.xlim(right=25)
# plt.ylim(bottom=25)
# plt.imshow(e2,cmap = 'gray')
#
# plt.subplot(2,3,3)
# plt.title("Srednia 20%")
# new_img4 = scale_mean(img2, 0.2)
# plt.xlim(right=100)
# plt.ylim(bottom=100)
# plt.imshow(new_img4.astype(np.uint8))
#
# plt.subplot(2,3,6)
# e3 = cv.Canny(new_img4.astype(np.uint8),100,200)
# plt.xlim(right=100)
# plt.ylim(bottom=100)
# plt.imshow(e3,cmap = 'gray')
# plt.show()

# #srednia 2

# plt.subplot(2,3,1)
# plt.title("Oryginal")
# plt.xlim(right=500)
# plt.ylim(bottom=500)
# plt.imshow(img2_2)
# # plt.show()
#
# plt.subplot(2,3,4)
# e1 = cv.Canny(img2_2,100,200)
# plt.xlim(right=500)
# plt.ylim(bottom=500)
# plt.imshow(e1,cmap = 'gray')
#
# plt.subplot(2,3,2)
# plt.title("Srednia 5%")
# new_img3 = scale_mean(img2_2, 0.05)
# plt.xlim(right=25)
# plt.ylim(bottom=25)
# plt.imshow(new_img3.astype(np.uint8))
# # plt.show()
#
# plt.subplot(2,3,5)
# e2 = cv.Canny(new_img3.astype(np.uint8),100,200)
# plt.xlim(right=25)
# plt.ylim(bottom=25)
# plt.imshow(e2,cmap = 'gray')
#
# plt.subplot(2,3,3)
# plt.title("Srednia 20%")
# new_img4 = scale_mean(img2_2, 0.2)
# plt.xlim(right=100)
# plt.ylim(bottom=100)
# plt.imshow(new_img4.astype(np.uint8))
#
# plt.subplot(2,3,6)
# e3 = cv.Canny(new_img4.astype(np.uint8),100,200)
# plt.xlim(right=100)
# plt.ylim(bottom=100)
# plt.imshow(e3,cmap = 'gray')
# plt.show()


# mediana 1

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2)

plt.subplot(2,3,4)
e1 = cv.Canny(img2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Mediana 5%")
new_img5 = scale_median(img2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img5.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img5.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Mediana 20%")
new_img6 = scale_median(img2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img6.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img6.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

#Mediana 2

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2_2)

plt.subplot(2,3,4)
e1 = cv.Canny(img2_2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Mediana 5%")
new_img5 = scale_median(img2_2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img5.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img5.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Mediana 20%")
new_img6 = scale_median(img2_2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img6.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img6.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

# nn zmniejszanie 1

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2)
# plt.show()

plt.subplot(2,3,4)
e1 = cv.Canny(img2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Najblizszy sasiad 5%")
new_img7_1 = scale_nn(img2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img7_1.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img7_1.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Najblizszy sasiad 20%")
new_img7_2 = scale_nn(img2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img7_2.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img7_2.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

# nn zmniejszanie 2

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2_2)
# plt.show()

plt.subplot(2,3,4)
e1 = cv.Canny(img2_2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Najblizszy sasiad 5%")
new_img7_1 = scale_nn(img2_2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img7_1.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img7_1.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Najblizszy sasiad 20%")
new_img7_2 = scale_nn(img2_2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img7_2.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img7_2.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

# interpolacja zmniejszanie 1

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2)
# plt.show()

plt.subplot(2,3,4)
e1 = cv.Canny(img2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Interpolacja 5%")
new_img8_1 = scale_interpolation(img2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img8_1.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img8_1.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Interpolacja 20%")
new_img8_2 = scale_nn(img2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img8_2.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img8_2.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

#interpolacja zmniejszanie 2

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2_2)
# plt.show()

plt.subplot(2,3,4)
e1 = cv.Canny(img2_2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Interpolacja 5%")
new_img8_1 = scale_interpolation(img2_2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img8_1.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img8_1.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Interpolacja 20%")
new_img8_2 = scale_nn(img2_2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img8_2.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img8_2.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

# wazona 1

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2)
# plt.show()

plt.subplot(2,3,4)
e1 = cv.Canny(img2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Srednia wazona 5%")
new_img9_1 = scale_weight(img2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img9_1.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img9_1.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Srednia wazona 20%")
new_img9_2 = scale_weight(img2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img9_2.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img9_2.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()

#wazona 2

plt.subplot(2,3,1)
plt.title("Oryginal")
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(img2_2)
# plt.show()

plt.subplot(2,3,4)
e1 = cv.Canny(img2_2,100,200)
plt.xlim(right=500)
plt.ylim(bottom=500)
plt.imshow(e1,cmap = 'gray')

plt.subplot(2,3,2)
plt.title("Srednia wazona 5%")
new_img9_1 = scale_weight(img2_2, 0.05)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(new_img9_1.astype(np.uint8))
# plt.show()

plt.subplot(2,3,5)
e2 = cv.Canny(new_img9_1.astype(np.uint8),100,200)
plt.xlim(right=25)
plt.ylim(bottom=25)
plt.imshow(e2,cmap = 'gray')

plt.subplot(2,3,3)
plt.title("Srednia wazona 20%")
new_img9_2 = scale_weight(img2_2, 0.2)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(new_img9_2.astype(np.uint8))

plt.subplot(2,3,6)
e3 = cv.Canny(new_img9_2.astype(np.uint8),100,200)
plt.xlim(right=100)
plt.ylim(bottom=100)
plt.imshow(e3,cmap = 'gray')
plt.show()
