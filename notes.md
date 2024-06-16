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

### project

#### project components

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

#### project architecture

- prod/dev split
    - two datawarehouses
        - datawarehouse
        - datawarehouse_dev
    - two airflow instances???

#### data warehouse schemas

schemas could represent environments (e.g. `max_dev.model` for max's development environment)
or pipeline stages (staging, intermediate, dimension, fact, marts). i'm not sure what is the
best answer yet.

i'm leaning towards schemas for pipeline stages.

- what should schemas represent?
    - separate schemas for raw, staging, intermediate, and mart pipeline stages?
    - dbt advises naming scheme for models `stg_datasource__tablename.sql`
    - and config files define where it's materialised
    - could materialise as `stg.xero__fct_payments_agg` for example?
- example 1
    - data lake (not a schema)
    - `raw`
        - temporary tables to load data from data lake
	- `stg` staging
        - *naming convention*: file `stg_[source]__[entity]s.sql` materialized as `stg.[source]__[entity]s.sql`
        - *permitted operations*: renaming, type casting, basic computations (cents to dollars), categorising
        - 1:1 relationship, one stg model for each source
        - *materialized as*: views
	- `int` intermediate
        - *naming convention*: file `int_[entity]s_[verb]s.sql` materialized as `int.[entity]s_[verb]s.sql` 
        - *permitted operations*: structural simplification, re-graining, isolating complex operations
        - *materialised as*: ephemeral, or as views in custom schema
        - *examples of verbs*: pivoted, aggregated_to_user, joined, fanned_out_by_quantity, funnel_created
        - ephemeral means the model isn't materialized, dbt will interpolate the code 
            from this model into dependent models as a common table expression
        - this makes debugging harder (no materialized results), so instead you may choose to
            use a custom schema to hide the materialized results from end users but allow
            developers to debug the intermediate results
    - `dim` [conformed dimensions](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/)
        - conformed dimensions allows the joining of multiple fact tables into a single report
        - if not conformed, please indicate source system e.g. `dim_xero__customers.sql`
    - `fct` facts
    - `mrt` marts
        - contains heavily denormalized (one-big-table or OBT) models
        - `models/marts/marketing` or `models/marts/sales`
        - can result straight from `stg` models or joining `fct` and `dim` tables together
        - practical advice
            - sometimes going straight from `stg` to `mrt` is the quickest way to analytics results
            - however this results in being potentially unable to report across multiple source systems 
                since their dimensions are not conformed
            - other times properly modelling conformed dimensions allows for reporting across multiple
                source systems at once
            - the downside here is the time investment of a data engineer to build the data model
            - the downside of denormalizing is row-based DB engines don't operate well on wide tables
            - thus only go straight from `stg` to `mrt` if:
                1. there's only a single source for this reporting topic
                2. you need to get results quickly but will remember to come back and refactor
                    into best practice star schemas later

