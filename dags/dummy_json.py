"""
## Dummy JSON Example
"""

import json
from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime
import requests


# Define the basic parameters of the DAG, like schedule and start_date
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["example"],
)
def dummy_json():
    # Define tasks
    @task(
        # Define a dataset outlet for the task. This can be used to schedule downstream DAGs when this task has run.
        # outlets=[Dataset("current_astronauts")]
    )  # Define that this task updates the `current_astronauts` Dataset
    def get_users() -> None:
        """
        get all users.
        """
        r = requests.get("https://dummyjson.com/users")
        with open('include/users.json', 'w') as f:
            json.dump(r.json(), f, indent=4)

    @task(
        # Define a dataset outlet for the task. This can be used to schedule downstream DAGs when this task has run.
        # outlets=[Dataset("current_astronauts")]
    )  # Define that this task updates the `current_astronauts` Dataset
    def get_posts() -> None:
        """
        get all posts.
        """
        r = requests.get("https://dummyjson.com/posts")
        with open('include/posts.json', 'w') as f:
            json.dump(r.json(), f, indent=4)

    # todo: write dbt code to ingest json files into duckdb

    # @task
    # def print_astronaut_craft(greeting: str, person_in_space: dict) -> None:
    #     """
    #     This task creates a print statement with the name of an
    #     Astronaut in space and the craft they are flying on from
    #     the API request results of the previous task, along with a
    #     greeting which is hard-coded in this example.
    #     """
    #     craft = person_in_space["craft"]
    #     name = person_in_space["name"]
    #
    #     print(f"{name} is currently in space flying on the {craft}! {greeting}")

    # Use dynamic task mapping to run the print_astronaut_craft task for each
    # Astronaut in space
    # print_astronaut_craft.partial(greeting="Hello! :)").expand(
    #     person_in_space=get_astronauts()  # Define dependencies using TaskFlow API syntax
    # )
    get_users() >> get_posts()


# Instantiate the DAG
dummy_json()
