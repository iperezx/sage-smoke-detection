import argparse
from inference import BinaryFire,SmokeyNet
import hpwren
import os,sys
from distutils.util import strtobool
from waggle.plugin import Plugin
from waggle.data.vision import Camera
from pathlib import Path

parser = argparse.ArgumentParser(description='Smoke Detector Plugin')

parser.add_argument('-st',
                        '--smoke_threshold',
                        metavar='smoke_threshold',
                        type=float,
                        default=0.9,
                        help='Threshold for model inference'
                    )

parser.add_argument('-c',
                        '--camera',
                        metavar='camera_endpoint',
                        type=str,
                        required=False,
                        help='Camera endpoint connected to the edge device.'
                    )

parser.add_argument('-hcid',
                        '--hpwren-camera-id',
                        metavar='hpwren_camera_id',
                        type=int,
                        default=0,
                        help='Camera ID for HPWREN. Optional if HPWREN camera API endpoint is being used.'
                    )

parser.add_argument('-hsid',
                        '--hpwren-site-id',
                        metavar='hpwren_site_id',
                        type=int,
                        default=0,
                        help='Site ID for HPWREN. Optional if HPWREN camera API endpoint is being used.'
                    )

args = parser.parse_args()

smoke_threshold=args.smoke_threshold
camera_endpoint=args.camera
hpwren_site_id = args.hpwren_site_id
hpwren_camera_id = args.hpwren_camera_id

TOPIC_SMOKE = os.getenv('TOPIC_SMOKE','env.smoke.')
MODEL_FILE = os.getenv('MODEL_FILE')
MODEL_ABS_PATH = os.path.abspath(MODEL_FILE)
MODEL_TYPE = os.getenv('MODEL_TYPE','smokeynet')
TEST_FLAG = strtobool(os.getenv('TEST_FLAG'))
HPWREN_FLAG = strtobool(os.getenv('HPWREN_FLAG'))

if TEST_FLAG and not HPWREN_FLAG:
    sampleMP4 = '20190610-Pauma-bh-w-mobo-c.mp4'
    cameraSrc = Path(sampleMP4)
    serverName = sampleMP4
    imageURL = sampleMP4
    description = 'Pre-recorded video'
elif not TEST_FLAG and not HPWREN_FLAG:
    if camera_endpoint is None:
        print(f'No camera device specified. Exiting...')
        exit(1)
    cameraSrc = camera_endpoint
    serverName = cameraSrc
    imageURL = serverName
    description = f'{cameraSrc} Camera on Device'
elif not TEST_FLAG and HPWREN_FLAG:
    #HPWREN Parameters
    hpwrenUrl = "https://firemap.sdsc.edu/pylaski/"\
    "stations?camera=only&selection="\
    "boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
    cameraID=hpwren_camera_id
    siteID=hpwren_site_id
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
if MODEL_TYPE == 'binary-classifier':
    print('Using binary classifier')
    binaryFire = BinaryFire(MODEL_ABS_PATH)
    binaryFire.setImageFromArray(imageArray)
    result  = binaryFire.inference()
    percent = result[1]
    if percent >= smoke_threshold:
        sample.save("sample.jpg")
        print('Publish', flush=True)
        with Plugin() as plugin:
            plugin.upload_file("sample.jpg", timestamp=timestamp)
            plugin.publish(TOPIC_SMOKE + 'certainty', percent, timestamp=timestamp,meta={"camera": f'{cameraSrc}'})
elif MODEL_TYPE == 'smokeynet':
    print('Using Smokeynet')
    previousImg = imageArray
    sample_current = camera.snapshot()
    timestamp_current = sample_current.timestamp
    currentImg = sample_current.data
    smokeyNet = SmokeyNet(MODEL_ABS_PATH,smoke_threshold)
    image_preds, tile_preds, tile_probs = smokeyNet.inference(currentImg,previousImg)
    print('Publish', flush=True)
    sample.save("sample_previous.jpg")
    sample_current.save("sample_current.jpg")
    with Plugin() as plugin:
        plugin.upload_file("sample_previous.jpg", timestamp=timestamp)
        plugin.upload_file("sample_current.jpg", timestamp=timestamp_current)
        tile_probs_list = str(tile_probs.tolist())
        plugin.publish(TOPIC_SMOKE + 'tile_probs', tile_probs_list, timestamp=timestamp_current,meta={"camera": f'{cameraSrc}'})
