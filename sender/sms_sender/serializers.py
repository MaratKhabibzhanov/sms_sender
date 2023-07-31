from rest_framework import serializers

from sms_sender.models import Message, Client, Mailing


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        fields = ['id', 'date_start', 'date_end', 'message', 'client_filter']
