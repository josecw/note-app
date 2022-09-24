# NOTE-APP for Demo
A simple note taking app built with FastAPI and Beanie ODM


## Intro

This simple app provides a basic note API on top of a MongoDB store with the following features:
* Registration
* JWT auth login
* Note model CRUD
* List Note by Tag
* Mock logout

### Libraries
The libraries are used to build the features:
- [FastAPI]() - Python async micro framework built on Starlette and PyDantic  
- [Beanie ODM]() - Async MongoDB object-document mapper built on PyDantic

### Tech Stack
The components below are applied in the application architectures:
- Python 3.9
- [MongoDB Atlas]()
- Nginx
- Docker
- Minikube

## Setup for MongoDB  
1. Setup MongoDB Atlas database
2. Setup custom role with all collection actions on `notes` and `users` collection, then assign to anew database user. 
3. Configure IP whitelisting at `Network Access` from left panel.

## Setup for Docker
Create `.env` in root directory with format below for running with Docker:
```
# APP Settings
HOST=<replace with host name, default 0.0.0.0 for running in local>
PORT=<replace with target port, default 8000 for running in local>
DEBUG_MODE=<indicate if the app running in development or debug mode, default True>
LOG_LEVEL=INFO

#Database Settings
DB_HOST=<replace with mongodb host name>
DB_USER=<replace with mongodb database username>
DB_PASSWORD=<replace with mongodb database password>
DB_NAME=<replace with mongodb database name>
DB_SOCKET_TIMEOUT=<input timeput in miliseconds>
DB_CONNECT_TIMEOUT=<input timeput in miliseconds>

# Auth
JWT_SECRET=<Replace with random hash values>
JWT_ALGO=HS256
JWT_EXPIRY=<input timeput in seconds, default to 600>

# REDIS
REDIS_HOST=<replace with redis host name or ip. Defaulto to redis if running in Docker>
REDIS_PORT=6379
REDIS_PASSWORD=<replace with redis password. The password will configure into redis server>

```

### Run as Docker
The app is built with container in mind.  
To build and run the app, simpliy run command below from root directory:
```
docker-compose up --build -d 
```
Once the containers are running, access app via `http://localhost/docs` 


## Setup for minikube
1. Enable [minikube-ingress]()
2. Create a new namespace `sandbox` in minikube.
3. Create Kubernetes secret manifest to store sensitive credentials for running with `minikube`:
```
apiVersion: v1
kind: Secret
metadata:
  name: note-secret
  namespace: sandbox
type: Opaque
data:
  DB_HOST: <replace with mongodb host name>
  DB_USER: <replace with mongodb database username>
  DB_PASSWORD: <replace with mongodb database password>
  DB_NAME: <replace with mongodb database name>
  JWT_SECRET: <Replace with random hash values>
```
4. Run command `kubectl apply -f secret.yaml` to create secret/
5. Run command `eval $(minikube docker-env)` to active minikube docker environment.
6. Build the image using `minikube image` to build and load the image locally:
```
minikube image build -t josecw/note-api note-api/
```
7. Deploy manifests:
```
kubectl apply -f release/deployment.yaml
kubectl apply -f release/ingress.yaml
```
8. Edit `/etc/hosts/` or host file to include localhost or 127.0.0.1 as `my-note-app.com` 
9. Open another terminal and run `minikube tunnel`
10. Now test the ingress is working `curl my-note-app.com` should see `{"message":"Note-App is live"}`
11. The app is officially running. Go to `http://my-note-app.com/docs` for documentation

### Run in K8S  
As pipeline is not available in the repo, please follow the steps in `Setup` to configure kubernetes deployment

## Test
Run the following command for test:
(Setup python environment before run test)
```
cd note-api
pytest -c pytest.ini
```

[FastAPI]: https://fastapi.tiangolo.com "FastAPI web framework"
[Beanie ODM]: https://roman-right.github.io/beanie/ "Beanie object-document mapper"
[MongoDB Atlas]: https://www.mongodb.com "MongoDB NoSQL homepage"
[minikube-ingress]: https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/ "Enable minikube ingress"