DOCKER_TAG := ready_python:3.5-slim
DOCKER_CMD := docker

all: build_image

build_image:
	$(DOCKER_CMD) build -t $(DOCKER_TAG) .

rm_image:
	$(DOCKER_CMD) rmi $(DOCKER_TAG)
