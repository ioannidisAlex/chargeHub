from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'common'

    def ready(self):
    	from common import signals
