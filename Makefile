start:
	astro dev start

stop:
	astro dev stop

restart:
	astro dev restart

venv:
	python -m venv .venv && echo 'ensure you activate your virtual environment before installing dev-requirements.txt'

install:
	pip install -r dev-requirements.txt

chmod:
	sudo chmod a=rwx ./include

