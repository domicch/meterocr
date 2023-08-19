import os
import requests
import cv2
import easyocr
import csv

from dotenv import load_dotenv
from datetime import datetime


load_dotenv()


def log(text):
    with open(os.environ.get('LOG_FILENAME'), 'a') as f:
        writer = csv.writer(f)
        data = [
            datetime.now().isoformat()[:19],
            text
        ]
        writer.writerow(data)


def get_image_from_camera():
    resp = requests.get(os.environ.get('CAM_URL'), auth=(os.environ.get('CAM_USERNAME'), os.environ.get('CAM_PASSWORD')))

    with open(os.environ.get('TEMP_IMG_NAME'), 'wb') as f:
        f.write(resp.content)


def convert_image():
    img = cv2.imread(os.environ.get('TEMP_IMG_NAME'))

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Set the threshold value (128)
    threshold_value = 50
    
    # Convert the grayscale image to black and white
    _, bw_img = cv2.threshold(gray_img, threshold_value, 255, cv2.THRESH_BINARY)

    cropped = bw_img[622:727, 868:1127]
    cv2.imwrite(os.environ.get('TEMP_IMG_CROPPED_NAME'), cropped)


def get_reading():
    reader = easyocr.Reader(['en'])
    result = reader.readtext(os.environ.get('TEMP_IMG_CROPPED_NAME'))
    log(result)
    return result


def save_result(result):
    filename_prefix = str(int(datetime.now().timestamp()))
    filename = f"{filename_prefix}_{result[0][1]}.jpg"
    os.rename(os.environ.get("TEMP_IMG_NAME"), filename)
    log(f"{filename}, {result}")


def main():
    get_image_from_camera()
    convert_image()
    save_result(get_reading())


if __name__ == '__main__':
    main()
