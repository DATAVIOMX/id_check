
#import notebooks.text_recog.image_recog as i_r
#import notebooks.preprocess_text.text_filter as t_f
#import notebooks.check_id.web_search as w_s
#import re
#import os
#
#from PIL import Image
#import pytesseract
#import cv2
#import imutils
#import numpy as np
#import string
#from pyzbar.pyzbar import decode
#from pyzbar.pyzbar import ZBarSymbol
#from bs4 import BeautifulSoup
#import requests

import complete_validation.comp_proces as c_p
import re
import os

#Paths & Files
dir_path = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/images2/'
filenames = os.listdir('/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/images2')
filenames.sort()
filtered_term = re.compile('^38_.*')
ex_files = list(filter(filtered_term.search, filenames))

image_test = c_p.id_all_flow(dir_path+ex_files[0], dir_path+ex_files[1], [300, 500, 800, 900])

X = image_test.id_wrapper()



#Init ocr & imgs
test_front = i_r.image_recognition(img_path = dir_path+ex_files[0],  h_list = [300, 500, 800, 900])
test_back = i_r.image_recognition(img_path = dir_path+ex_files[1],  h_list = [300, 500, 800, 900])

#Text ocr
front_text = test_front.ocr_image()
back_text = test_back.ocr_image()

#Init text preprocess
text_vector = t_f.text_prep(front_text, back_text)

#Preprocess text
data_dict = text_vector.preprocess()

#Find QR info
qr_front = test_front.check_qr()
qr_back = test_back.check_qr()

data_dict['qr_url'] = [qr_url for qr_url in [qr_front, qr_back] if 'http' in str(qr_url)][0]

#Init web check
ine_revision = w_s.consulta_id(data_dict)

ine_revision.qr_url != ''
#QR check
qr_output = ine_revision.unpack_qr_ine_response()
'puedes votar' in str(qr_output[0])

#Ordinary check
API_KEY = 'f93c8b9646c63020ef084ecac088583d'
response_ord = ine_revision.ine_check(API_KEY)

#tabla_respuesta = ine_revision.unpack_ord_ine_response(response_ord)
#
#'si-vota' in str(tabla_respuesta[0])
#
#
##ine_lista_page = requests.get(url_ine)
##soup = BeautifulSoup(ine_lista_page.content, 'html.parser')
##soup.find(name = 'div', id = "menje")
##
##cv2.imshow('img', test_back.resized_imgs[13])
##cv2.waitKey(0)
##cv2.destroyAllWindows()
#