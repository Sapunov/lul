APP_NAME   := logulife-app
DOCKER_TAG := $(APP_NAME):$($(grep VERSION src/app/settings.py | awk '{print $3}' | sed "s/'//g"))
DOCKER_CMD := docker

all: build_image

build_image:
	./build

rm_image:
	$(DOCKER_CMD) rmi $(DOCKER_TAG)

run_container:
	$(DOCKER_CMD) run -d --name $(APP_NAME) -p 8000:8000 --network logulife $(DOCKER_TAG)

make_static:
	rm -rf static/* && python src/manage.py collectstatic && tar czvf static.tgz static
