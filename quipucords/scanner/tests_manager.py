#
# Copyright (c) 2017-2018 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#
"""Test the scan manager capabilities."""

from multiprocessing import Process
from unittest.mock import Mock, patch

from django.test import TestCase

from api.models import ScanJob, ScanTask
from scanner.manager import Manager


class MockTask(Process):
    """Mock Task class."""

    # pylint: disable=invalid-name
    def __init__(self):
        """Create a mock task."""
        Process.__init__(self)
        self.id = 1
        self.scan_job = Mock()
        self.scan_job.status = ScanTask.PENDING
        self.identifier = 'TestScan'

    def log_message(self, message):
        """Fake log message."""
        pass


class ScanManagerTest(TestCase):
    """Tests against the Manager class and functions."""

    def setUp(self):
        """Create test case setup."""
        self.task = MockTask()
        self.scan_manager = Manager()
        self.scan_manager.start()

    def tearDown(self):
        """Cleanup test case setup."""
        if self.task.is_alive():
            self.task.terminate()

        if self.scan_manager.is_alive():
            self.scan_manager.running = False
            self.scan_manager.join()

    def test_put(self):
        """Test the put feature of the manager."""
        self.scan_manager.put(self.task)
        self.assertEqual(len(self.scan_manager.scan_queue), 1)

    # @patch.object(ScanJob.objects, "filter")
    def test_work(self):
        """Test the work function."""
        self.assertIsNone(self.scan_manager.current_job_runner)
        self.scan_manager.put(self.task)
        self.assertIsNone(self.scan_manager.current_job_runner)
        self.scan_manager.work()

    def test_kill_missing(self):
        """Test kill on missing id."""
        killed = self.scan_manager.kill(self.task, "cancel")
        self.assertFalse(killed)
