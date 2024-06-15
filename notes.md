# Notes

### todo

- [ ] add basic airflow packages to dev-requirements.txt
- [ ] add docker (wsl2) installation instructions
- [ ] dbt integration using astronomer's `cosmos` package
- [ ] ci/cd tasks
    - [ ] format
    - [ ] lint

### what am i unsure about

- if project is to be used across unix and windows, need to add ci task
    to properly format new lines?
- do i want to separate dags and include into their own repos?
    - this repo includes both infra (airflow) and code (dags / include)
    - could make dags and include both git submodules
    - link to another repository
    - how does this factor into people's development cycle?


### what do i want to demonstrate?

a simple data warehouse architecture, project structure, and developer workflow.

- project structure
    - airflow
    - dbt
    - what goes in dags vs include
- how to build a pipeline that goes through all stages
    - EL to data lake
    - ingest to raw/staging DW
    - goes through all stages, [see video for pipeline stages](https://youtu.be/fz4tax6nKZM?si=l8IZrvYeqWpFEaiT)
- how to secure secrets
- dev / prod environment splits as separate databases
    - how to deploy code to dev, test, and then ci/cd to prod

### motherduck

- 30 day free trial
    - members, compute, storage, secrets, shares, access tokens
    - all unlimited
- unlimited duration free tier
    - 10 gb storage
    - 10 compute unit hrs per month
    - no credit card required
- does motherduck allow you to create separate DB's and schemas within them?

### project components

- **orchestration**
    - airflow
- **storage**
    - data warehouse
        - duckdb (local)
        - motherduck (remote)
    - data lake
        - minio?
        - local storage? unless blob storage has functionality local storage doesn't
- **compute**
    - ELT
        - extract and load
            - airflow runtime
            - not best practice to use airflow but ok for demo
        - transform
            - duckdb (local)
            - motherduck (remote)
    - **orchestration** (airflow)
        - do we need a VM?
        - can we emulate using docker? how will github actions connect?
        - ideally want this whole thing to run on free tier, even better if 
            it doesn't require setting up any cloud resources

