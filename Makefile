DOCKER_TAG := latest
DOCKER_IMG := m1dnight/vub-resto-v2

.PHONY: build

build:
	docker build -t $(DOCKER_IMG):$(DOCKER_TAG) .

push: 
	docker push $(DOCKER_IMG):$(DOCKER_TAG)