### Docker commands to run the application locally 
Creating image
```bash
docker build -t fullstackauthenticationwebappwithdatabase/api .
```
Creating and running container
```bash
docker run -p 5000:5000 -d fullstackauthenticationwebappwithdatabase/api
```
Listing containers
```bash
docker ps -a
```
Realtime log
```bash
docker logs -f <id-container>
```
Inspecting container
```bash
docker inspect <id-container>
```
Stoping container
```bash
docker stop <id-container>
```
Removing container
```bash
docker rm <id-container>
```
Listing images
```bash
docker images
```
Removing image
```bash
docker rmi <id-image>
```
Pushing image on Dockerhub
```bash
docker push fullstackauthenticationwebappwithdatabase/api:latest
```