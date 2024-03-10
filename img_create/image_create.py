import base64
import datetime
import os

from PIL import Image
from io import BytesIO


def create_images(images_codes: list, name, folder_path):

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_bin_code = base64.b64decode(images_codes[0])

    image = Image.open(BytesIO(image_bin_code))

    image_name = f"{formatted_datetime}_{name}.jpg"

    file_path = folder_path + image_name

    i = 2
    while os.path.exists(file_path):
        image_name = f"{formatted_datetime}_{name}_{i}.jpg"
        file_path = folder_path + image_name
        i += 1

    image.save(file_path)

    return image_name

