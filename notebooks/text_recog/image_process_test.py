# import the necessary packages
from imutils import paths
from itertools import compress
import numpy as np
import argparse
import imutils
import cv2
import os
import pytesseract
from PIL import Image


img_dir = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/correct_imgs/'
f_names = os.listdir(img_dir)

# initialize a rectangular and square structuring kernel
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

# loop over the input image paths
#for imagePath in paths.list_images(args["images"]):

########################
#cv2.imshow('image', edged)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
########################
##### EJemplos 140 y 141

idx = ['226_' in file_name for file_name in f_names]
examples = list(compress(f_names, idx))

textes = []

h_limits = [500, 600, 800] 
for imagen in examples:
    #load the image, resize it, and convert it to grayscale
    image = cv2.imread(img_dir + imagen)
    for h_limit in h_limits:
        image = imutils.resize(image, height=h_limit) # ESTE PARAMETRO DEPENDERA DE LA ALTURA DE LA IMAGEN / QUE TAN GRANDE SE VE LA CREDENCIAL
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('image', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    
        # smooth the image using a 3x3 Gaussian, then apply the blackhat
        # morphological operator to find dark regions on a light background
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
        #cv2.imshow('image', blackhat)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # compute the Scharr gradient of the blackhat image and scale the
        # result into the range [0, 255]
        gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")

        # apply a closing operation using the rectangular kernel to close
        # gaps in between letters -- then apply Otsu's thresholding method
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
        thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # perform another closing operation, this time using the square
        # kernel to close gaps between lines of the MRZ, then perform a
        # series of erosions to break apart connected components
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
        thresh = cv2.erode(thresh, None, iterations=4)
        #cv2.imshow('image', thresh)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        # during thresholding, it's possible that border pixels were
        # included in the thresholding, so let's set 1% of the left and
        # right borders to zero
        p = int(image.shape[1] * 0.05)
        thresh[:, 0:p] = 0
        thresh[:, image.shape[1] - p:] = 0
        # find contours in the thresholded image and sort them by their
        # size
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[-2]
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True) 
        # loop over the contours
        for c in cnts[:]:
            # compute the bounding box of the contour and use the contour to
            # compute the aspect ratio and coverage ratio of the bounding box
            # width to the width of the image
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            crWidth = w / float(gray.shape[1])
            # check to see if the aspect ratio and coverage width are within
            # acceptable criteria
            if (ar >= 4):# | ((ar > 1.2) & (ar < 1.5)):
                # pad the bounding box since we applied erosions and now need
                # to re-grow it
                pX = int((x + w) * 0.03)
                pY = int((y + h) * 0.03)
                (x, y) = (x - pX, y - pY)
                (w, h) = (w + (pX * 2), h + (pY * 2))
                # extract the ROI from the image and draw a bounding box
                # surrounding the MRZ
                roi = image[y:y + h, x:x + w].copy()
                roi_blackhat = blackhat[y:y + h, x:x + w].copy()
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # show the output images
                try:
                    #cv2.imshow("Image", image)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    #cv2.imshow("ROI", roi)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    # write the image to disk as a temporary file so we can
                    # apply OCR to it
                    filename = "{}.png".format(os.getpid())
                    cv2.imwrite(filename, roi)
                    # load the image as a PIL/Pillow image, apply OCR, and then delete
                    # the temporary file
                    texto = pytesseract.image_to_string(Image.open(filename), lang='spa')
                    #image_datum = pytesseract.image_to_data(Image.open(filename), lang='spa')
                    os.remove(filename)
                    textes.append(texto)
                    #image_datum.append(image_datum)
                except:
                    continue
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
                    
        texto = pytesseract.image_to_string(Image.open(img_dir + imagen), lang='spa')        
        textes.append(texto)
        #image_datum = pytesseract.image_to_data(Image.open(img_dir + imagen), lang='spa')
        #image_data.append(image_datum)


complete_text = ' '.join([str(elem) for elem in textes])
complete_text = 'text\n{}'.format(complete_text)


with open('/home/ferhdzschz/sandbox/projects/datavio_files/lime/ocr_split/634_IFE.tsv', 'wt') as file:
    file.write(complete_text)

#################### reading function ###########

split_algo_ocr = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/rotatted_ocr/'
img_dir = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/images/'
f_names = os.listdir(img_dir)
f_names.sort()

