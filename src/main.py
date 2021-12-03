import sys
import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
import logging,requests
from distutils.util import strtobool
from waggle import plugin
from waggle.data.vision import Camera
from pathlib import Path

TOPIC_SMOKE = "env.smoke.certainty"
SMOKE_CRITERION_THRESHOLD=0.5
modelFileName = 'model.tflite'
modelPath = os.path.abspath(modelFileName)
TEST_FLAG = strtobool(os.getenv('TEST_FLAG'))
HPWREN_FLAG = strtobool(os.getenv('HPWREN_FLAG'))

#For plugin
plugin.init()
if TEST_FLAG and not HPWREN_FLAG:
    sampleMP4 = '20190610-Pauma-bh-w-mobo-c.mp4'
    cameraSrc = Path(sampleMP4)
    serverName = sampleMP4
    imageURL = sampleMP4
    description = 'Pre-recorded video'
elif not TEST_FLAG and not HPWREN_FLAG:
    if len(sys.argv) < 2:
        print(f'No camera device specified. Exiting...')
        exit(1)
    cameraSrc = sys.argv[1]
    serverName = cameraSrc
    imageURL = serverName
    description = f'{cameraSrc} Camera on Device'
elif not TEST_FLAG and HPWREN_FLAG:
    #HPWREN Parameters
    hpwrenUrl = "https://firemap.sdsc.edu/pylaski/"\
    "stations?camera=only&selection="\
    "boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
    cameraID=0
    siteID=0
    camObj = hpwren.cameras(hpwrenUrl)
    serverName = 'HPWREN Camera'
    imageURL,description = camObj.getImageURL(cameraID,siteID)
    cameraSrc = imageURL

camera = Camera(cameraSrc)


print('Starting smoke detection inferencing')
testObj = inference.FireImage()

print('Get image from ' + serverName)
print("Image url: " + imageURL)
print("Description: " + description)


sample = camera.snapshot()
image = sample.data
timestamp = sample.timestamp
testObj.setImageFromArray(image)

interpreter = tflite.Interpreter(model_path=modelPath)
interpreter.allocate_tensors()
print('Perform an inference based on trainned model')
result  = testObj.inference(interpreter)
percent = result[1]

if percent >= SMOKE_CRITERION_THRESHOLD:
    sample.save("sample.jpg")
    plugin.upload_file("sample.jpg", timestamp=timestamp)
    print('Publish\n', flush=True)
    plugin.publish(TOPIC_SMOKE, percent, timestamp=timestamp,meta={"camera": f'{cameraSrc}'})

