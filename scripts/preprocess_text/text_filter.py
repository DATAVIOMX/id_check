import numpy as np
import re

class text_prep():
    '''
    Class for preprocessing ocr text recognition
    --------------------------------------------

    Params:
    -------
    text_front: a list containing ocr info about the front face of the id
    text_back: a list containing ocr info about the back face of the id


    Methods:
    --------
    join_tsv(tsv_1, tsv_2): joins the text column of two tsv containing ocr
    info of the id

    identify_cardtype(text_vector): identifies de id card type by text

    prep_text(text_vector, cardtype): preprocess data to fit the web search script

    preprocess(): wrapper method to transform tsv information for the web search script
    '''

    def __init__(self, text_front, text_back):
        self.text_front = text_front
        self.text_back = text_back
        self.all_text = np.append(self.text_front, self.text_back)
        self.all_text = [x.upper() for x in self.all_text]


    def identify_cardtype(self, text_vector):
        ##### OJO HAY QUE TENER CUIDADO CON EL TEXTO ELECCIONES FEDERALES
        if((any('TO FEDERAL' in mystring for mystring in text_vector)) and \
            ((any('DMEX' in mystring for mystring in text_vector)) or \
                (any('IDMEX' in mystring for mystring in text_vector)) or \
                    (any('0MEX' in mystring for mystring in text_vector)))):
            cred_type = 'd'
        elif(any('TO NACIONAL' in mystring for mystring in text_vector) or any('TO NACION' in mystring for mystring in text_vector)):
            cred_type = 'e'
        elif(any('TO FEDERAL' in mystring for mystring in text_vector) and \
            ((any('DOCUMENTO' in mystring for mystring in text_vector)) or \
                (any('TACHA' in mystring for mystring in text_vector)) or \
                (any('ENMENDADURA' in mystring for mystring in text_vector)) or \
                    (any('INTRANSFERIBLE' in mystring for mystring in text_vector)) \
            )):
            cred_type = 'a'
        else:
            cred_type = 'NOT DETECTED'
        return(cred_type)

    def prep_text(self, text_vector, cardtype):
        if cardtype == 'a':
            try:
                regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
                cve_elector_completo = list(filter(regex_find.search, text_vector))[0]
                cve_elector = regex_find.findall(cve_elector_completo)[0]
            except:
                cve_elector = 'NOT DETECTED'
            emision = "placeholder"
            ocr_v = "placeholder"
            cic = ''
            ocr_h = ''
            cve_ciudadano = ''
            err_msg = ''
        elif cardtype == 'd':
            try:
                regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
                cve_elector_completo = list(filter(regex_find.search, text_vector))[0]
                cve_elector = regex_find.findall(cve_elector_completo)[0]
            except:
                cve_elector = 'NOT DETECTED'
            emision = ''
            ocr_v = ''
            cve_ciudadano = ''
            err_msg = ''
            flt = np.array(['DMEX' in mystring for mystring in text_vector])
            try:
                cic, ocr_h = np.array(text_vector)[flt][0].split('<<')
                cic = cic[-10:len(cic)]
            except:
                cic, ocr_h = ("NOT DETECTED", "NOT DETECTED")
        elif cardtype == 'e':
            try:
                regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
                cve_elector_completo = list(filter(regex_find.search, text_vector))[0]
                cve_elector = regex_find.findall(cve_elector_completo)[0]
            except:
                cve_elector = 'NOT DETECTED'
            emision = ''
            ocr_v = ''
            ocr_h = ''
            err_msg = ''
            flt = np.array(['DMEX' in mystring for mystring in text_vector])#buscar en todos los resultados
            try:
                cic, cve_ciudadano = np.array(text_vector)[flt][0].split('<<')
                cic = cic[-10:len(cic)]
            except:
                cic, cve_ciudadano = ("NOT DETECTED", "NOT DETECTED")
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

        keys_ = ['tipo_cred', 'cve_elec', 'emision', 'ocr_vertical', \
                  'ocr_horizontal', 'cic', 'cve_ciudadano', 'err_msg']

        output_dict = dict(zip(keys_, outputs))

        return(output_dict)

    def preprocess(self):
        tipo_cred = self.identify_cardtype(self.all_text)
        data_id = self.prep_text(self.all_text, tipo_cred)
        return(data_id)
