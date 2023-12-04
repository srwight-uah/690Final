## Organized
### To run:
```
docker build -t proxy:latest ./proxy
docker build -t storage:latest ./storage

docker run --rm -d -p 5000:5000 --network app --name proxy proxy
docker run --rm -d --network app storage
docker run --rm -d --network app storage
docker run --rm -d --network app storage
docker run --rm -d --network app storage
docker run --rm -d --network app storage
docker run --rm -d --network app storage
docker run --rm -d --network app storage
docker run --rm -d --network app storage
```
Navigate to http://localhost:5000/store/KEY/VALUE
(replacing KEY and VALUE with the key/value pair you wish to store)

Repeat with different keys and values. Repeated use of the same key will overwrite.

Navigate to http://localhost:5000/retrieve/KEY
(replacing KEY with the key to retrieve)

When finished be sure to stop all docker containers.
## Random
### To run:
```
docker build -t r_proxy:latest ./r_proxy
docker build -t r_storage:latest ./r_storage

docker run --rm -d -p 5000:5000 --network app --name proxy proxy
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
docker run --rm -d --network app r_storage
```
Navigate to http://localhost:5000/store/KEY/VALUE
(replacing KEY and VALUE with the key/value pair you wish to store)

Repeat with different keys and values. Repeated use of the same key may result in multiple copies being stored.

Navigate to http://localhost:5000/retrieve/KEY
(replacing KEY with the key to retrieve)

When finished be sure to stop all docker containers.

## Note
Stopping nodes is not supported. If nodes are stopped, please stop all containers and restart from the beginning.