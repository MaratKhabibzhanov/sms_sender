import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sms_sender.models import Report, Client, Teg
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
