import text_recog.image_recog as i_r
import preprocess_text.text_filter as t_f
import check_id.web_search as w_s
import string
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import re
import os
from PIL import Image
import pytesseract
import imutils
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol


class id_all_flow():

    def __init__(self, front_img_path, back_img_path, heigths):
        
        self.front_img_path = front_img_path
        self.back_img_path = back_img_path
        self.heigths = heigths
        self.API_KEY = 'f93c8b9646c63020ef084ecac088583d'


    def id_wrapper(self):
        #Init ocr & imgs
        print('Initializing images...')
        test_front = i_r.image_recognition(img_path = self.front_img_path,  h_list = self.heigths)
        test_back = i_r.image_recognition(img_path = self.front_img_path,  h_list = self.heigths)

        #Text ocr
        print('Initializing OCR images...')
        front_text = test_front.ocr_image()
        back_text = test_back.ocr_image()

        #Init text preprocess
        print('Initializing text preprocessing...')
        text_vector = t_f.text_prep(front_text, back_text)

        #Preprocess text
        print('Initializing text dictionary...')
        data_dict = text_vector.preprocess()
        
        #Find QR info
        print('Initializing QR detection...')
        qr_front = test_front.check_qr()
        qr_back = test_back.check_qr()
        for i in range(len(test_back.resized_imgs)):
            cv2.imshow
        print(qr_back)
        print(qr_front)


        try:
            print('QR found...')
            data_dict['qr_url'] = [qr_url for qr_url in [qr_front, qr_back] if 'http' in str(qr_url)][0]
        except IndexError:
            print('QR not found...')
            data_dict['qr_url'] = ''

        #Init web check
        print('Initializing Web Search...')
        ine_revision = w_s.consulta_id(data_dict)

        if ine_revision.qr_url != '':
            #QR check
            validation_output = ine_revision.unpack_qr_ine_response()
            respuesta_tipo = 'QR'
        elif (ine_revision.tipo != 'NOT DETECTED') & (ine_revision.cve_elec != 'NOT DETECTED'):
            #Ordinary check
            ord_output = ine_revision.ine_check(self.API_KEY)
            validation_output = ine_revision.unpack_ord_ine_response(ord_output)
            respuesta_tipo = 'ORD'
        elif ine_revision.tipo == 'NOT DETECTED':
            respuesta_tipo = 'NA'
            validation_output = 'NA'

        return [respuesta_tipo, validation_output]

    def valid_id(self, validatino_response, type_response):
        pass
