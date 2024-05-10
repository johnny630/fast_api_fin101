import os
from functools import lru_cache
from dotenv import load_dotenv

class BaseConfig:
    load_dotenv()

    CELERY_broker_url: str = os.environ.get('CELERY_broker_url', 'redis://127.0.0.1:6379/1')
    result_backend: str = os.environ.get('result_backend', 'redis://127.0.0.1:6379/2')
    # https://www.cnblogs.com/baiyifengyun/p/17467861.html
    broker_connection_retry_on_startup = True


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()

settings = get_settings()
