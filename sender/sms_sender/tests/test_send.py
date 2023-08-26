from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from sms_sender.models import Message, Teg, Code, Client, Report, Mailing
from sms_sender.tasks import make_sms_send


class MailingApiTestCase(TestCase):
    def setUp(self):
        self.teg_1 = Teg.objects.create(teg='not_my')
        self.teg_2 = Teg.objects.create(teg='is_my')
        self.teg_3 = Teg.objects.create(teg='neighbor')

        self.code_1 = Code.objects.create(operator_code='985')
        self.code_2 = Code.objects.create(operator_code='989')
        self.code_3 = Code.objects.create(operator_code='999')

        self.client_1 = Client.objects.create(phone='+79895854568',
                                              operator_code=self.code_2,
                                              teg=self.teg_1)
        self.client_2 = Client.objects.create(phone='+79855854668',
                                              operator_code=self.code_1,
                                              teg=self.teg_1)
        self.client_3 = Client.objects.create(phone='+79995840741',
                                              operator_code=self.code_3,
                                              teg=self.teg_2)
        self.client_4 = Client.objects.create(phone='+79895855568',
                                              operator_code=self.code_2,
                                              teg=self.teg_3)

        self.message_1 = Message.objects.create(text='Test message now')
        self.message_2 = Message.objects.create(text='Test message stop')
        self.message_3 = Message.objects.create(text='Test message past')

    def test_passed(self):
        self.assertEqual(0, Report.objects.all().count())
        mailing = Mailing.objects.create(
            date_start=timezone.now().__str__(),
            date_end=(timezone.now() + timedelta(days=3)).__str__(),
            message=self.message_1,
        )
        tegs = Teg.objects.filter(id__in=(self.teg_2.id, self.teg_3.id))
        codes = Code.objects.filter(id__in=(self.code_2.id,))
        mailing.teg.set(tegs)
        mailing.operator_code.set(codes)
        make_sms_send(mailing.id)
        self.assertEqual(3, Report.objects.all().count())

    def test_break(self):
        self.assertEqual(0, Report.objects.all().count())
        mailing = Mailing.objects.create(
            date_start=timezone.now().__str__(),
            date_end=(timezone.now() + timedelta(seconds=2)).__str__(),
            message=self.message_2,
        )
        tegs = Teg.objects.filter(id__in=(self.teg_2.id, self.teg_3.id))
        codes = Code.objects.filter(id__in=(self.code_2.id, self.code_1.id))
        mailing.teg.set(tegs)
        mailing.operator_code.set(codes)
        make_sms_send(mailing.id)
        self.assertEqual(2, Report.objects.all().count())

    def test_not_start(self):
        self.assertEqual(0, Report.objects.all().count())
        mailing = Mailing.objects.create(
            date_start=(timezone.now() - timedelta(days=2)).__str__(),
            date_end=(timezone.now() - timedelta(seconds=2)).__str__(),
            message=self.message_3,
        )
        tegs = Teg.objects.filter(id__in=(self.teg_2.id, self.teg_3.id))
        codes = Code.objects.filter(id__in=(self.code_2.id, self.code_1.id))
        mailing.teg.set(tegs)
        mailing.operator_code.set(codes)
        make_sms_send(mailing.id)
        self.assertEqual(0, Report.objects.all().count())
