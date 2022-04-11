import onnx
import onnxruntime
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import sys
class BinaryFire:
    def __init__(self,modelPath):
        self.classes = ["No Fire", "Fire"]
        self.modelPath = modelPath
        self.setInterpreter()
        self.newsize = (128,128)
        self.scalingfactor = 255.0
        self.image = None

    def setImage(self,image):
        self.image=image
    
    def setImageFromArray(self,array):
        image = Image.fromarray(array)
        img = np.array(image.resize(self.newsize))
        img = img.astype("float32") / self.scalingfactor
        self.setImage(img)

    def getImageFromArray(self,array):
        image = Image.fromarray(array)
        img = np.array(image.resize(self.newsize))
        img = img.astype("float32") / self.scalingfactor
        return img
    
    def setInterpreter(self):
        interpreter = tflite.Interpreter(model_path=self.modelPath)
        interpreter.allocate_tensors()
        self.interpreter = interpreter

    def inference(self):
        try:
            image = self.image
            input_data = np.expand_dims(image, axis=0)
            image_shape = input_data.shape
        except AttributeError:
            return "No Image Attatched!"
        try:
            input_details = self.interpreter.get_input_details()
            input_shape = input_details[0]["shape"]
            output_details = self.interpreter.get_output_details()
        except AttributeError:
            print("TF_Lite Model is not able to be formated!")

        if np.array_equal(input_shape, image_shape):
            self.interpreter.set_tensor(input_details[0]["index"], input_data)
            self.interpreter.invoke()
            output = self.interpreter.get_tensor(output_details[0]["index"])
            j = np.argmax(output)
            value = output[0][j]
            percent = "{:.2%}".format(value)
            ans = f"{self.classes[j]}, {percent}"
            return  [ans,float(value)]
        else:
            return "ERROR! Image input is not in correct dimensions!"

class SmokeyNet:
    def __init__(self,modelPath):
        self.modelPath = modelPath
        self.check_model()

    def check_model(self):
        onnx_model = onnx.load(self.modelPath)
        result = onnx.checker.check_model(onnx_model)
        if result is not None:
            sys.exit('Onnx model failed checker')