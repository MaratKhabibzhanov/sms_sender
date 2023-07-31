from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from sms_sender.models import Message, Client, Mailing
from sms_sender.serializers import MessageSerializer, ClientSerializer, MailingSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
