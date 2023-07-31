from django.core.validators import RegexValidator
from django.db import models


class Message(models.Model):
    send_date = models.DateTimeField("Дата создания")
    text = models.TextField("Текст сообщения")

    def __str__(self):
        return f'{self.text}'


class Client(models.Model):
    phone = models.CharField("Номер телефона", max_length=12, validators=(RegexValidator(regex=r'\+7(\d{10})'),))
    operator_code = models.CharField("Код оператора", max_length=3)
    teg = models.SlugField("Тег")

    # def __str__(self):
    #     return f'{self.operator_code}, {self.teg}'


class Mailing(models.Model):
    date_start = models.DateTimeField("Дата создания рассылки")
    date_end = models.DateTimeField("Дата окончания рассылки")
    message = models.ForeignKey(Message, verbose_name="Сообщение", related_name='mailing', on_delete=models.PROTECT)
    client_filter = models.SlugField("Метки для фильтра клиентов")
