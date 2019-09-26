import pandas as pd
import numpy as np

tsv_f = pd.read_csv('notebooks/ifes_ocr/2015-12-19 13.54.30.tsv', sep='\t')
tsv_f.text.dropna()

tsv_b = pd.read_csv('notebooks/ifes_ocr/3_back.tsv', sep='\t')
tsv_b.text.dropna()


def join_tsv(tsv_1, tsv_2):
    all_text = np.append(tsv_1.text.dropna(), tsv_2.text.dropna())
    all_text = [x.upper() for x in all_text]
    return(all_text)


def identify_cardtype(text_vector):
    if(('FEDERAL' in text_vector) and ((any('DMEX' in mystring for mystring in text_vector) or (any('IDMEX' in mystring for mystring in text_vector))))):
        cred_type = 'd'
    elif('NACIONAL' in text_vector):
        cred_type = 'e'
    elif(('FEDERAL' in text_vector) and ((any('DOCUMENTO' in mystring for mystring in text_vector) or (any('INTRANSFERIBLE' in mystring for mystring in text_vector))))): 
        cred_type = 'a'
    else:
        cred_type = 'NOT DETECTED'

    return(cred_type)



def prep_text(text_vector, cardtype):
    if card_type == 'a':
        cve_elector = "placeholder"
        emision = "placeholder"
        ocr_v = "placeholder"
    elif card_type == 'd':
        flt = np.array(['DMEX' in mystring for mystring in text_vector])
        cic, ocr_h = np.array(text_vector)[flt][0].split('<<')
        cic = cic[-10:len(cic)]
    elif card_type == 'e':
        flt = np.array(['DMEX' in mystring for mystring in text_vector])
        cic, cve_ciudadano = np.array(text_vector)[flt][0].split('<<')
        cic = cic[-10:len(cic)]
    elif card_type == 'NOT DETECTED'
        return('error')

  
  #test = join_tsv(tsv_f, tsv_b)
  #flt = np.array(['ELECTOR' in mystring for mystring in test])
  