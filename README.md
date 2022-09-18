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

## Setup

1. Setup MongoDB Atlas database
2. Setup custom role with all collection actions on `notes` and `users` collection, then assign to anew database user. 
3. Create `.env` in root directory with format below:
```
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

```

## Run  
The app is built with containerise in mind. To build and run the app, simpliy run command below from root directory:
```
docker-compose up --build -d 
```
Once the containers are running, access app via `http://localhost/docs` 

## Test
Run the following command for test:
```
pytest -c pytest.ini tests/test_note.py
```

[FastAPI]: https://fastapi.tiangolo.com "FastAPI web framework"
[Beanie ODM]: https://roman-right.github.io/beanie/ "Beanie object-document mapper"
[MongoDB Atlas]: https://www.mongodb.com "MongoDB NoSQL homepage"
