import pandas as pd
import numpy as np

class tsv_prep():


    '''
    Class for preprocessing ocr text recognition
    --------------------------------------------

    Params:
    -------
    tsv_front: a tsv containing ocr info about the front face of the id
    tsv_back: a tsv containing ocr info about the back face of the id


    Methods:
    --------
    join_tsv(tsv_1, tsv_2): joins the text column of two tsv containing ocr
    info of the id

    identify_cardtype(text_vector): identifies de id card type by text

    prep_text(text_vector, cardtype): preprocess data to fit the web search script

    preprocess(): wrapper method to transform tsv information for the web search script
    '''
    def __init__(self, tsv_front, tsv_back):
        self.tsv_front = tsv_front
        self.tsv_back = tsv_back

    def join_tsv(self):
        all_text = np.append(self.tsv_front.text.dropna(), self.tsv_back.text.dropna())
        all_text = [x.upper() for x in all_text]
        return(all_text)

    def identify_cardtype(self, text_vector):
        if(('FEDERAL' in text_vector) and ((any('DMEX' in mystring for mystring in text_vector) or (any('IDMEX' in mystring for mystring in text_vector))))):
            cred_type = 'd'
        elif('NACIONAL' in text_vector):
            cred_type = 'e'
        elif(('FEDERAL' in text_vector) and ((any('DOCUMENTO' in mystring for mystring in text_vector) or (any('INTRANSFERIBLE' in mystring for mystring in text_vector))))):
            cred_type = 'a'
        else:
            cred_type = 'NOT DETECTED'
        return(cred_type)

    def prep_text(self, text_vector, cardtype):
        if cardtype == 'a':
            cve_elector = "placeholder"
            emision = "placeholder"
            ocr_v = "placeholder"
            cic = ''
            ocr_h = ''
            cve_ciudadano = ''
            err_msg = ''
        elif cardtype == 'd':
            cve_elector = ''
            emision = ''
            ocr_v = ''
            cve_ciudadano = ''
            err_msg = ''
            flt = np.array(['DMEX' in mystring for mystring in text_vector])
            cic, ocr_h = np.array(text_vector)[flt][0].split('<<')
            cic = cic[-10:len(cic)]
        elif cardtype == 'e':
            cve_elector = ''
            emision = ''
            ocr_v = ''
            ocr_h = ''
            err_msg = ''
            flt = np.array(['DMEX' in mystring for mystring in text_vector])
            cic, cve_ciudadano = np.array(text_vector)[flt][0].split('<<')
            cic = cic[-10:len(cic)]
        elif cardtype == 'NOT DETECTED':
            cve_elector = ''
            emision = ''
            ocr_v = ''
            ocr_h = ''
            cic = ''
            cve_ciudadano = ''
            err_msg = 'ERROR: Por favor mejorar la calidad de la imagen'
        outputs = list()
        outputs.extend([str(cardtype), str(cve_elector), str(emision),
                        str(ocr_v), str(ocr_h), str(cic), str(cve_ciudadano),
                        str(err_msg)])

        outputs = pd.Series(outputs,
                            index=[('tipo_cred'), ('cve_elec'),
                                   ('emision'), ('ocr_vertical'),
                                   ('ocr_horizontal'), ('cic'),
                                   ('cve_ciudadano'), ('err_msg')])

        return(outputs)

    def preprocess(self):
        joined_text = self.join_tsv()
        tipo_cred = self.identify_cardtype(joined_text)
        data_id = self.prep_text(joined_text, tipo_cred)
        return(data_id)