def split_algo(image_path, h_list):

    # initialize a rectangular and square structuring kernel
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    #creating list
    textes = []
 
    #load the image, resize it, and convert it to grayscale
    image = cv2.imread(image_path)
    for rot in [0,90,180,270]:
        rotated = imutils.rotate_bound(image, rot)
        for h_limit in h_list:
            r_image = imutils.resize(rotated, height=h_limit) # ESTE PARAMETRO DEPENDERA DE LA ALTURA DE LA IMAGEN / QUE TAN GRANDE SE VE LA CREDENCIAL
            gray = cv2.cvtColor(r_image, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('image', image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
        
            # smooth the image using a 3x3 Gaussian, then apply the blackhat
            # morphological operator to find dark regions on a light background
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
            #cv2.imshow('image', blackhat)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            # compute the Scharr gradient of the blackhat image and scale the
            # result into the range [0, 255]
            gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
            gradX = np.absolute(gradX)
            (minVal, maxVal) = (np.min(gradX), np.max(gradX))
            gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")

            # apply a closing operation using the rectangular kernel to close
            # gaps in between letters -- then apply Otsu's thresholding method
            gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
            thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            # perform another closing operation, this time using the square
            # kernel to close gaps between lines of the MRZ, then perform a
            # series of erosions to break apart connected components
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
            thresh = cv2.erode(thresh, None, iterations=4)
            #cv2.imshow('image', thresh)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            # during thresholding, it's possible that border pixels were
            # included in the thresholding, so let's set 5% of the left and
            # right borders to zero
            p = int(r_image.shape[1] * 0.05)
            thresh[:, 0:p] = 0
            thresh[:, r_image.shape[1] - p:] = 0
            # find contours in the thresholded image and sort them by their
            # size
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[-2]
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True) 
            # loop over the contours
            for c in cnts[:]:
                # compute the bounding box of the contour and use the contour to
                # compute the aspect ratio and coverage ratio of the bounding box
                # width to the width of the image
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                crWidth = w / float(gray.shape[1])
                # check to see if the aspect ratio and coverage width are within
                # acceptable criteria
                if (ar >= 4):
                    # pad the bounding box since we applied erosions and now need
                    # to re-grow it
                    
                    pX = int((x + w) * 0.03)
                    pY = int((y + h) * 0.03)
                    (x, y) = (x - pX, y - pY)
                    (w, h) = (w + (pX * 2), h + (pY * 2))
                    # extract the ROI from the image and draw a bounding box
                    # surrounding the MRZ
                    roi = r_image[y:y + h, x:x + w].copy()
                    roi_blackhat = blackhat[y:y + h, x:x + w].copy()
                    cv2.rectangle(r_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # show the output images
                    try:
                        #cv2.imshow("Image", r_image)
                        #cv2.waitKey(0)
                        #cv2.destroyAllWindows()
                        #cv2.imshow("ROI", roi)
                        #cv2.waitKey(0)
                        #cv2.destroyAllWindows()
                        # write the image to disk as a temporary file so we can
                        # apply OCR to it
                        filename = "{}.png".format(os.getpid())
                        cv2.imwrite(filename, roi)
                        # load the image as a PIL/Pillow image, apply OCR, and then delete
                        # the temporary file
                        texto = pytesseract.image_to_string(Image.open(filename), lang='spa')
                        #image_datum = pytesseract.image_to_data(Image.open(filename), lang='spa')
                        os.remove(filename)
                        textes.append(texto)
                        #image_datum.append(image_datum)
                    except:
                        continue
            #cv2.imshow("Image", r_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            texto = pytesseract.image_to_string(Image.open(image_path), lang='spa')        
            textes.append(texto)
            #image_datum = pytesseract.image_to_data(Image.open(img_dir + imagen), lang='spa')
            #image_data.append(image_datum)

    texto = pytesseract.image_to_string(Image.open(image_path), lang='spa')        
    textes.append(texto)

    complete_text = ' '.join([str(elem) for elem in textes])
    complete_text = 'text\n{}'.format(complete_text)

    return(complete_text)


i = 0
total = len(f_names[1710:2000])

import datetime
start_time = datetime.datetime.now()

for f in f_names[1710:2000]:
    file_str = str.split(f, sep='.')[0]
    h_limits_list = [500, 600, 900]
    try:
        texto_completo = split_algo(img_dir + f, h_limits_list)
        with open(split_algo_ocr+'{}.tsv'.format(file_str), 'wt') as file:
            file.write(texto_completo)
        i += 1
        progresso = round(i / total, ndigits = 3) * 100
        print('Progress = {}% \n Iterarion: {}'.format(str(progresso), str(i)))
    except AttributeError:
        continue

print("Start time: {}\n".format(str(start_time)))
end_time = datetime.datetime.now()
print("End time: {}".format(str(end_time)))
total_time = end_time-start_time
print("Elapsed time: {}\n\n".format(str(total_time)))
