# sage-smoke-detection
The edge compute environment consist of the sensor data acquisition system (HPWREN cameras [3] or Wild Sage Nodes) and the smoke detection plugin. The plugin uses a novel deep learning architecture called SmokeyNet [4] which uses spatiotemporal information from camera imagery for real-time wildfire smoke detection. When trained on the FIgLib dataset, SmokeyNet outperforms comparable baselines and rivals human performance. The trainning data comes from the Fire Ignition Library [5] which is an open source image library that consist of historical fires that were labeled as smoke or no smoke 40 minutes before and after the fire started and became visible from the HPWREN cameras. See [references](ecr-meta/ecr-science-description.md)

The rest of the README provides instructions to run the model on different environments.

To re-train the edge model with your own data, please see [trainning README](training/README.md).

The [Dockerfile](Dockerfile) already downloads the most recent versions of both the binary classifier model and Smokeynet (during the build stage) that can be ran on an edge device or locally and for user-convience to test the models.
## Instructions

## Step 1: Build Docker image for plugin

Build image:
```
docker build -t sagecontinuum/sage-smoke-detection:0.1.0 .
```

Build image with buildx:
```
docker build -t sagecontinuum/sage-smoke-detection:0.1.0 --platform linux/amd64,linux/arm64 .
```

Build image without buildx:
```
docker build -t sagecontinuum/sage-smoke-detection:0.1.0 .
```

## Step 2: Run Docker container locally or on an edge device
There are three possible camera inputs and two smoke detector models to configure the plugin and to run the Docker container. 

Each combination can be configured in the `.env` file and are outline below.
An example `.env` file (`.env.example`) is provided. Make a copy of it to use it for the rest of the next steps.
```
cp .env.example .env
```

Camera inputs:
- HPWREN camera API: `HPWREN_FLAG=True` and `TEST_FLAG=False` are set in `.env` file
- Pre-recorded video of a fire (taken from FigLib): `HPWREN_FLAG=True` and `TEST_FLAG=False`
- Camera connected to an edge device and passed in as a command line argument: `HPWREN_FLAG=False` and `TEST_FLAG=False`
    - RSTP endpoint that is reacheable on the node

Smoke Detector Models:
- Smokeynet (set as default): `MODEL_FILE=model.onnx` and `MODEL_TYPE=smokeynet`
- Binary classifier model: `MODEL_FILE=model.tflite` and `MODEL_TYPE=binary-classifier`

Lastly, there are two other environment variables that could be set for running the container on the [Sage Platform](https://docs.waggle-edge.ai/docs/about/overview):
- TOPIC_SMOKE: The name of the topic to push to [Sage Data Repository](https://docs.waggle-edge.ai/docs/about/architecture) and become publicly accessible to users through the [Data API](https://docs.waggle-edge.ai/docs/tutorials/accessing-data#data-api)
- PYWAGGLE_LOG_DIR: temporary directory to output the [pywaggle](https://github.com/waggle-sensor/pywaggle) log files for debugging purposes. This is the same format used by the [Data API](https://docs.waggle-edge.ai/docs/tutorials/accessing-data#data-api).

Run model after setting all the environment variables in `.env` for a specific use-case:
```
docker run  -v ${PWD}/pywaggle-logs:/src/pywaggle-logs --env-file=.env sagecontinuum/sage-smoke-detection:0.1.0
```

Note that setting `-v ${PWD}/pywaggle-logs:/src/pywaggle-logs` allows to show the written files by pywaggle when debugging.

For the case that it is not needed, simply run the container without the volume mount:
```
docker run --env-file=.env sagecontinuum/sage-smoke-detection:0.1.0
```

Output when plugin is configured to run HPWREN camera API as a camera input:
```
Starting smoke detection inferencing
Get image from HPWREN Camera
Image url: http://hpwren.ucsd.edu/cameras/L/tje-1-mobo-c.jpg
Description:  Unknown direction Color Original
Perform an inference based on trainned model
Publish
.
.
.
Get image from HPWREN Camera
Image url: http://hpwren.ucsd.edu/cameras/L/tje-1-mobo-c.jpg
Description:  Unknown direction Color Original
Perform an inference based on trainned model
Publish
```

Example output of the plugin when the pre-recorded MP4 is used:
```
Starting smoke detection inferencing
Get image from 20190610-Pauma-bh-w-mobo-c.mp4
Image url: 20190610-Pauma-bh-w-mobo-c.mp4
Description: Pre-recorded video
Perform an inference based on trainned model
Publish
.
.
.
Get image from 20190610-Pauma-bh-w-mobo-c.mp4
Image url: 20190610-Pauma-bh-w-mobo-c.mp4
Description: Pre-recorded video
Perform an inference based on trainned model
Publish
```

Example output of the plugin when the bottom camera on the Wild Sage Node is used:
```
Coming Soon
```