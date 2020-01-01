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
import cv2

class id_all_flow():

    def __init__(self, front_img_path, back_img_path, heigths):       
        self.front_img_path = front_img_path
        self.back_img_path = back_img_path
        self.heigths = heigths
        self.API_KEY = 'f93c8b9646c63020ef084ecac088583d'      

    def id_wrapper(self):
        #Init ocr & imgs
        print('Initializing images...')
        self.img_front = i_r.image_recognition(img_path = self.front_img_path,  h_list = self.heigths)
        self.img_back = i_r.image_recognition(img_path = self.back_img_path,  h_list = self.heigths)

#        for i in range(len(test_front.resized_imgs)):
#            cv2.imshow('imagen', test_front.resized_imgs[i])
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()
#            cv2.imshow('imagen', test_back.resized_imgs[i])
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()

        #Text ocr
        print('Initializing OCR images...')
        front_text = self.img_front.ocr_image()
        back_text = self.img_back.ocr_image()

        #Init text preprocess
        print('Initializing text preprocessing...')
        self.text_vector = t_f.text_prep(front_text, back_text)

        #Preprocess text
        print('Initializing text dictionary...')
        self.data_dict = self.text_vector.preprocess()
        
        #Find QR info
        print('Initializing QR detection...')
        qr_front = self.img_front.check_qr()
        qr_back = self.img_back.check_qr()
 
        try:
            self.data_dict['qr_url'] = [qr_url for qr_url in [qr_front, qr_back] if 'http' in str(qr_url)][0]
        except IndexError:            
            self.data_dict['qr_url'] = ''

        #Init web check
        print('Initializing Web Search...')
        self.ine_revision = w_s.consulta_id(self.data_dict)

        if self.ine_revision.qr_url != '':
            #QR check
            print('QR found...')
            self.validation_output = self.ine_revision.unpack_qr_ine_response()
            self.respuesta_tipo = 'QR'
            if self.validation_output[1] == None:
                #Ordinary check
                print('QR invalid...')
                print('Cheching INE page...')
                self.ord_output = self.validation_output.ine_check(self.API_KEY)
                self.validation_output = self.ine_revision.unpack_ord_ine_response(ord_output)
                self.respuesta_tipo = 'ORD'    
        elif (self.ine_revision.tipo != 'NOT DETECTED') & (self.ine_revision.cic != 'NOT DETECTED'):
            #Ordinary check
            print('QR not found...')
            print('Cheching INE page...')
            self.ord_output = self.ine_revision.ine_check(self.API_KEY)
            self.validation_output = self.ine_revision.unpack_ord_ine_response(self.ord_output)
            self.respuesta_tipo = 'ORD'
        elif (self.ine_revision.tipo == 'NOT DETECTED') | (self.ine_revision.cic == 'NOT DETECTED'):
            print('\n ID NOT DETECTED... PLEASE GIVE A BETTER IMAGE')
            self.respuesta_tipo = 'NA'
            self.validation_output = 'NA'

        return [self.respuesta_tipo, self.validation_output]

  