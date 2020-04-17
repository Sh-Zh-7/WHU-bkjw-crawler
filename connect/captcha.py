import cv2 as cv
import pytesseract as tess

from PIL import Image
from io import BytesIO
from matplotlib.pyplot import imread


def Bin2Img(bin_obj):
    return imread(BytesIO(bin_obj), "jpeg")


def RecognizeCAPTCHA(img):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 2))
    bin1 = cv. morphologyEx(binary, cv.MORPH_OPEN, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 1))
    out = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)

    cv.bitwise_not(out, out)

    cv.imshow("title", out)
    cv.waitKey(0)

    text_image = Image.fromarray(out)
    text = tess.image_to_string(text_image)
    return text.replace(" ", "")
