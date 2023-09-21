REGISTRY=ghcr.io/almazkun
IMAGE_NAME=django_jwt_ninja
CONTAINER_NAME=django_jwt_ninja_container
VERSION=latest

lint:
	@echo "Running lint..."
	ruff check --fix -e .
	black .

build:
	@echo "Building..."
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .

push:
	@echo "Pushing..."
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

run:
	@echo "Running..."
	docker run \
		-it \
		--rm \
		-d \
		-p 8000:8000 \
		--name $(CONTAINER_NAME) \
		--volume ./:/app \
		$(REGISTRY)/$(IMAGE_NAME):$(VERSION)

stop:
	@echo "Stopping..."
	docker stop $(CONTAINER_NAME)

pull:
	@echo "Pulling..."
	docker pull $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

logs:
	@echo "Showing logs..."
	docker logs $(CONTAINER_NAME) -f

manage:
	@echo "Running manage.py..."
	docker exec -it $(CONTAINER_NAME) python manage.py $(cmd)

test:
	make manage cmd="test"