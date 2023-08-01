from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from sms_sender.models import Message, Client, Mailing, Report
from sms_sender.serializers import MessageSerializer, ClientSerializer, MailingSerializer, ReportSerializer
from sms_sender.tasks import make_sms_send


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        make_sms_send.delay(instance.id)


class ReportViewSet(ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
