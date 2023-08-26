import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

import sms_sender.views
from sms_sender.models import Report, Client, Teg, Code, Mailing, Message
from sms_sender.serializers import TegSerializer


class TegApiTestCase(APITestCase):
    def setUp(self):
        self.teg_1 = Teg.objects.create(teg='not_my')
        self.teg_2 = Teg.objects.create(teg='is_my')

    def test_get(self):
        url = reverse('teg-list')
        response = self.client.get(url)
        tegs = Teg.objects.all()
        serializer_data = TegSerializer(tegs, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(2, Teg.objects.all().count())
        url = reverse('teg-list')
        data = {"teg": "parents"}
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Teg.objects.all().count())

    def test_update(self):
        url = reverse('teg-detail', args=(self.teg_1.id,))
        data = {"teg": "parents"}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.teg_1.refresh_from_db()
        self.assertEqual("parents", self.teg_1.teg)

    def test_delete(self):
        self.assertEqual(2, Teg.objects.all().count())
        url = reverse('teg-detail', args=(self.teg_1.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Teg.objects.all().count())


class MailingApiTestCase(APITestCase):
    def setUp(self):
        self.teg_1 = Teg.objects.create(teg='not_my')
        self.teg_2 = Teg.objects.create(teg='is_my')
        self.teg_3 = Teg.objects.create(teg='neighbor')

        self.code_1 = Code.objects.create(operator_code='985')
        self.code_2 = Code.objects.create(operator_code='989')
        self.code_3 = Code.objects.create(operator_code='999')

        data_now = {
            "date_start": timezone.now().__str__(),
            "date_end": (timezone.now() + timedelta(days=3)).__str__(),
            "message": {"text": "Test message"},
            "operator_code": [
                self.code_1.id,
                self.code_2.id
            ],
            "teg": [
                self.teg_2.id,
                self.teg_3.id
            ]
        }
        self.json_data_now = json.dumps(data_now)
        self.date_start_future = (timezone.now() + timedelta(seconds=100))

        data_future = {
            "date_start": self.date_start_future.__str__(),
            "date_end": (timezone.now() + timedelta(days=3)).__str__(),
            "message": {"text": "Test message"},
            "operator_code": [
                self.code_1.id,
                self.code_2.id
            ],
            "teg": [
                self.teg_2.id,
                self.teg_3.id
            ]
        }
        self.json_data_future = json.dumps(data_future)

    def test_create(self):
        self.assertEqual(0, Mailing.objects.all().count())
        url = reverse('mailing-list')
        with patch('sms_sender.views.make_sms_send.apply_async'):
            response = self.client.post(url, data=self.json_data_now,
                                        content_type='application/json')
        message = Message.objects.all()[0]
        mailing = Mailing.objects.all()[0]
        tegs = Teg.objects.filter(id__in=(self.teg_2.id, self.teg_3.id))
        codes = Code.objects.filter(id__in=(self.code_1.id, self.code_2.id))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Mailing.objects.all().count())
        self.assertEqual("Test message", message.text)
        self.assertEqual(message, mailing.message)
        self.assertQuerysetEqual(codes, mailing.operator_code.all(), ordered=False)
        self.assertQuerysetEqual(tegs, mailing.teg.all(), ordered=False)

    def test_task_called(self):
        url = reverse('mailing-list')
        with patch('sms_sender.views.make_sms_send.apply_async') as mock_task:
            self.client.post(url, data=self.json_data_now,
                             content_type='application/json')
            self.assertTrue(mock_task.called)

    def test_task_called_future(self):
        url = reverse('mailing-list')
        with patch('sms_sender.views.make_sms_send.apply_async') as mock_task:
            self.client.post(url, data=self.json_data_future,
                             content_type='application/json')
            mailing = Mailing.objects.all()[0]
            self.assertTrue(mock_task.call_args)
            mock_task.assert_called_with((mailing.id,), eta=self.date_start_future)
