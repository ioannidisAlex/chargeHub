import os

from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "common"

    def ready(self):
        # pass
        if os.getenv("BASE_DATA_LOADING_VAR") is None:
            import common.signals
