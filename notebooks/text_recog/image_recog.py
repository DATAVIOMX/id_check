from PIL import Image
import pytesseract
import argparse
import cv2
import os
import imutils

class image_recognition():


  def __init__(self, img_path, preprocess):
    self.img_path = str(img_path)
    self.preprocess = str(preprocess)


  def img_recog(self):
      #load the example image and convert it to grayscale
      image = cv2.imread(self.img_path)
      image = imutils.resize(image, height=600)

      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      # check to see if we should apply thresholding to preprocess the
      # image
      if self.preprocess == "thresh":
          gray = cv2.threshold(gray, 0, 255,
          cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
      # make a check to see if median blurring should be done to remove
      # noise
      elif self.preprocess == "blur":
      	  gray = cv2.medianBlur(gray, 3)
      # write the grayscale image to disk as a temporary file so we can
      # apply OCR to it
      filename = "{}.png".format(os.getpid())
      cv2.imwrite(filename, gray)
      # load the image as a PIL/Pillow image, apply OCR, and then delete
      # the temporary file
      text = pytesseract.image_to_string(Image.open(filename), lang='spa')
      info = pytesseract.image_to_data(Image.open(filename), lang='spa')
      os.remove(filename)
      output = [text, info]
      return(output)

