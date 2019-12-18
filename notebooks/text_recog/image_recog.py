from PIL import Image
import pytesseract
import argparse
import cv2
import os
import imutils
import numpy as np

class image_recognition():


  def __init__(self, img_path: str, h_list: list):
        self.img_path = str(img_path)
        self.image_orig = cv2.imread(self.img_path)
        self.rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        self.sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        #Rotations
        self.rotations = [0, 90, 180, 270]
        self.rotated_imgs = [imutils.rotate_bound(self.image_orig, x) for x in self.rotations]
        #Resize
        self.orig_img_dims = self.image_orig.shape
        self.h_list = h_list
        self.h_list.append(self.orig_img_dims[0])
        self.sizes = len(h_list)
        self.resized_imgs = [imutils.resize(x, hgth) for x in self.rotated_imgs \
              for hgth in self.h_list]

        #Transformations
        # transform into grayscale the images
        self.grayscales = [cv2.GaussianBlur(cv2.cvtColor(x, \
            cv2.COLOR_BGR2GRAY), (3, 3), 0) \
              for x in self.resized_imgs]
        # smooth the image using a 3x3 Gaussian, then apply the blackhat
        # morphological operator to find dark regions on a light background
        self.blackhats = [cv2.morphologyEx(x, cv2.MORPH_BLACKHAT, \
            self.rectKernel) for x in self.grayscales]
        # compute the Scharr gradient of the blackhat image and scale the
        # result into the range [0, 255]
        self.gradX = [np.absolute(cv2.Sobel(x, ddepth=cv2.CV_32F, \
            dx=1, dy=0, ksize=-1)) for x in self.blackhats]
        self.minumum_img_col = [np.min(x) for x in self.gradX]
        self.maximum_img_col = [np.max(x) for x in self.gradX]
        self.gradX  = [(255*(x-mini) / (maxi-mini)).astype("uint8") \
            for x, mini, maxi in zip(self.gradX, self.minumum_img_col, \
                self.maximum_img_col)]
        # apply a closing operation using the rectangular kernel to close
        # gaps in between letters -- then apply Otsu's thresholding method
        self.gradX = [cv2.morphologyEx(x, cv2.MORPH_CLOSE, self.rectKernel) \
            for x in self.gradX]
        self.thresh = [cv2.threshold(x, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] \
            for x in self.gradX]
        # perform another closing operation, this time using the square
        # kernel to close gaps between lines of the MRZ, then perform a
        # series of erosions to break apart connected components
        self.thresh = [cv2.erode(cv2.morphologyEx(x, cv2.MORPH_CLOSE, self.sqKernel), None, iterations=4) \
            for x in self.thresh]
        # during thresholding, it's possible that border pixels were
        # included in the thresholding, so let's set 5% of the left and
        # right borders to zero
        self.borders = [int(x.shape[1] * 0.05) for x in self.resized_imgs]
        self.black_borders = []
        for i in range(len(self.resized_imgs)):
            A = self.thresh[i]
            b = self.borders[i]
            A[:,0:b] = 0
            A[:,A.shape[1]-b:] = 0
            self.black_borders.append(A)

        # find contours in the thresholded image and sort them by their size
        self.cnts = [cv2.findContours(x.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) \
            for x in self.black_borders] #[-2]

        self.cnts = [sorted(imutils.grab_contours(x),  key=cv2.contourArea, reverse=True) \
            for x in self.cnts]

        self.contours = [[num_foto, cv2.boundingRect(cont_indiv)] \
              for cont, num_foto in zip(self.cnts, range(len(self.grayscales))) \
                  for cont_indiv in cont]

        self.contour_data = [[num_foto, cont_data, cont_data[2] / float(cont_data[3]), \
            cont_data[2] / float(self.grayscales[num_foto].shape[1])] \
            for num_foto, cont_data in self.contours]

        self.valid_contours =  [[num_foto, cont_data, ar, crWidth] \
            for num_foto, cont_data, ar, crWidth in self.contour_data if ar >= 3]
        
        #coordinate for cropping images
        self.coord_rectangles = [[num_foto, int((cont_data[0] + cont_data[2]) * 0.03), \
            int((cont_data[1] + cont_data[3]) * 0.03), \
            cont_data[0] - int((cont_data[0] + cont_data[2]) * 0.03), \
            cont_data[1] - int((cont_data[1] + cont_data[3]) * 0.03), \
            cont_data[2] + (int((cont_data[0] + cont_data[2]) * 0.03) *2), \
            cont_data[3] + (int((cont_data[1] + cont_data[3]) * 0.03) *2)] \
            for num_foto, cont_data, ar, crWidth in self.valid_contours]
        #cropped images
        self.rois = [self.grayscales[num_foto][y:y + h, x:x + w] \
            for num_foto, pX, pY, x, y, w, h in self.coord_rectangles] 




  def img_recog(self, rr_image):
      textes = []
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
                