import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
import logging,requests
from distutils.util import strtobool
from waggle import plugin
from waggle.data.vision import Camera

TOPIC_SMOKE = "env.smoke.certainty"
SMOKE_CRITERION_THRESHOLD=0.5
object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)

#For plugin
plugin.init()
camera = Camera("bottom_camera")

print('Starting smoke detection inferencing')
while True:
    testObj = inference.FireImage()
    sample = camera.snapshot()
    image = sample.data
    timestamp = sample.timestamp
    testObj.setImage(image)

    interpreter = tflite.Interpreter(model_path=modelPath)
    interpreter.allocate_tensors()
    print('Perform an inference based on trainned model')
    result,percent = testObj.inference(interpreter)
    print(result)
    
    if percent >= SMOKE_CRITERION_THRESHOLD:
        sample.save("smoke.jpg")
        plugin.upload_file("smoke.jpg")
        print('Publish\n', flush=True)
        plugin.publish(TOPIC_SMOKE, percent, timestamp=timestamp,meta={"camera":"bottom"})
        plugin.publish("my.sensor.name", 123, meta={"camera": "left"})
    
    time.sleep(5)

