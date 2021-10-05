FROM waggle/plugin-base:1.1.1-base
COPY . .
WORKDIR /src
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r /src/requirements.txt

ARG SAGE_STORE_URL="HOST"
ARG BUCKET_ID_MODEL="BUCKET_ID_MODEL"
ARG LC_ALL="C.UTF-8"
ARG LANG="C.UTF-8"
ARG HPWREN_FLAG="False"
ARG TEST_FLAG="True"

ENV LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    WAGGLE_PLUGIN_ID="50" \
    WAGGLE_PLUGIN_NAME="Smoke Detection Model" \
    WAGGLE_PLUGIN_VERSION="0.1.0" \
    WAGGLE_PLUGIN_INSTANCE="1" \
    WAGGLE_PLUGIN_REF="https://github.com/iperezx/edge-plugins/tree/master/plugin-smokedetect" \
    SAGE_STORE_URL=${SAGE_STORE_URL} \
    BUCKET_ID_MODEL=${BUCKET_ID_MODEL} \
    HPWREN_FLAG=${HPWREN_FLAG} \
    TEST_FLAG=${TEST_FLAG}

RUN sage-cli.py storage files download ${BUCKET_ID_MODEL} 2021-05-11/model.tflite --target /src/model.tflite
CMD [ "python3","/src/main.py" ]