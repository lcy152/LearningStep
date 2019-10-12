# Learning and talking

## 1. docker命令

* 创建文件:
~~~~
hello-docker
  |____index.html
  |____Dockerfile
~~~~

Dockerfile
~~~~
FROM nginx

COPY ./index.html /usr/share/nginx/html/index.html

EXPOSE 80
~~~~

index.html
~~~~
<h1>Hello docker</h1>
~~~~


* 打包镜像:
~~~~
cd hello-docker/ # 进入刚刚的目录
docker image build ./ -t hello-docker:1.0.0 # 打包镜像
~~~~

docker image build ./ -t hello-docker:1.0.0的意思是：基于路径./（当前路径）打包一个镜像，镜像的名字是hello-docker，版本号是1.0.0。该命令会自动寻找Dockerfile来打包出一个镜像


* 运行容器:
~~~~
docker container create -p 2333:80 hello-docker:1.0.0
docker container start xxx # xxx 为上一条命令运行得到的结果
~~~~


* 命令:
~~~~
docker images: 查看本机已有的镜像
docker rmi xxx: 删除镜像
docker container ls: 查看当前运行的容器
docker ps -a: 查看所有容器
docker rm xxx: 删除容器
docker stop xxx: 删除容器
~~~~

* 进入容器内部
~~~~
docker container exec -it xxx /bin/bash # xxx 为容器ID
~~~~
