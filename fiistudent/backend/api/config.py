"""Base for configuration settings."""
from api import settings


class BaseConfig(object):

    """Common configuration."""

    DEBUG = False
    DATASTORE_NAMESPACE = None  # Uses [default] implicitly.


class ProductionConfig(BaseConfig):

    """What is used in production (cloud deployment) runs."""

    DATASTORE_NAMESPACE = "production"


class DevelopmentConfig(BaseConfig):

    """Used while doing local development & debugging."""

    DEBUG = True
    DATASTORE_NAMESPACE = "development"

DefaultConfig = DevelopmentConfig if settings.DEBUG else ProductionConfig

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": DefaultConfig,
}
