Pipeline
     > import images front and back
     > detect face for front image
     > detect borders on both images
     > check if two fronts or two backs
     > detect ine class with cnn classifier
     > crop on borders -> find alignment?
     > crop precise MRZ to collect information of INE
     > extract pytesseract or train new model?
     > use INE api or web scrapper

Requirements:
     > Models:
       >> Face detector
       >> Border detector
       >> Alignment detector
       >> OCR detector

     > Infrastructure:
       >> API (Motoko) hosteado en AWS
       >> db (Motoko) en sql-lite con todos los métodos agregados.
       >> Permisos de uso para el reconocimiento de INE

