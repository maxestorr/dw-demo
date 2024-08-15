import logging
from typing import Any

import dlt
# TODO: Airlfow fails to import ./rest_api package
from rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)


log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)
log.debug("Starting rest_api_pipeline.py")


@dlt.source
def ebird_source(
    ebird_token: str=dlt.secrets.value,
    region_code: str=dlt.secrets.value
) -> Any:
    log.debug(f"In ebird_source()")
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://api.ebird.org/v2/",
            "auth": {
                "type": "api_key",
                "name": "x-ebirdapitoken",
                "api_key": f"{ebird_token}",
                "location": "header",
            },
        },
        "resource_defaults": {
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "top100",
                "endpoint": {
                    "path": "product/top100/{region_code}/{year}/{month}/{day}",
                    "params": {
                        # TODO: pass airflow params to select y/m/d
                        "region_code": f"{region_code}",
                        "year": "2024",
                        "month": "08",
                        "day": "01",
                    },
                },
            },
            {
                "name": "historic_observations",
                "endpoint": {
                    "path": "data/obs/{region_code}/historic/{year}/{month}/{day}",
                    "params": {
                        # TODO: pass airflow params to select y/m/d
                        "region_code": f"{region_code}",
                        "year": "2024",
                        "month": "08",
                        "day": "01",
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_ebird() -> None:
    log.debug("In load_ebird()")
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_ebird",
        destination='duckdb',
        dataset_name="ebird",
    )

    load_info = pipeline.run(ebird_source())
    print(load_info)


if __name__ == "__main__":
    load_ebird()
