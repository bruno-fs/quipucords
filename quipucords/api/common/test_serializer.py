import pytest
from rest_framework import serializers
from api.common.serializer import AlwaysManyMixin


class Normal(serializers.Serializer):
    inner_attr = serializers.CharField()


class InnerSerializer(AlwaysManyMixin, serializers.Serializer):
    inner_attr = serializers.CharField()


class OuterSerializer(serializers.Serializer):
    outer_attr = InnerSerializer()


class TestAlwaysManyMixin:
    def test_single_data(self):
        data = {"inner_attr": "foo"}
        s = InnerSerializer(data)
        assert s.data == [{"inner_attr": "foo"}]

    def test_nested_single_data(self):
        data = {"outer_attr": {"inner_attr": "foo"}}
        s = OuterSerializer(data)
        assert s.data == {"outer_attr": [{"inner_attr": "foo"}]}

    def test_many_data(self):
        data = [{"inner_attr": "foo"}, {"inner_attr": "bar"}]
        s = InnerSerializer(data)
        assert s.data == [{"inner_attr": "foo"}, {"inner_attr": "bar"}]

    # @pytest.mark.parametrize("factory", [list, tuple, set])
    def test_nested_many_data(self):
        data = {"outer_attr": [{"inner_attr": "foo"}, {"inner_attr": "bar"}]}
        s = OuterSerializer(data)
        assert s.data == {"outer_attr": [{"inner_attr": "foo"}, {"inner_attr": "bar"}]}

    def test_many_data2(self):
        data = [{"inner_attr": "foo"}, {"inner_attr": "bar"}]
        s = InnerSerializer(data=data)
        assert s.is_valid(), s.errors
        assert s.validated_data == [{"inner_attr": "foo"}, {"inner_attr": "bar"}]

    def test_nested_many_data2(self):
        data = {"outer_attr": [{"inner_attr": "foo"}, {"inner_attr": "bar"}]}
        s = OuterSerializer(data=data)
        assert s.is_valid(), s.errors
        assert s.data == {"outer_attr": [{"inner_attr": "foo"}, {"inner_attr": "bar"}]}

    def test_single_data2(self):
        data = {"inner_attr": "foo"}
        s = InnerSerializer(data=data)
        assert s.is_valid(), s.errors
        assert s.data == [{"inner_attr": "foo"}]

    def test_nested_single_data2(self):
        data = {"outer_attr": {"inner_attr": "foo"}}
        s = OuterSerializer(data=data)
        assert s.is_valid(), s.errors
        assert s.data == {"outer_attr": [{"inner_attr": "foo"}]}
