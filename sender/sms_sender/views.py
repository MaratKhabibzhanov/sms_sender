from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from sms_sender.models import Message, Client, Mailing, Report
from sms_sender.serializers import MessageSerializer, ClientSerializer, MailingSerializer, ReportSerializer
from sms_sender.tasks import make_sms_send


class MessageViewSet(ReadOnlyModelViewSet):
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
        if timezone.now() < instance.date_end:
            make_sms_send.apply_async((instance.id,), eta=instance.date_start)


class ReportViewSet(ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
