# Run trainning jupyter notebook and save model
There are currently two versions of the smoke detector model:
- Binary classifier model based from this [work](https://pyimagesearch.com/2019/11/18/fire-and-smoke-detection-with-keras-and-deep-learning/)
- [Smokeynet](https://gitlab.nrp-nautilus.io/anshumand/pytorch-lightning-smoke-detection)

The rest of the instructions covered in this `README` will only be devoted to covered the first model (binary classifier model).

There are two options to train the smoke detection neural network. The first one is to
run the jupyter notebook on a Kubernetes cluster (for us it is temporarily going to be [Nautilus](https://ucsd-prp.gitlab.io)). 
The second option is to run it locally assuming that there is a GPU availabe on the local node.

### Training on a Kubernetes Cluster (Nautilus):
Clone the smoke detection model:
```
cd training/
```
Create a persistent volume claim on Nautilus under the Sage namespace (not needed now since it exists):
```
kubectl create -f training.pvc.yaml
```

Create a deployment on kubernetes:
```
kubectl create -f training.deployment.yaml
```

Attach to a pod and run bash:
```
kubectl exec -it POD-NAME bash
```

Run jupyter notebook on pod:
```
jupyter notebook -—ip=0.0.0.0 -—port=9000
```

Port forward from pod to local node:
```
kubectl port-forward POD-NAME 9000:9000
```
Access the notebook through your desktops browser on http://localhost:9000 

### Training on a local node(if no kubernetes cluster is available):
If there is no kubernetes cluster available for the user, there is a docker file that can be used to run on a local node (assuming that there is a GPU available).

Build docker image:
```
docker build --build-arg SAGE_STORE_URL=${SAGE_STORE_URL} --build-arg SAGE_USER_TOKEN=${SAGE_USER_TOKEN} --build-arg BUCKET_ID_MODEL=${BUCKET_ID_MODEL} -t iperezx/training-smokedetect:0.1.0 .
```

Run docker image:
```
docker run -it -p 9000:9000 iperezx/training-smokedetect:0.1.0
```

Attach to container and run jupyter notebook:
```
docker attach iperezx/training-smokedetect:0.1.0
jupyter notebook --ip 0.0.0.0 --port 9000 --no-browser --allow-root
```

Access the notebook through your desktops browser on http://localhost:9000 
