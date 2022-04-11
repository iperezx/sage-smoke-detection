import sys
from inference import BinaryFire,SmokeyNet
import hpwren
import os,sys
from distutils.util import strtobool
from waggle import plugin
from waggle.data.vision import Camera
from pathlib import Path

TOPIC_SMOKE = "env.smoke.certainty"
SMOKE_CRITERION_THRESHOLD=0.5
modelFileName = os.getenv('MODEL_FILE')
modelPath = os.path.abspath(modelFileName)
modelType = os.getenv('MODEL_TYPE')
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
elif modelType == 'smokeynet':
    print('Using Smokeynet')
    smokeyNet = SmokeyNet(modelPath)

if percent >= SMOKE_CRITERION_THRESHOLD:
    sample.save("sample.jpg")
    plugin.upload_file("sample.jpg", timestamp=timestamp)
    print('Publish\n', flush=True)
    plugin.publish(TOPIC_SMOKE, percent, timestamp=timestamp,meta={"camera": f'{cameraSrc}'})
