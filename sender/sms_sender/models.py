from django.core.validators import RegexValidator
from django.db import models


class Message(models.Model):
    send_date = models.DateTimeField()
    text = models.TextField()


class Client(models.Model):
    phone = models.CharField(max_length=12, validators=(RegexValidator(regex=r'\+7(\d{10})'),))
    operator_code = models.CharField(max_length=3)
    teg = models.SlugField()


class Mailing(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    message = models.ForeignKey(Message, related_name='mailing', on_delete=models.PROTECT)
    client_filter = models.SlugField()
