from django.test import TestCase

from sms_sender.models import Teg
from sms_sender.serializers import TegSerializer


class TegSerializerTestCase(TestCase):
    def test_ok(self):
        self.teg_1 = Teg.objects.create(teg='not_my')
        self.teg_2 = Teg.objects.create(teg='is_my')
        tegs = Teg.objects.all()
        data = TegSerializer(tegs, many=True).data
        expected_data = [
            {
                'id': self.teg_1.id,
                'teg': 'not_my'
            },
            {
                'id': self.teg_2.id,
                'teg': 'is_my'
            }
        ]
        self.assertEqual(expected_data, data)
