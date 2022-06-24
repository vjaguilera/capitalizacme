# CapitalizAcme
This project is a simplified DRF Api to handle Coyote's Menu scheduling

## RUN IT WITH DOCKER
A `Makefile` is installed to make your life easier while running this project

Run `make help` to find more about the available commands

If you are in a rush, just run:

- `make build` To build the project based on a Dockerfile
- `make up` To run the proyect in a not-detached mode

## RUN IT WITHOUT DOCKER
First, create virtual enviroment named venv

`capitalizacme$ virtualenv --python=python3 venv`

Then activate the virtual enviroment named venv

`capitalizacme$ source venv/bin/activate`

Install the dependencies

`capitalizacme$ pip install -r requirements.txt`

Run the project

`capitalizacme$ python manage.py runserver`

Then go to `http://127.0.0.1:8000`