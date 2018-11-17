from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DataChimpConfig(AppConfig):
    name = 'datachimp'
    verbose_name = 'DataChimp'

    def ready(self):
        import datachimp.signals
