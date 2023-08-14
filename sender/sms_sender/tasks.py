# import os
from celery import shared_task
from django.db.models import Q
from django.utils import timezone
# from smsaero import SmsAero

from sms_sender.models import Mailing, Client, Report


# SMSAERO_EMAIL = os.environ.get('SMS_EMAIL')
# SMSAERO_API_KEY = os.environ.get('SMS_API_KEY')


@shared_task()
def make_sms_send(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    operator_code = mailing.operator_code.all()
    teg = mailing.teg.all()
    clients = Client.objects.filter(Q(teg__in=teg) |
                                     Q(operator_code__in=operator_code))
    for client in clients:
        print(f'\nНомер телефона: {client}\nСообщение: \n{mailing.message}')
        Report.objects.create(message=mailing.message, client=client)
        if timezone.now() >= mailing.date_end:
            break

    # for client in clients:
    #     result = send_sms(client.phone, str(mailing.message))
    #     if result.get('id'):
    #         Report.objects.create(message=mailing.message, client=client)
    #     if timezone.now() >= mailing.date_end:
    #         break



# def send_sms(phone: int, message: str) -> dict:
#     """
#     Send sms and return results.
#
#             Parameters:
#                     phone (int): Phone number
#                     message (str): Message to send
#
#             Returns:
#                     data (dict): API request result
#     """
#     api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
#     res = api.send(phone, message)
#     assert res.get('success'), res.get('message')
#     return res.get('data')
