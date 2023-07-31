from rest_framework import serializers

from sms_sender.models import Message, Client, Mailing


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'send_date', 'text']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'operator_code', 'teg']


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        fields = ['id', 'date_start', 'date_end', 'message', 'operator_code', 'teg']
