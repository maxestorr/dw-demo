"""
## Dummy JSON Example
"""

import json
from airflow.decorators import dag, task
import duckdb
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
    @task
    def get_users() -> None:
        """
        get all users.
        """
        r = requests.get("https://dummyjson.com/users")
        with open('include/data/users.json', 'w') as f:
            json.dump(r.json(), f, indent=4)

    @task
    def get_posts() -> None:
        """
        get all posts.
        """
        r = requests.get("https://dummyjson.com/posts")
        with open('include/data/posts.json', 'w') as f:
            json.dump(r.json(), f, indent=4)


    # dbt doesn't handle E&L so best to do this in Airflow or using some other framework
    @task
    def load_users():
        """Load users.json into raw schema in DuckDB"""
        conn = duckdb.connect("include/data/datawarehouse.db")
        conn.sql(
            f"""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE OR REPLACE TABLE raw.dummy__users AS
            SELECT unnest(users, recursive := true)
            FROM 'include/data/users.json';
            """
        )

    @task
    def load_posts():
        """Load users.json into raw schema in DuckDB"""
        conn = duckdb.connect("include/data/datawarehouse.db")
        conn.sql(
            f"""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE OR REPLACE TABLE raw.dummy__posts AS
            SELECT unnest(posts, recursive := true)
            FROM 'include/data/posts.json';
            """
        )


    get_users() >> get_posts() >> \
    load_users() >> load_posts()


# Instantiate the DAG
dummy_json()
