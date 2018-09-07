import cv2
import numpy as np
import multiprocessing
from multiprocessing import Process, Lock
from multiprocessing import Pool
import os
import tifffile as tiff

def get8n(x, y, shape):
    out = []
    maxx = shape[1]-1
    maxy = shape[0]-1

    #top left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

    #top center
    outx = x
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

    #top right
    outx = min(max(x+1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

    #left
    outx = min(max(x-1,0),maxx)
    outy = y
    out.append((outx,outy))

    #right
    outx = min(max(x+1,0),maxx)
    outy = y
    out.append((outx,outy))

    #bottom left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    #bottom center
    outx = x
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    #bottom right
    outx = min(max(x+1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    return out


def region_growing(img, seed, h, w):
    list1 = []
    list2 = []             
    list1.append((seed[0], seed[1]))
    list2.append((seed[0], seed[1]))

    processed = []
    while(len(list1) > 0):
        
        pix = list1[0]

        for coord in get8n(pix[0], pix[1], img.shape):
            if(coord[0] < h-1 and coord[1] < w-1):

                ans = img[coord[0], coord[1]]
                ans = list(ans)
                ans1 = list(img[seed])

                rp = ans1[0] + 10
                rm = ans1[0] - 10
                gp = ans1[1] + 10
                gm = ans1[1] - 10
                bp = ans1[2] + 10
                bm = ans1[2] - 10

                if( (ans[0] > rm and ans[0] < rp) and (ans[1] > gm and ans[1] < gp) and (ans[2] > bm and ans[2] < bp) ):          ## if == val at that pixel.........do algo
                    if not coord in processed:
                        list1.append(coord)
                        list2.append(coord)
                    processed.append(coord)
        list1.pop(0)
    return list2


def start_code(seed):
    img = cv2.imread('1.tif')
    h,w,bpp = np.shape(img)
    img2 = cv2.imread('2.tif')

    img3 = np.zeros_like(img)                
    for px in range(0, int(h)):
        for py in range(0, int(w)):
            img3[px][py] = 125

    px=seed[0]
    py=seed[1]

    for x in range(px, h+px-int(2*h/3)):
        for y in range(py, w+py-int(2*w/3)):

            if(img3[x][y][0] == 125):

                s = (x, y)
                list2 = region_growing(img, s, h, w)

                nb = 0
                nw = 0
                T = 0.7

                for i in range(len(list2)):         # count number of white and black pixels
                    if(img2[list2[i]][0] == 255):
                        nw+=1
                    else:
                        nb+=1

                if(nw/len(list2) >= T):             # check threshold
                    for i in range(len(list2)):
                        img3[list2[i]] = 255   # if white pixels are more than T, color output as white (255)
                else:
                    for i in range(len(list2)):
                        img3[list2[i]] = 0          # else black (0)

    cv2.imwrite("part_"+str(seed[0])+"_"+str(seed[1])+".tif", img3)


def join_img():
    i=1
    for file in os.listdir():
        if file.endswith(".tif"):
            file = os.rename(file,str(i)+".tif")
            i+=1

    i1 = cv2.imread('3.tif')
    h,w,bpp = np.shape(i1)
    i2 = cv2.imread('4.tif')
    i3 = cv2.imread('5.tif')
    i4 = cv2.imread('6.tif')
    i5 = cv2.imread('7.tif')
    i6 = cv2.imread('8.tif')
    i7 = cv2.imread('9.tif')
    i8 = cv2.imread('10.tif')
    i9 = cv2.imread('11.tif')
    
    out = cv2.imread('3.tif')

    for px in range(0, int(h/3)):
        for py in range(0, int(w/3)):
                out[px][py] = i1[px][py]

    for px in range(0, int(h/3)):
        for py in range(int(w/3), int(2*w/3)):
                out[px][py] = i2[px][py]

    for px in range(0, int(h/3)):
        for py in range(int(2*w/3), w):
                out[px][py] = i3[px][py]



    for px in range(int(h/3), int(2*h/3)):
        for py in range(0, int(w/3)):
                out[px][py] = i4[px][py]

    for px in range(int(h/3), int(2*h/3)):
        for py in range(int(w/3), int(2*w/3)):
                out[px][py] = i5[px][py]

    for px in range(int(h/3), int(2*h/3)):
        for py in range(int(2*w/3), w):
                out[px][py] = i6[px][py]



    for px in range(int(2*h/3), h):
        for py in range(0, int(w/3)):
                out[px][py] = i7[px][py]

    for px in range(int(2*h/3), h):
        for py in range(int(w/3), int(2*w/3)):
                out[px][py] = i8[px][py]

    for px in range(int(2*h/3), h):
        for py in range(int(2*w/3), w):
                out[px][py] = i9[px][py]

    cv2.imwrite("out.tif",out)


if __name__ == '__main__':

    img = tiff.imread('1.tif')
    height,width,bpp = np.shape(img)

    h=int(height/3)
    w=int(width/3)

    seed = [(0, 0), (0, w), (2*w, 0), (h, 0), (h, w), (h,2*w), (2*h, 0), (2*h, w), (2*h, 2*w)]

    pool = Pool(processes=9)
    pool.map(start_code, seed)
    pool.close()
    pool.join()

    join_img()
