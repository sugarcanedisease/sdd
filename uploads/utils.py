import cv2
from matplotlib import pyplot as plt
import numpy as np
from rembg import remove
import matplotlib.pyplot as plt


def Removed_bg_Image(image_path):
    image = cv2.imread(f'media/{image_path}')
    # Removing Background to clearly identify the infected area
    removed_bg_image = remove(image)  
    return removed_bg_image

def Read_Image(image):
    # RGB`
    rgb_image_size = cv2.resize(image,(300,400), interpolation = cv2.INTER_AREA)
    return rgb_image_size 

def Gray_Scale_Image(rgb_image):
    # Converting to gray
    # blur = cv2.medianBlur(rgb_image, 7)
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    return gray

def Equalized_Hist(gray_image):
    # Converting to equalized
    eqalized_image = cv2.equalizeHist(gray_image)
    return eqalized_image

def Binary_Image(image):
    # Converting to Binary
    binary = cv2.threshold(image,125, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    return binary

def Morphology_Image(binary_image):
    # Converting to Morphology by using kernel 3x3
    kernel = np.ones((3,3),np.uint8)
    MORPH_close = cv2.morphologyEx(binary_image,cv2.MORPH_CLOSE,kernel, iterations = 1)
    return MORPH_close


def Contours(M_Image):
    # Figuring out number of infected region
    contours, hierarchy = cv2.findContours(M_Image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
    
    biggest_contour =  max(contours,key=cv2.contourArea)
    leaf_area = cv2.contourArea(biggest_contour)

    infected_contour_lst = []
    for i in contours:
        infected_contour_lst.append(cv2.contourArea(i))
    infected_contour_lst.remove(leaf_area)
    infected_area =    sum(infected_contour_lst)

    Num_of_contour = len(contours)

    return contours, leaf_area, infected_area, Num_of_contour

def Contours_On_Orinial(Image, contours):
    # Drawing image of number of infected region
    image_copy = Image.copy()
    spot_on_org_img = cv2.drawContours(image_copy, contours, -1, (0, 255, 0), thickness=3)

    # draw the contours on the black image
    black_img = np.zeros(Image.shape)
    cv2.drawContours(black_img, contours, -1, (0,255,0), 3)
    return spot_on_org_img, black_img


def Save_Images(img_path, removed_bg_image, gray, eqalized_image, binary, MORPH_close, spot_on_org_img, black_img):
    cv2.imwrite(f'media/Removed_bg_Images/{img_path}', removed_bg_image)  
    cv2.imwrite(f'media/GrayScale_Images/{img_path}', gray)  
    cv2.imwrite(f'media/Equalized_images/{img_path}', eqalized_image)  
    cv2.imwrite(f'media/binary_Images/{img_path}', binary)  
    cv2.imwrite(f'media/morphological_images/{img_path}', MORPH_close)  
    cv2.imwrite(f'media/spot_on_org_images/{img_path}', spot_on_org_img)  
    cv2.imwrite(f'media/spot_on_black_images/{img_path}', black_img)  
    return True




