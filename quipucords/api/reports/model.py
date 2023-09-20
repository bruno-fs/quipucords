"""Report and related models."""

import uuid

from django.db import models


class Report(models.Model):
    """Representation of a Report."""

    report_version = models.CharField(max_length=64, null=False)
    report_platform_id = models.UUIDField(default=uuid.uuid4)
