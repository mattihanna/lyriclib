from django.apps import AppConfig


class MyapiConfig(AppConfig):
    
    name = 'myapi'

    def ready(self):
        import myapi.signals