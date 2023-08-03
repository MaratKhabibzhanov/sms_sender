from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from smsaero import SmsAero

from sms_sender.models import Mailing, Client, Report


SMSAERO_EMAIL = 'skylinegtr_r34@mail.ru'
SMSAERO_API_KEY = 't_eXAlYUE35w3wz-ytOD3z_LqbCjS25z'


@shared_task()
def make_sms_send(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    filter_data = mailing.client_filter.values_list('filter_data', flat=True)
    clients = Client.objects.filter(Q(teg__in=filter_data) |
                                     Q(operator_code__in=filter_data))
    for client in clients:
        result = send_sms(client.phone, str(mailing.message))
        if result.get('id'):
            Report.objects.create(message=mailing.message, client=client)
        if timezone.now() >= mailing.date_end:
            break


def send_sms(phone: int, message: str) -> dict:
    """
    Send sms and return results.

            Parameters:
                    phone (int): Phone number
                    message (str): Message to send

            Returns:
                    data (dict): API request result
    """
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    res = api.send(phone, message)
    assert res.get('success'), res.get('message')
    return res.get('data')
