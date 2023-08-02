from django.utils import timezone

from celery import shared_task
from django.db.models import Q
from sms_sender.models import Mailing, Client, Report


@shared_task()
def make_sms_send(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    filter_data = mailing.client_filter.values_list('filter_data', flat=True)
    clients = Client.objects.filter(Q(teg__in=filter_data) |
                                     Q(operator_code__in=filter_data))
    for client in clients:
        Report.objects.create(message=mailing.message, client=client)
        if timezone.now() >= mailing.date_end:
            break
