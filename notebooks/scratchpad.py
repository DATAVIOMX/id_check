from notebooks.complete_validation import comp_proces
import re
import os
import numpy as np

#Paths & Files
dir_path = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/images2/'
filenames = os.listdir('/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/images2')

dir_path = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/1st_dataset/correct_imgs/'
filenames = os.listdir('/home/ferhdzschz/sandbox/projects/datavio_files/lime/1st_dataset/images')


hlimits = [300, 500, 800, 900]
filenames.sort()

fnames_index  = np.unique(np.array([str(s).split(sep='_')[0] for s in filenames]))

filtered_term = re.compile('^16_.*')
ex_files = list(filter(filtered_term.search, filenames))

image_test = comp_proces.id_all_flow(dir_path+ex_files[0], \
  dir_path+ex_files[1], [300, 500, 800, 900])

X = image_test.id_wrapper()


image_test.text_vector.all_text

import cv2
import imutils
import pytesseract


cv2.imshow('roi', image_test.img_front.binaries[18])
cv2.waitKey(0)
cv2.destroyAllWindows()


pytesseract.image_to_string(image_test.img_front.binaries[16])


for i in range(len(image_test.img_front.binaries)):
  cv2.imshow('roi', image_test.img_front.binaries[i])
  cv2.waitKey(0)
  cv2.destroyAllWindows

import check_id.web_search as w_s
import text_recog.image_recog as i_r

web_check_ine = w_s.consulta_id(image_test.data_dict)

HTML_response = web_check_ine.ine_check(image_test.API_KEY)
web_check_ine.unpack_ord_ine_response(HTML_response)

ima = cv2.imread(dir_path+ex_files[0])
ima

cv2.imshow('img', image)
cv2.waitKey(0)
cv2.destroyAllWindows

#Init ocr & imgs
test_front = i_r.image_recognition(img_path = dir_path+ex_files[0],  h_list = [300, 500, 800, 900])
test_back = i_r.image_recognition(img_path = dir_path+ex_files[1],  h_list = [300, 500, 800, 900])

#Show all imgs
for i in range(len(test_front.rois)):
  cv2.imshow('imagen', test_front.rois[i])
  cv2.waitKey(0)
  cv2.destroyAllWindows()


#  cv2.imshow('imagen', test_back.resized_imgs[i])
#  cv2.waitKey(0)
#  cv2.destroyAllWindows()

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
qr_output[1] == None
'no puedes votar' in str(qr_output[0])
'puedes votar' in str(qr_output[0])

#Ordinary check
API_KEY = 'f93c8b9646c63020ef084ecac088583d'
response_ord = ine_revision.ine_check(API_KEY)

tabla_respuesta = ine_revision.unpack_ord_ine_response(response_ord)

'si-vota' in str(tabla_respuesta[0])
