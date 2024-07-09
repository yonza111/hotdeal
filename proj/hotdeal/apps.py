from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)



class HotdealConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotdeal'
