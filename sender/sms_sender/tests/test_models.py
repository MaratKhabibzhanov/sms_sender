from django.test import TestCase

from sms_sender.models import Teg, Code, Message, Client


class TegModelTestCase(TestCase):
    def setUp(self):
        self.teg_1 = Teg.objects.create(teg='not_my')

    def test_str(self):
        teg = Teg.objects.get(id=self.teg_1.id)
        self.assertEqual('not_my', teg.__str__())


class CodeModelTestCase(TestCase):
    def setUp(self):
        self.code_1 = Code.objects.create(operator_code='999')

    def test_str(self):
        code = Code.objects.get(id=self.code_1.id)
        self.assertEqual('999', code.__str__())


class MessageModelTestCase(TestCase):
    def setUp(self):
        self.message_1 = Message.objects.create(text='Test message')

    def test_str(self):
        message = Message.objects.get(id=self.message_1.id)
        self.assertEqual('Test message', message.__str__())


class ClientModelTestCase(TestCase):
    def setUp(self):
        self.code_1 = Code.objects.create(operator_code='985')
        self.teg_1 = Teg.objects.create(teg='neighbor')
        self.client_1 = Client.objects.create(phone='+79855840256',
                                              operator_code=self.code_1,
                                              teg=self.teg_1)

    def test_str(self):
        client = Client.objects.get(id=self.client_1.id)
        self.assertEqual('+79855840256', client.__str__())
