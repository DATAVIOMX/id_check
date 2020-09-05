import image_recog as i_r
import text_filter as t_f
import string
import re
import os

class id_local_flow():

    def __init__(self, front_img_path, back_img_path, f_heigths, b_heigths, API_KEY):
        self.front_img_path = front_img_path
        self.back_img_path = back_img_path
        self.front_heights = f_heigths
        self.back_heigths = b_heigths
        self.API_KEY = API_KEY
    
    def id_wrapper(self):
        #Init ocr & imgs
        print('Initializing images...')
        self.img_front = i_r.image_recognition(img_path=self.front_img_path, h_list=self.front_heights)
        self.img_back = i_r.image_recognition(img_path=self.back_img_path,  h_list=self.back_heigths)

        #Text ocr
        print('Initializing OCR images...')
        self.front_text = self.img_front.ocr_image()
        self.back_text = self.img_back.ocr_image()

        #Init text preprocess
        print('Initializing text preprocessing...')
        self.text_vector = t_f.text_prep(self.front_text, self.back_text)

        #Preprocess text
        print('Initializing text dictionary...')
        self.data_dict = self.text_vector.preprocess()
        
        return self.data_dict
    
    def call_api(self):
        self.data_dict
