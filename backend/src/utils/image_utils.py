import cv2, os
import numpy as np

from datetime import date, timedelta
def convert_to_jpg(file_path):
    file_name = file_path.split("/")[-1]
    extension = file_name.split(".")[-1]

    new_filepath = file_path.replace(f".{extension}", ".jpg")
    if extension.lower() in ["tif", "tiff", "png", "jpg", "jpeg"]:
        img = cv2.imread(file_path)
        cv2.imwrite(new_filepath, img)
        
    if extension.lower() != "jpg":
        os.remove(file_path)
    return new_filepath

def create_thumb(image_path, new_size=(300, 200)):
    img = cv2.imread(image_path)
    img = cv2.resize(img, new_size)
    cv2.imwrite(image_path, img)
    return image_path