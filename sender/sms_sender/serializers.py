from rest_framework import serializers

from sms_sender.models import Message, Client, Mailing, Teg, Report, Code


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']


class TegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teg
        fields = ['id', 'teg']


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['id', 'operator_code']


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
        fields = ['id', 'date_start', 'date_end', 'message', 'operator_code', 'teg']

    def create(self, validated_data):
        message_data = validated_data.pop('message')
        validates_tegs = validated_data.pop('teg')
        validated_codes = validated_data.pop('operator_code')
        message = Message.objects.create(text=message_data['text'])
        validated_data['message'] = message
        tegs = Teg.objects.filter(teg__in=validates_tegs)
        codes = Code.objects.filter(operator_code__in=validated_codes)
        mailing = Mailing.objects.create(**validated_data)
        mailing.teg.set(tegs)
        mailing.operator_code.set(codes)

        return mailing



