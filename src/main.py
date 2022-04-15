import sys
from inference import BinaryFire,SmokeyNet
import hpwren
import os,sys
from distutils.util import strtobool
from waggle.plugin import Plugin
from waggle.data.vision import Camera
from pathlib import Path
import json

TOPIC_SMOKE = "env.smoke."
SMOKE_CRITERION_THRESHOLD=0.5
modelFileName = os.getenv('MODEL_FILE')
modelPath = os.path.abspath(modelFileName)
modelType = os.getenv('MODEL_TYPE')
TEST_FLAG = strtobool(os.getenv('TEST_FLAG'))
HPWREN_FLAG = strtobool(os.getenv('HPWREN_FLAG'))

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
else:
    sys.exit('Error: not supported case for TEST_FLAG and HPWREN_FLAG.')

camera = Camera(cameraSrc)

print('Starting smoke detection inferencing')
print('Get image from ' + serverName)
print("Image url: " + imageURL)
print("Description: " + description)

sample = camera.snapshot()
imageArray = sample.data
timestamp = sample.timestamp

print('Perform an inference based on trainned model')
if modelType == 'binary-classifier':
    print('Using binary classifier')
    binaryFire = BinaryFire(modelPath)
    binaryFire.setImageFromArray(imageArray)
    result  = binaryFire.inference()
    percent = result[1]
    if percent >= SMOKE_CRITERION_THRESHOLD:
        sample.save("sample.jpg")
        print('Publish\n', flush=True)
        with Plugin() as plugin:
            plugin.upload_file("sample.jpg", timestamp=timestamp)
            plugin.publish(TOPIC_SMOKE + 'certainty', percent, timestamp=timestamp,meta={"camera": f'{cameraSrc}'})
elif modelType == 'smokeynet':
    print('Using Smokeynet')
    previousImg = imageArray
    sample_current = camera.snapshot()
    currentImg = sample_current.data
    smokeyNet = SmokeyNet(modelPath,SMOKE_CRITERION_THRESHOLD)
    image_preds, tile_preds, tile_probs = smokeyNet.inference(currentImg,previousImg)
    print('Publish\n', flush=True)
    sample.save("sample_previous.jpg")
    sample_current.save("sample_current.jpg")
    with Plugin() as plugin:
        plugin.upload_file("sample_previous.jpg", timestamp=timestamp)
        plugin.upload_file("sample_current.jpg", timestamp=timestamp)
        tile_probs_list = str(tile_probs.tolist())
        plugin.publish(TOPIC_SMOKE + 'tile_probs', tile_probs_list, timestamp=timestamp,meta={"camera": f'{cameraSrc}'})
