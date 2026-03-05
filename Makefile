.PHONY: build up down serve clean logs

# Build the Docker image and install all dependencies
build:
	docker compose build

# Start the local dev server (http://localhost:4000)
serve: build
	docker compose up

# Start in detached mode
up: build
	docker compose up -d

# Stop the running containers
down:
	docker compose down

# View container logs
logs:
	docker compose logs -f

# Remove containers, volumes, and generated site files
clean:
	docker compose down -v
	rm -rf _site .jekyll-cache .sass-cache