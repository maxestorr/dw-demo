# dw-demo

A demo for a simple data warehouse, intended to demonstrate data warehouse architecture,
project structure, and developer workflow.

## Running the Project

### System Dependencies

- Astronomer
- Docker (needs to be running)
- Python version >= 11

### Getting Going

### Makefile

A makefile is provided for convenience on unix systems.

- `make venv` creates python virtual environment
    - You have to source it yourself as Make can't spawn terminals
- `make install` to install dev dependencies
- `make start` to start Airflow docker server
- `make restart` to restart Airflow docker server
- `make stop` to stop Airflow docker server
