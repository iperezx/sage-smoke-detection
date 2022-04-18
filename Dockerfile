FROM waggle/plugin-base:1.1.1-base

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY src /src
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r /src/requirements.txt

ARG SAGE_STORE_URL="https://osn.sagecontinuum.org"
ARG BUCKET_ID_MODEL="719e3f3f-2905-429e-9ef5-20a03436af95"
ARG BUCKET_KEY_MODEL="2021-05-11"
ARG MODEL_FILE="model.tflite"
ARG MODEL_TYPE="binary-classifier"
ARG LC_ALL="C.UTF-8"
ARG LANG="C.UTF-8"
ARG HPWREN_FLAG="False"
ARG TEST_FLAG="False"

ENV LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    WAGGLE_PLUGIN_ID="50" \
    WAGGLE_PLUGIN_NAME="Smoke Detection Model" \
    WAGGLE_PLUGIN_VERSION="0.3.0" \
    WAGGLE_PLUGIN_INSTANCE="1" \
    WAGGLE_PLUGIN_REF="https://github.com/iperezx/edge-plugins/tree/master/plugin-smokedetect" \
    SAGE_STORE_URL=${SAGE_STORE_URL} \
    BUCKET_ID_MODEL=${BUCKET_ID_MODEL} \
    BUCKET_KEY_MODEL=${BUCKET_KEY_MODEL} \
    MODEL_FILE=${MODEL_FILE} \
    MODEL_TYPE=${MODEL_TYPE} \
    HPWREN_FLAG=${HPWREN_FLAG} \
    TEST_FLAG=${TEST_FLAG}

WORKDIR /src
RUN curl https://s3-west.nrp-nautilus.io/smokeynet/model.onnx -o /src/model.onnx
ENTRYPOINT [ "python3","/src/main.py" ]