"""Module for serializing all model object for database storage."""
from rest_framework.serializers import CharField, ChoiceField, JSONField

from api.common.serializer import NotEmptySerializer
from api.models import (
    RawFact,
    SystemInspectionResult,
)


class RawFactSerializer(NotEmptySerializer):
    """Serializer for the SystemInspectionResult model."""

    name = CharField(required=True, max_length=1024)
    value = JSONField(required=True)

    class Meta:
        """Metadata for serializer."""

        model = RawFact
        fields = ["name", "value"]
        qpc_allow_empty_fields = []


class SystemInspectionResultSerializer(NotEmptySerializer):
    """Serializer for the SystemInspectionResult model."""

    name = CharField(required=True, max_length=1024)
    status = ChoiceField(
        required=True, choices=SystemInspectionResult.CONN_STATUS_CHOICES
    )

    class Meta:
        """Metadata for serializer."""

        model = SystemInspectionResult
        fields = ["name", "status", "source", "facts"]
        qpc_allow_empty_fields = ["facts", "source"]
