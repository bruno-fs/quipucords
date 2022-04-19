from contextlib import suppress
from unittest.mock import patch

import pytest


def _kill_scan_manager(manager_instance):
    for job in manager_instance.scan_queue:
        with suppress(AttributeError):
            job.terminate()

    manager_instance.running = False
    if manager_instance.is_alive():
        manager_instance.join()


@pytest.fixture(autouse=True)
def scan_manager():
    from scanner import manager

    _kill_scan_manager(manager.SCAN_MANAGER)
    scan_manager_instance = manager.SCAN_MANAGER = manager.Manager()
    with (
        patch.object(manager, "sleep"),
        patch.object(scan_manager_instance.__class__, "__call__", _call_itself),
    ):
        yield scan_manager_instance

    _kill_scan_manager(scan_manager_instance)


def _call_itself(instance):
    return instance


@pytest.fixture(autouse=True)
def patch_scan_manager(scan_manager):
    with (
        # patch.object(scan_manager.__class__, "__call__", _call_itself),
        patch("api.signal.scanjob_signal.manager.Manager", scan_manager),
        patch("api.signal.scanjob_signal.manager.SCAN_MANAGER", scan_manager),
        patch("scanner.tests_manager.Manager", scan_manager),
    ):
        yield
