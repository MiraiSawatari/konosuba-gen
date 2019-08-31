# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import os
from PIL import Image, ImageDraw, ImageFilter
from PIL import ImageFont
from time import time
import urllib.request




args = sys.argv
urllib.request.urlretrieve('https://minotar.net/avatar/'+str(args[1])+'/240',str(args[1])+".png")

image_path = str(args[1])+".png"
img = cv2.imread(image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.merge((gray, gray, gray), img)

kernel = np.ones((4,4),np.uint8)
dilation = cv2.dilate(img,kernel,iterations = 1)

diff = cv2.subtract(dilation, img)

white = [102, 83, 53]



cv2.imwrite('output.png', img)
img1 = cv2.imread('output.png',-1)
img2 = cv2.imread("on.png", -1) # this one has transparency
h, w, c = img2.shape

img1 = cv2.resize(img1, (w, h), interpolation = cv2.INTER_CUBIC)
result = np.zeros((h, w, 3), np.uint8)

#slow
st = time()
for i in range(h):
  for j in range(w):
        color1 = img1[i, j]
        color2 = img2[i, j]
        alpha = color2[3] / 255.0
        new_color = [ (1 - alpha) * color1[0] + alpha * color2[0],
                      (1 - alpha) * color1[1] + alpha * color2[1],
                      (1 - alpha) * color1[2] + alpha * color2[2] ]
        result[i, j] = new_color
end = time() - st
print(end)

#fast
st = time()
alpha = img2[:, :, 3] / 255.0
result[:, :, 0] = (1. - alpha) * img1[:, :, 0] + alpha * img2[:, :, 0]
result[:, :, 1] = (1. - alpha) * img1[:, :, 1] + alpha * img2[:, :, 1]
result[:, :, 2] = (1. - alpha) * img1[:, :, 2] + alpha * img2[:, :, 2]
end = time() - st
print(end)

cv2.imwrite('output.png',result)


im1 = Image.open('back.png')
im2 = Image.open('output.png')

back_im = im1.copy()
back_im.paste(im2, (1230, 194))
back_im.save('out_'+str(args[1])+"_1.png")

def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'

    draw.text(position, text, font_color, font=font)

    return img

song_title = str(args[1]).upper()
font_path = "ex.otf"
font_size = 72
font_color = (53, 33, 18)
height = 210
width = 140
img = add_text_to_image(back_im, song_title, font_path, font_size, font_color, height, width)
img.save('out_'+str(args[1])+".png")
os.remove('out_'+str(args[1])+"_1.png")
os.remove('output.png')




