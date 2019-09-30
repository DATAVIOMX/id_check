# Datavio

Instalaciones básicas:

- Para dlib:
```bash
sudo apt-get install build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev -y
```

- Tesseract:
   
```bash
sudo add-apt-repository ppa:alex-p/tesseract-ocr
sudo apt-get update
sudo apt-get install tesseract-ocr-all
```

- Libraries:

```bash
pip install --user install face_recognition
pip install --user pytesseract
pip install --user opencv-python
pip insall --user Pillow
pip install --user tensorflow==1.12.1 opencv-contrib-python==4.1.0
pip install --user mtcnn
pip install --user python-Levenshtein
pip install --user tqdm
pip install --user python-anticaptcha
```





