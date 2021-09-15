import tflite_runtime.interpreter as tflite
import numpy as np
import os
from PIL import Image
import requests
from requests.exceptions import HTTPError
from io import BytesIO

class FireImage:
    oneFire = False
    newsize = (128,128)
    classes = ["No Fire", "Fire"]
    def __init__(self):
        self.image = None
    
    def setImage(self,image):
        self.image=image
    
    def readImage(self, imagePath):
        image = Image.open(imagePath)
        img = np.array(image.resize(FireImage.newsize))
        img = img.astype("float32") / 255.0
        self.setImage(img)

    def urlToImage(self,url):
        img = None    
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            img = np.array(image.resize(FireImage.newsize))
            img = img.astype("float32") / 255.0
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            print(f'Other error occurred: {err}')
        self.setImage(img)

    def inference(self, tf_lite_interpreter):
        try:
            input_data = np.expand_dims(self.image, axis=0)
            image_shape = input_data.shape
        except AttributeError:
            return "No Image Attatched!"
        try:
            input_details = tf_lite_interpreter.get_input_details()
            input_shape = input_details[0]["shape"]
            output_details = tf_lite_interpreter.get_output_details()
            output_shape = output_details[0]["shape"]
        except AttributeError:
            print("TF_Lite Model is not able to be formated!")

        if np.array_equal(input_shape, image_shape):
            tf_lite_interpreter.set_tensor(input_details[0]["index"], input_data)
            tf_lite_interpreter.invoke()
            output = tf_lite_interpreter.get_tensor(output_details[0]["index"])
            j = np.argmax(output)
            value = output[0][j]
            percent = "{:.2%}".format(output[0][j])
            ans = f"{FireImage.classes[j]}, {percent}"

            return  [ans,float(value)]
        else:
            return "ERROR! Image input is not in correct dimensions!"