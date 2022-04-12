"""Common fixtures for integration tests."""

from urllib.parse import urljoin

import pytest
from pytest_docker_tools import build, container

from tests import constants
from tests.utils.container_wrappers import (
    PostgresContainer,
    QuipucordsContainer,
    ScanTargetContainer,
)
from tests.utils.http import ApiClient, QPCAuth

# pylint: disable=no-value-for-parameter
postgres_container = container(
    scope="class",
    image="postgres:14.1",
    environment=dict(
        POSTGRES_USER=constants.POSTGRES_USER,
        POSTGRES_PASSWORD=constants.POSTGRES_PASSWORD,
        POSTGRES_DB=constants.POSTGRES_DB,
    ),
    restart_policy={"Name": "on-failure"},
    wrapper_class=PostgresContainer,
)

qpc_server_image = build(path=constants.PROJECT_ROOT_DIR.as_posix())
qpc_server_container = container(
    scope="class",
    image="{qpc_server_image.id}",
    ports={
        "443/tcp": None,
    },
    environment=dict(
        QUIPUCORDS_LOG_LEVEL="ERROR",
        DJANGO_LOG_LEVEL="ERROR",
        QPC_DBMS="postgres",
        QPC_DBMS_DATABASE=constants.POSTGRES_DB,
        QPC_DBMS_HOST="{postgres_container.ips.primary}",
        QPC_DBMS_PASSWORD=constants.POSTGRES_PASSWORD,
        QPC_DBMS_USER=constants.POSTGRES_USER,
        QPC_SERVER_PASSWORD=constants.QPC_SERVER_PASSWORD,
        QPC_SERVER_USERNAME=constants.QPC_SERVER_USERNAME,
        QUIPUCORDS_COMMIT=constants.QPC_COMMIT,
    ),
    restart_policy={"Name": "always", "MaximumRetryCount": 5},
    wrapper_class=QuipucordsContainer,
)

scan_target_image = build(
    path=constants.PROJECT_ROOT_DIR.as_posix(),
    dockerfile="Dockerfile.scan-target",
)
scan_target_container = container(
    scope="module",
    image="{scan_target_image.id}",
    ports={
        "22/tcp": None,
    },
    wrapper_class=ScanTargetContainer,
)
# pylint: enable=no-value-for-parameter


@pytest.fixture(scope="class")
def apiclient(qpc_server_container: QuipucordsContainer):
    """QPC api client configured make requests to containerized qpc server."""
    client = ApiClient(
        base_url=urljoin(qpc_server_container.server_url, "api/v1/"),
    )
    client.auth = QPCAuth(
        base_url=qpc_server_container.server_url,
        username=constants.QPC_SERVER_USERNAME,
        password=constants.QPC_SERVER_PASSWORD,
    )
    return client
