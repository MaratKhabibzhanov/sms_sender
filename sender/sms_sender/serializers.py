from rest_framework import serializers

from sms_sender.models import Message, Client, Mailing, Tag, Report


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['id', 'send_date', 'message', 'client']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'operator_code', 'teg']


class MailingSerializer(serializers.ModelSerializer):
    message = MessageSerializer()

    class Meta:
        model = Mailing
        fields = ['id', 'date_start', 'date_end', 'message', 'client_filter']

    def create(self, validated_data):
        message_data = validated_data.pop('message')
        message = Message.objects.create(text=message_data['text'])
        client_filter = validated_data.pop('client_filter')
        validated_data['message'] = message
        mailing = Mailing.objects.create(**validated_data)
        for tag in client_filter:
            mailing.client_filter.add(tag)

        return mailing



