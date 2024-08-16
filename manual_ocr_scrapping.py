import time
import os
import sys
from pdf2image import convert_from_path
import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import re
import pytesseract
import datetime

#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

##Description: Retrives directory path for Google Tesseract Engine, allowing the script to run
##Input: File path (String)
##Ouput: None


def getTesseractPath(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r"pytesseract\.pytesseract\.tesseract_cmd\s*=\s*r?'(.*)'", line)
            if match:
                print("Found")
                return match.group(1)
    print("Not Found")
    return None

##Description: Gets directory for screenshots
##Creates a directory if one doesn't currently exist
##Input: Directory path (String)
##Ouput: Directory path (String)

def getScreenshot(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Input directory created: {directory_path}")
    else:
        print(f"Input directory already exists: {directory_path}")
    return directory_path

##Description: Gets directory for PDF
##Creates a directory if one doesn't currently exist
##Input: Directory path (String)
##Ouput: Directory path (String)

def getPDF(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Input directory created: {directory_path}")
    else:
        print(f"Input directory already exists: {directory_path}")
    return directory_path

##Description: Gets directory for PDF when they are converted to images
##Creates a directory if one doesn't currently exist
##Input: Directory path (String)
##Ouput: Directory path (String)

def getPDFImages(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Input directory created: {directory_path}")
    else:
        print(f"Input directory already exists: {directory_path}")
    return directory_path

##Description: Gets directory for pickle files
##Creates a directory if one doesn't currently exist
##Input: Directory path (String)
##Ouput: Directory path (String)

def createPickleOutputDirectory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Output directory created: {directory_path}")
    else:
        print(f"Output directory already exists: {directory_path}")
    return directory_path

##Description: Converts PDFs to images
##Input: Directory path (String), Directory path (String), DPI (Int), FMT (String)
##Ouput: Image paths (String)


def pdfToImages(pdf_input_directory, output_directory, dpi=300, fmt='JPEG'):
    image_list = os.listdir(pdf_input_directory)
    for pdf in sorted(image_list, key=lambda x:x[-2:]):
        pdf_path = os.path.join(pdf_input_directory, pdf)
        if os.path.isfile(pdf_path) and pdf.lower().endswith(('.pdf')):
            # Convert PDF to a list of PIL Image objects
            images = convert_from_path(pdf_path, dpi=dpi)
    
            # Save each image and collect its path
            image_paths = []
            for i, image in enumerate(images):
                image_path = f"{output_directory}/page_{i + 1}.{fmt.lower()}"
                image.save(image_path, fmt)
                image_paths.append(image_path)
    
    return image_paths

##Description: Extracts text from images and PDFs
##Can be adjusted to remove headers and footers from PDFs
##Input: Directory path (String), Header (Boolean), Footer (Boolean)
##Ouput: Extracted text from images (Strings in Nested List)

def extractText(screenshot_input_directory, header=True, footer=True):
    text_list = []
    image_list = os.listdir(screenshot_input_directory)
    for screenshot in sorted(image_list, key=lambda x:x[-7:]):
    #Uses last 6 characters to determine image processing order
        screenshot_path = os.path.join(screenshot_input_directory, screenshot)
        if os.path.isfile(screenshot_path) and screenshot.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            print(f"Processing file: {screenshot_path}")
            
            # Enhance the image to make it more suitable for OCR
            image = Image.open(screenshot_path)
            width, height = image.size
            header_margin = int(height)
            footer_margin = int(height)
            
            enhancer = ImageEnhance.Contrast(image)
            image_enhanced = enhancer.enhance(4)  # Increase contrast

            # Convert image to black and white
            image_enhanced = image_enhanced.convert('L') 
            image_enhanced = image_enhanced.point(lambda x: 0 if x < 128 else 255, '1')

            # Apply some filters
            image_filtered = image_enhanced.filter(ImageFilter.SHARPEN)
            #Checks whether header and/or footer should be removed
            if not(header or footer):
                if header == False:
                    header_margin = int(height * 0.1)  # Top 10% for headers
                if footer == False:
                    footer_margin = int(height * 0.1)  # Bottom 10% for footers    
                cropped_image = image_filtered.crop((0, header_margin, width, height - footer_margin))
                text_list.append(pytesseract.image_to_string(cropped_image))
            else:
                text_list.append(pytesseract.image_to_string(image_filtered))
        else:
            print(f"Skipping file: {screenshot_path}")
    return text_list

##Description: Wrapper function for extracting text from an image
##Input: Image files (JPEG, PNG, etc)
##Output: Extracted text (Strings in  Nested List)


def extractTextFromImage():
    screenshot_input_directory = getScreenshot("screenshot-input-directory")
    extracted_text = extractText(screenshot_input_directory)

    return extracted_text

##Description: Wrapper function for extracting text from a PDF
##Input: Image files (JPEG, PNG, etc)
##Output: Extracted text (Strings in  Nested List)

def extractTextFromPDF(header, footer):
    pdf_input_directory = getPDF("pdf-input-directory")
    pdf_images_input_directory = getPDF("pdf-images-input-directory")
    pdfToImages(pdf_input_directory, pdf_images_input_directory)
    extracted_text = extractText(pdf_images_input_directory, header, footer)

    return extracted_text


if __name__ == "__main__":

    file_path = 'config.txt'
    tesseract_cmd_path = getTesseractPath(file_path)
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
    extracted_text = extractTextFromImage()
    df = pd.DataFrame(extracted_text)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pickle_output_directory = createPickleOutputDirectory("pickle-output-directory")
    if (sys.argv[1]):
        pickle_filename = f"{sys.argv[1]}_dataframe_{timestamp}.pkl"
    else:
        pickle_filename = f"output_dataframe_{timestamp}.pkl"
    pickle_path = os.path.join(pickle_output_directory, pickle_filename)
    df.to_pickle(pickle_path)
