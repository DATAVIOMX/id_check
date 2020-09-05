from PIL import Image
import pytesseract
import cv2
from cv2 import waitKey, destroyAllWindows
import os
import imutils
import numpy as np
#from pyzbar.pyzbar import decode
#from pyzbar.pyzbar import ZBarSymbol


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
        self.grayscales = [cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) for x in self.resized_imgs]
        self.binaries = [cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv2.THRESH_BINARY, 11, 2) for img in self.grayscales]
        self.grayscales = [cv2.GaussianBlur(img, (3, 3), 0) for img in self.grayscales]

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
            img_mat = self.thresh[i]
            b = self.borders[i]
            img_mat[:, 0:b] = 0
            img_mat[:, img_mat.shape[1]-b:] = 0
            self.black_borders.append(img_mat)

        # find contours in the thresholded image and sort them by their size
        self.cnts = [cv2.findContours(x.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) \
            for x in self.black_borders]

        self.cnts = [sorted(imutils.grab_contours(x),  key=cv2.contourArea, reverse=True) \
            for x in self.cnts]

        self.contours = [[num_foto, cv2.boundingRect(cont_indiv)] \
              for cont, num_foto in zip(self.cnts, range(len(self.grayscales))) \
                  for cont_indiv in cont]

        self.contour_data = [[num_foto, cont_data, cont_data[2] / float(cont_data[3]), \
            cont_data[2] / float(self.grayscales[num_foto].shape[1])] \
            for num_foto, cont_data in self.contours]

        self.valid_contours =  [[num_foto, cont_data, ar, crWidth] \
            for num_foto, cont_data, ar, crWidth in self.contour_data if ar >= 4]
 
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
        self.rois_bin = [cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) \
            for img in self.rois]

  def handling_ocr_func(self, img):
      if len(img) == 0:
          texto = ''
      else:
          try:
              texto = pytesseract.image_to_string(img, lang="spa").strip().split('\n')
          except ValueError:
              texto = ''
      return(texto)

  def ocr_image(self):
      comp_text = []
      [comp_text.append(self.handling_ocr_func(imagen)) \
          for imagen in self.rois]
      #range(len(self.grayscales))[::len(self.h_list)]
      #[comp_text.append(self.handling_ocr_func(imagen)) \
      #    for imagen in self.grayscales]   
      usefull_text = [palabra for frase in comp_text \
          for palabra in frase if palabra != '']

    
      return(usefull_text)

  def check_qr(self):
      try:
          qrs = [''] #[decode(cred, symbols=[ZBarSymbol.QRCODE]) \
              #for cred in self.resized_imgs]
          url_qr = "NOT DETECTED" #[qr_info for qr_element in qrs \
              #for qr_info in qr_element if qr_element != []][0][0]
      except IndexError:
          url_qr = "NOT DETECTED"
    
      return url_qr
  
  def find_mx_seal(self):
      pass
