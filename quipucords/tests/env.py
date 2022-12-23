"""
env module.

Utilities for handling env vars in testing.
"""
import os
from functools import cached_property
from urllib.parse import urlparse, urlunparse


class EnvVar:
    """
    Environment value with an fallback value.

    The environment variable name will match the name of the attribute
    where this is instanciated.
    """

    def __init__(self, fallback_value, coercer=str):
        """Initialize EnvVar."""
        self.coercer = coercer
        self._fallback_value = fallback_value
        # env_var will be set when EnvVar becomes an attribute of another class
        self.env_var = None

    @cached_property
    def value(self):
        """Return the value from envvar (or fallback value)."""
        assert self.env_var
        val_from_env = os.environ.get(self.env_var)
        if val_from_env is None:
            return self.fallback_value
        return self.coercer(val_from_env)

    @cached_property
    def fallback_value(self):
        """Return the fallback value."""
        return self.coercer(self._fallback_value)

    def __set_name__(self, obj, name):
        """Set env var name."""
        self.env_var = name
        # coerce value/fallback value to validate'em
        self.value and self.fallback_value  # pylint: disable=pointless-statement

    def __str__(self):
        return self.value


class BaseURI:
    def __init__(self, uri: str):
        self._uri = uri
        self.parsed_uri = self.urlparse(self._uri)

    def __eq__(self, other):
        return self._uri == other

    def __str__(self) -> str:
        return self._uri

    def __hash__(self):
        return hash(self._uri)

    @property
    def scheme(self):
        return self.parsed_uri.scheme

    @property
    def host(self):
        return self.parsed_uri.hostname

    @property
    def port(self):
        return self.get_port(self.parsed_uri)

    @classmethod
    def get_port(cls, parsed_uri):
        _port = parsed_uri.port
        if _port is None:
            return {"https": 443, "http": 80}[parsed_uri.scheme]
        return _port

    @classmethod
    def urlparse(cls, uri):
        parsed_uri = urlparse(uri)
        scheme, host, *other_parts = parsed_uri  # pylint: disable=unused-variable
        if other_parts != [""] * 4:
            raise ValueError(
                f"URI ({uri}) should contain only schema, hostname and port"
            )
        return parsed_uri

    def replace_base_uri(self, uri):
        scheme, host, *other_parts = urlparse(uri)  # pylint: disable=unused-variable
        return urlunparse((self.scheme, f"{self.host}:{self.port}", *other_parts))


def as_bool(value) -> bool:
    if value.strip().lower() in ["0", "false", ""]:
        return False
    return True
