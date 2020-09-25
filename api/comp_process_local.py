import image_recog as i_r
import text_filter as t_f
import string
import re
import os
import requests

class id_local_flow():

    def __init__(self, front_img_path, back_img_path, f_heigths, b_heigths, API_KEY='MJfvgk91xkTdRyDNPc-TO1LhxK6fo_4a'):
        self.front_img_path = front_img_path
        self.back_img_path = back_img_path
        self.front_heights = f_heigths
        self.back_heigths = b_heigths
        self.API_KEY = API_KEY
    
    def id_wrapper(self):
        #Init ocr & imgs
        #print('Initializing images...')
        self.img_front = i_r.image_recognition(img_path=self.front_img_path, h_list=self.front_heights)
        self.img_back = i_r.image_recognition(img_path=self.back_img_path,  h_list=self.back_heigths)

        #Text ocr
        #print('Initializing OCR images...')
        self.front_text = self.img_front.ocr_image()
        self.back_text = self.img_back.ocr_image()

        #Init text preprocess
        #print('Initializing text preprocessing...')
        self.text_vector = t_f.text_prep(self.front_text, self.back_text)

        #Preprocess text
        #print('Initializing text dictionary...')
        self.data_dict = self.text_vector.preprocess()
        
        return self.data_dict
    
    def call_api(self):
        #print("in call_api",self.data_dict)
        req_data = {}
        #print("keys", self.data_dict.keys())
        if self.data_dict["err_msg"] != "":
            print("err_msg", self.data_dict["err_msg"])
            exit
        else:
            #print("inside else")
            if self.data_dict["tipo_cred"] == 'a':
                req_data = {"tipo": self.data_dict["tipo_cred"],
                            "cve_elec": self.data_dict["cve_elec"],
                            "emision": self.data_dict["emision"],
                            "ocr":self.data_dict["ocr_vertical"],
                            "api_key":self.API_KEY}
            elif self.data_dict["tipo_cred"] == 'd':
                req_data = {"tipo": self.data_dict["tipo_cred"],
                            "ocr":self.data_dict["ocr_horizontal"],
                            "cic":self.data_dict["cic"],
                            "api_key":self.API_KEY}
            elif self.data_dict["tipo_cred"] == 'e':
                    req_data = {"tipo": self.data_dict["tipo_cred"],
                        "cic":self.data_dict["cic"],
                        "cve_elec":self.data_dict["cve_elec"],
                        "api_key":self.API_KEY}
            else:
                print("error en la llamada")
                exit
        #URL_TXT = "http://www.dataviomx.com/api/v1/id-check/text"
        URL_TXT = "http://127.0.0.1:5000/api/v1/id-check/text"
        response = requests.post(URL_TXT, data=req_data)
        return response
