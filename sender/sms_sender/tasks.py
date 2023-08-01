import datetime
import time

from celery import shared_task
# from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F


@shared_task()
def set_price(subscription_id):
    pass
