APP_NAME   := logulife-tgbot
DOCKER_TAG := $(APP_NAME):latest
DOCKER_CMD := docker

all: build_image

build_image:
	./build

rm_image:
	$(DOCKER_CMD) rmi $(DOCKER_TAG)

run_container:
	$(DOCKER_CMD) run -d --name $(APP_NAME) --network logulife $(DOCKER_TAG)
