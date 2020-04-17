import os
import queue

import cv2
import imutils
from PIL import Image, ImageDraw

a = [0, 1, 2, 3]
t2val = {}


def CFS(img):
    pix_data = img.load()
    w, h = img.size
    visited = set()
    q = queue.Queue()
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    x_cuts = []
    y_cuts = []
    for x in range(w):
        for y in range(h):
            x_axis = []
            y_axis = []
            if pix_data[x, y] == 0 and (x, y) not in visited:
                q.put((x, y))
                visited.add((x, y))
            while not q.empty():
                x_p, y_p = q.get()
                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset
                    if (x_c, y_c) in visited:
                        continue
                    visited.add((x_c, y_c))
                    try:
                        if pix_data[x_c, y_c] == 0:
                            q.put((x_c, y_c))
                            x_axis.append(x_c)
                            y_axis.append(y_c)
                    except:
                        pass
            if x_axis:
                min_x, max_x = min(x_axis), max(x_axis)
                min_y, max_y = min(y_axis), max(y_axis)
                if max_x - min_x > 3:
                    # 宽度小于3的认为是噪点，根据需要修改
                    x_cuts.append((min_x, max_x + 1))
                    y_cuts.append((min_y, max_y + 1))
    return x_cuts, y_cuts


def ClearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1


def SaveSmall(SaveDir, img, x_cuts):
    if not os.path.exists("./" + SaveDir):
        os.makedirs("./" + SaveDir)
    for j, item in enumerate(x_cuts):
        if j < 4:
            box = (item[0], 0, item[1], 30)
            a[j] = img.crop(box)
            a[j].save('./' + SaveDir + '/' + str(j) + '.png')


def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


def SaveImage(size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])
    return image


def Resize2Fit(image, width, height):
    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]
    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)
    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)
    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)
    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_REPLICATE)
    image = cv2.resize(image, (width, height))
    # return the pre-processed image
    return image
