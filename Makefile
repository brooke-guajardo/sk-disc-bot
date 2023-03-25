PROJECT_NAME=discord-bot
PROJECT_YML=docker_setup/discord_bot_compose.yml

.PHONY: start
start:
	docker compose -p $(PROJECT_NAME) -f $(PROJECT_YML) down
	docker compose -p $(PROJECT_NAME) -f $(PROJECT_YML) up -d

.PHONY: stop
stop:
	docker compose -p $(PROJECT_NAME) -f $(PROJECT_YML) down

.PHONY: build
build:
	docker build -t discord_bot -f docker_setup/Dockerfile .
