FROM quay.io/astronomer/astro-runtime:11.8.0
# FROM --platform=linux/amd64 quay.io/astronomer/astro-runtime:8.6.0 # for Motherduck compatibility
# install dbt into a virtual environment
ENV PYTHONPATH "/usr/local/airflow:/usr/local/airflow/include/dlt"
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-duckdb && deactivate
