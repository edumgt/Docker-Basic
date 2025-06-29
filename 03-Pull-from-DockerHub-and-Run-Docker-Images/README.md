# Flow-1: Pull Docker Image from Docker Hub and Run it

## Step-1: Verify Docker version and also login to Docker Hub
```
docker version
docker login
```

## Step-2: Pull Image from Docker Hub
```
docker pull stacksimplify/dockerintro-springboot-helloworld-rest-api:1.0.0-RELEASE
```

## Step-3: Run the downloaded Docker Image & Access the Application
- Copy the docker image name from Docker Hub
```
docker run --name app1 -p 80:8080 -d stacksimplify/dockerintro-springboot-helloworld-rest-api:1.0.0-RELEASE
```

## docker image 목록 보기
## docker image ls

## 웹 브라우저에서 실행 - http://localhost/hello
![alt text](image.png)
![alt text](image-1.png)

# For Mac with Apple Chips (use different application)
Step-1: Install Docker with Apple Chips binary (https://docs.docker.com/desktop/mac/install/) on your mac machine

Step-2: Run the simple Nginx Application container. 
docker run --name kube1 -p 80:80 --platform linux/amd64 -d  stacksimplify/kubenginx:1.0.0
http://localhost

## Sample Output
kalyanreddy@Kalyans-Mac-mini-2 ~ % docker run --name kube1 -p 80:80 --platform linux/amd64 -d  stacksimplify/kubenginx:1.0.0
370f238d97556813a4978572d24983d6aaf80d4300828a57f27cda3d3d8f0fec
kalyanreddy@Kalyans-Mac-mini-2 ~ % curl http://localhost
<!DOCTYPE html>
<html>
   <body style="background-color:lightgoldenrodyellow;">
      <h1>Welcome to Stack Simplify</h1>
      <p>Kubernetes Fundamentals Demo</p>
      <p>Application Version: V1</p>
   </body>
</html>%
kalyanreddy@Kalyans-Mac-mini-2 ~ % 

```

## Step-4: List Running Containers
```
docker ps
docker ps -a
docker ps -a -q
```
```
## 위와 동일하게 Desktop 목록
![alt text](image-2.png)

## Step-5: Connect to Container Terminal
```
docker exec -it <container-name> /bin/sh
![alt text](image-3.png)
```
## docker exec -it app1 /bin/sh
## docker exec -it 300039d4d0f39ce638d9678765d09ab92705c42544b6920f30f5e2c14890cfca /bin/sh
```
PS C:\edumgt-java-education\docker-fundamentals> docker exec -it app1 /bin/sh
/ # ls -al
total 18840
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 .
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 ..
-rwxr-xr-x    1 root     root             0 Jun 29 01:31 .dockerenv
-rw-r--r--    1 root     root      19225249 Nov 23  2019 app.jar
drwxr-xr-x    2 root     root          4096 May  9  2019 bin
drwxr-xr-x    5 root     root           340 Jun 29 01:31 dev
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 etc
drwxr-xr-x    2 root     root          4096 May  9  2019 home
drwxr-xr-x    1 root     root          4096 May 11  2019 lib
drwxr-xr-x    5 root     root          4096 May  9  2019 media
drwxr-xr-x    2 root     root          4096 May  9  2019 mnt
drwxr-xr-x    2 root     root          4096 May  9  2019 opt
dr-xr-xr-x  322 root     root             0 Jun 29 01:31 proc
drwx------    1 root     root          4096 Jun 29 01:36 root
drwxr-xr-x    2 root     root          4096 May  9  2019 run
drwxr-xr-x    2 root     root          4096 May  9  2019 sbin
drwxr-xr-x    2 root     root          4096 May  9  2019 srv
dr-xr-xr-x   13 root     root             0 Jun 29 01:31 sys
drwxrwxrwt    5 root     root          4096 Jun 29 01:31 tmp
drwxr-xr-x    1 root     root          4096 May 11  2019 usr
drwxr-xr-x    1 root     root          4096 May  9  2019 var
/ # exit
PS C:\edumgt-java-education\docker-fundamentals> docker exec -it 300039d4d0f39ce638d9678765d09ab92705c42544b6920f30f5e2c14890cfca /bin/sh
/ # ls -al
total 18840
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 .
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 ..
-rwxr-xr-x    1 root     root             0 Jun 29 01:31 .dockerenv
-rw-r--r--    1 root     root      19225249 Nov 23  2019 app.jar
drwxr-xr-x    2 root     root          4096 May  9  2019 bin
drwxr-xr-x    5 root     root           340 Jun 29 01:31 dev
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 etc
drwxr-xr-x    2 root     root          4096 May  9  2019 home
drwxr-xr-x    1 root     root          4096 May 11  2019 lib
drwxr-xr-x    5 root     root          4096 May  9  2019 media
drwxr-xr-x    2 root     root          4096 May  9  2019 mnt
drwxr-xr-x    2 root     root          4096 May  9  2019 opt
dr-xr-xr-x  319 root     root             0 Jun 29 01:31 proc
drwx------    1 root     root          4096 Jun 29 01:36 root
drwxr-xr-x    2 root     root          4096 May  9  2019 run
drwxr-xr-x    2 root     root          4096 May  9  2019 sbin
drwxr-xr-x    2 root     root          4096 May  9  2019 srv
dr-xr-xr-x   13 root     root             0 Jun 29 01:31 sys
drwxrwxrwt    5 root     root          4096 Jun 29 01:31 tmp
drwxr-xr-x    1 root     root          4096 May 11  2019 usr
drwxr-xr-x    1 root     root          4096 May  9  2019 var
/ # exit
PS C:\edumgt-java-education\docker-fundamentals>
```

## Step-6: Container Stop, Start 
```
docker stop <container-name>
docker start  <container-name>
```

## Step-7: Remove Container 
```
docker stop <container-name> 
docker rm <container-name>
```

## Step-8: Remove Image
```
docker images
docker rmi  <image-id>
```

## docker 실행 상태
![alt text](image-4.png)
## : 클릭 -> detail 뷰 클릭
![alt text](image-5.png)

