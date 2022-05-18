import cv2
import numpy as np
from PIL import Image

def Encode(source, message, dest):
    img = cv2.imread("assets//intruder.png")
    wid,hei = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1
    
    array=array.reshape(hei, wid, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(dest)
    print("Image Encoded Successfully")

def Decode(source):
    img = Image.open(source, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

# teste com imshow e pá
# cv2.namedWindow("Cute Kittens", cv2.WINDOW_KEEPRATIO)
# cv2.imshow("Cute Kittens", img)
    
# wait_time = 1000
# while cv2.getWindowProperty("Cute Kittens", cv2.WND_PROP_VISIBLE) >= 1:
#     keyCode = cv2.waitKey(wait_time)
#     if keyCode == 27:
#         cv2.destroyAllWindows()
#         break