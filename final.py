import sys
import cv2
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import matplotlib.pyplot as plt


small = cv2.imread('rotated.jpg')
#small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

big = cv2.imread('original.jpg')
#big = cv2.cvtColor(big, cv2.COLOR_BGR2RGB)

big2 = Image.open('original.jpg')
#small2 = Image.open('cropped.jpg').convert('RGBA')

#big = (width, height)=(3393, 2622)
#small = (width, height)=(653, 741)


bH, bW = big.shape[:2]
sH, sW = small.shape[:2]

big_size = big2.size



m1 = float(input("What is x of Point 1 in small image: "))
n1 = float(input("What is y of Point 1 in small image: "))
m2 = float(input("What is x of Point 2 in small image: "))
n2 = float(input("What is y of Point 2 in small image: "))
m3 = float(input("What is x of Point 3 in small image: "))
n3 = float(input("What is y of Point 3 in small image: "))
m4 = float(input("What is x of Point 4 in small image: "))
n4 = float(input("What is y of Point 4 in small image: "))



x1 = float(input("What is x of Point 1 in large image: "))
y1 = float(input("What is y of Point 1 in large image: "))
x2 = float(input("What is x of Point 2 in large image: "))
y2 = float(input("What is y of Point 2 in large image: "))
x3 = float(input("What is x of Point 3 in large image: "))
y3 = float(input("What is y of Point 3 in large image: "))
x4 = float(input("What is x of Point 4 in large image: "))
y4 = float(input("What is y of Point 4 in large image: "))

'''m1 = int(m1)
m2 = int(m2)
m3 = int(m3)
m4 = int(m4)
n1 = int(n1)
n2 = int(n2)
n3 = int(n3)
n4 = int(n4)

x1 = int(x1)
x2 = int(x2)
x3 = int(x3)
x4 = int(x4)
y1 = int(y1)
y2 = int(y2)
y3 = int(y3)
y4 = int(y4)'''

# Cordinates: TopLeft, TopRight, BottomRight, BottomLeft
inp = np.float32([[m1, n1], [m2, n2], [m3, n3], [m4, n4]])
out = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])



if (x1<0 or x1>2740 or x2>3393 or x3>3393 or x4<0 or x4>2740 or y1<0 or y1>1881 or y2>1881 or y3>2622 or y4>2622):
    
    new_size = (4000, 4000)
    new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
    new_im.paste(big2, (int((new_size[0]-big_size[0])/2), int((new_size[1]-big_size[1])/2)))
    new_im.save('new.jpg')

    new = cv2.imread('new.jpg')
    #new = cv2.cvtColor(new, cv2.COLOR_BGR2RGB)
    new[:] = (0, 0, 0)

    bH1, bW1 = new.shape[:2]
    sH, sW = small.shape[:2]

    empty = 0 * np.ones((bH1, bW1, 3), dtype=np.uint8)
    empty[:sH, :sW] = small

    # Cordinates: TopLeft, TopRight, BottomRight, BottomLeft
    inp = np.float32([[m1, n1], [m2, n2], [m3, n3], [m4, n4]])
    out = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    
    M, status = cv2.findHomography(inp, out)
    transformed = cv2.warpPerspective(empty, M, (bH1, bW1))

    new[np.where(transformed != 0)] = transformed[np.where(transformed != 0)]

    cv2.imwrite('out-final.png', new)
    out1 = Image.open("out-final.png")

    out1 = out1.convert("RGBA")
    datas = out1.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    out1.putdata(newData)
    out1.save("out-final2.png", "PNG")
    
    width, height = out1.size
    print("Size of output image is: ", width, height)
    

else:
    empty = 0 * np.ones((bH, bW, 3), dtype=np.uint8)
    empty[:sH, :sW] = small
    big[:] = (0, 0, 0)

    # Cordinates: TopLeft, TopRight, BottomRight, BottomLeft
    inp = np.float32([[m1, n1], [m2, n2], [m3, n3], [m4, n4]])
    out = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])


    M, status = cv2.findHomography(inp, out)
    transformed = cv2.warpPerspective(empty, M, (bH, bW))

    big[np.where(transformed != 0)] = transformed[np.where(transformed != 0)]
        


    cv2.imwrite('out-normal.png', big)
    out2 = Image.open("out-normal.png")

    out2 = out2.convert("RGBA")
    datas = out2.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    out2.putdata(newData)
    out2.save("out-normal2.png", "PNG")
    
    width, height = out2.size
    print("Size of output image is: ", width, height)
