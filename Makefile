.PHONY: start up resetdb makemigrations migrate test stop restart down destroy build logs prune help register

DOCKER_COMPOSE ?= docker-compose
COMPOSE_FILE   ?= ./docker-compose.yml
MAIN_SERVICE_TARGET ?= web

start:
	$(info Make: Starting service(s) in background)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d $(s)

up:
	$(info Make: Starting service(s) in foreground)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up $(s)

resetdb:
	$(info Make: Resetting database (dropping and creating db))
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm ${MAIN_SERVICE_TARGET} python manage.py flush

makemigrations:
	$(info Make: Make migrations)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm ${MAIN_SERVICE_TARGET} python manage.py makemigrations

migrate:
	$(info Make: Applying migrations)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm ${MAIN_SERVICE_TARGET} python manage.py migrate

test:
	$(info Make: Running tests)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(MAIN_SERVICE_TARGET) python manage.py test

seed:
	$(info Make: Running tests)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(MAIN_SERVICE_TARGET) python seed.py

register:
	$(info Make: Creating superuser)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm ${MAIN_SERVICE_TARGET} python manage.py createsuperuser --email=alan@acme.com --username=alan

stop:
	$(info Make: Stopping service(s))
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) stop $(s)

restart:
	$(info Make: Restarting container(s))
	@make -s stop
	@make -s start

down:
	$(info Make: Cleaning container(s))
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

destroy:
	$(info Make: Cleaning container(s) and volume(s))
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down --remove-orphans

build:
	$(info Make: Building service(s))
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build $(s)

rebuild:
	$(info Make: Forcing rebuild of service(s) without cache)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build --no-cache $(s)

logs:
	$(info Make: Showing logs)
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs --tail=100 -f $(s)

prune:
	$(info Make: Running 'docker system prune -a')
	docker system prune -a

help: ## show help
	@echo ''
	@echo 'Usage: make [TARGET] [EXTRA_ARGUMENTS]'
	@echo 'Targets:'
	@echo '  start              start all or s=<name> services in background. Default make command.'
	@echo '  up                 start all or s=<name> services in foreground'
	@echo '  resetdb            reset the database (drop and create database)'
	@echo '  makemigrations     make django migrations'
	@echo '  migrate            apply django migrations'
	@echo '  test               run django tests'
	@echo '  stop               stop all or s=<name> services'
	@echo '  restart            restart all or s=<name> services'
	@echo '  down               clean containers'
	@echo '  destroy            clean containers and remove volumes'
	@echo '  build              only build all or s=<name> services'
	@echo '  rebuild            force a rebuild of all or s=<name> services without cache'
	@echo '  logs               Show logs for all or s=<name> services'
	@echo '  down               clean containers (remove containers)'
	@echo '  destroy            clean containers & related volumes'
	@echo '  prune              docker system prune -a'
	@echo '  register              creates a super user named Alan
	@echo '  help               show help'
	@echo ''