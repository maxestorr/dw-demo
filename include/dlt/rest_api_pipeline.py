import logging
from typing import Any

import dlt
from dlt.common import pendulum

from rest_api import RESTAPIConfig, rest_api_resources

log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)
log.debug("Starting rest_api_pipeline.py")


@dlt.source
def ebird_source(
    ebird_token: str = dlt.secrets.value,
    region_code: str = dlt.secrets.value,
    date: pendulum.Date = pendulum.today(),
) -> Any:
    log.debug(f"In ebird_source()")
    year, month, day = (date.year, date.month, date.day)

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
                        "year": year,
                        "month": month,
                        "day": day,
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
                        "year": year,
                        "month": month,
                        "day": day,
                        "detail": "full",
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
        destination="duckdb",
        dataset_name="ebird",
    )

    load_info = pipeline.run(ebird_source())
    print(load_info)


if __name__ == "__main__":
    load_ebird()
