# Training the Tesseract library for OCR-A font

## Motivation

Tesseract is giving terrible results for the OCR-A font as this is not a 
standard font in their training suite. So, for improving the results of reading
both the INE-A numbers and the INE-(B,C,D,E) numbers in the back we need to 
improve accuracy of the reading.

Results with a simple test of 300 random words:

word accuracy: 
letter accuracy: 

## Method

To improve the quality of reading the Tesseract documentation asks for:

- Perspective correction
- Image binarization
- Font size (30)

This was previously tried on sample images giving the above results.

### Sample generation

To train the model, we generated 300 samples for the trainset using random
strings consisting of the following characters and chosen randomly
letter, numbers, and the `<>` signs.
Images in tiff format in black over white background were generated using the 
PIL imaging library and the font was obtained from a free fonts website. 
Alongside the images a file containing the image file name and the image text
was generated so as to be able to programatically assess accuracy.

### Generation of the boxfiles

To generate boxfiles for each of the images a shell script was developed

```

```

### Correction of the boxfiles

To correct the boxfiles programmatically a python script was developed, the
script corrects only for letter substitution, letter insertion is dealt with
manually.

### Generation of training file



## Calibration


