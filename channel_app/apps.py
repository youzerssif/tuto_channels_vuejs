from django.apps import AppConfig


class ChannelAppConfig(AppConfig):
    name = 'channel_app'
    
    def ready(self):
        from .auto import updater

        updater.start()
