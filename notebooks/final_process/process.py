import os
import re
import pandas as pd
import pytesseract
import numpy as np
import face_recognition
from preproces_tsv import tsv_prep 
import web_search
import sys


def ine_consult(front_path, tsv_front, tsv_back):
    # Detect face
    image = face_recognition.load_image_file(front_path)
    face_locations = face_recognition.face_locations(image, model="cnn")
    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    
    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    
    tsv_front = pd.read_csv(tsv_front, sep=r'\t', dtype={'text': str}, engine='python')
    tsv_back = pd.read_csv(tsv_back, sep=r'\t', dtype={'text': str}, engine='python')
    
    tsv = tsv_prep(tsv_front, tsv_back)
    prep_text = tsv.preprocess()
    df = prep_text.to_frame("data").reset_index()
    df = df.T
    df.columns = df.iloc[0]
    df_final = df.drop(df.index[0]).set_index(pd.Index([0]))
    
    if df_final['tipo_cred'].values[0] == 'a':
        df_final['ocr_vertical'] = str(int(df_final.loc['ocr_vertical']))
    elif df['tipo_cred'].values[0] == 'd':
        df_final['ocr_horizontal'] = str(int(df.loc['ocr_horizontal']))
        df_final['cic'] = str(int(df_final.loc['cic']))
    elif df_final['tipo_cred'].values[0] == 'e':
        df_final['cve_ciudadano'] = str(int(df_final.loc['cve_ciudadano']))
        df_final['cic'] = str(int(df_final.loc['cic']))
        
    id_check = web_search.consulta_id(df_final)
    res = id_check.ine_check(api_key='f93c8b9646c63020ef084ecac088583d')
    
    print(res)
    return res

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    ine_consult(*sys.argv[1:])