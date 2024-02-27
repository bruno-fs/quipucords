"""Test ScanTask.get_facts."""

import pytest

from api.models import (
    RawFact,
    ScanJob,
    ScanTask,
    SystemInspectionResult,
)
from tests.factories import ScanJobFactory
from tests.utils.facts import random_name, random_value


@pytest.fixture
def raw_facts_list():
    """Fixture representing a list of random facts."""
    systems = []
    for _ in range(50):
        systems.append({random_name(): random_value() for _ in range(100)})
    return systems


@pytest.fixture
def inspection_scantask(raw_facts_list):
    """Scantask instance mapped to raw_facts_list."""
    scanjob = ScanJobFactory(scan_type=ScanTask.SCAN_TYPE_INSPECT)
    for i, facts in enumerate(raw_facts_list):
        system_inspection_result = SystemInspectionResult.objects.create(
            name=i,
        )
        system_inspection_result.scanjobs.add(scanjob)
        raw_fact_instances = [
            RawFact(
                name=fact_name,
                system_inspection_result=system_inspection_result,
                value=fact_value,
            )
            for fact_name, fact_value in facts.items()
        ]
        RawFact.objects.bulk_create(raw_fact_instances)

    scan_task = ScanTask.objects.create(
        scan_type=ScanTask.SCAN_TYPE_INSPECT,
        job=ScanJob.objects.create(),
    )
    return scan_task


def test_content(db, raw_facts_list, inspection_scantask: ScanTask):
    """Check if get_facts content is equal to the original data."""
    assert raw_facts_list == inspection_scantask.get_facts()


def test_number_of_queries(
    db,
    django_assert_max_num_queries,
    inspection_scantask: ScanTask,
):
    """Ensure get_facts makes only one query."""
    with django_assert_max_num_queries(1):
        inspection_scantask.get_facts()
