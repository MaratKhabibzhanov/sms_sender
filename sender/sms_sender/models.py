from django.core.validators import RegexValidator
from django.db import models, IntegrityError


class Code(models.Model):
    operator_code = models.CharField("Код оператора", max_length=3, unique=True)

    def __str__(self):
        return f'{self.operator_code}'


class Teg(models.Model):
    teg = models.SlugField("Тег", unique=True)

    def __str__(self):
        return f'{self.teg}'


class Message(models.Model):
    text = models.TextField("Текст сообщения")

    def __str__(self):
        return f'{self.text}'


class Client(models.Model):
    phone = models.CharField("Номер телефона", max_length=12, unique=True,
                             validators=(RegexValidator(regex=r'\+7(\d{10})'),))
    operator_code = models.ForeignKey(Code, verbose_name="Код оператора", on_delete=models.PROTECT)
    teg = models.ForeignKey(Teg, verbose_name="Тег", on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.phone}'


class Mailing(models.Model):
    date_start = models.DateTimeField("Дата создания рассылки")
    date_end = models.DateTimeField("Дата окончания рассылки")
    message = models.ForeignKey(Message, verbose_name="Сообщение", on_delete=models.PROTECT)
    operator_code = models.ManyToManyField(Code, verbose_name="Код оператора")
    teg = models.ManyToManyField(Teg, verbose_name="Тег")


class Report(models.Model):
    send_date = models.DateTimeField("Дата и время отправки", auto_now_add=True)
    message = models.ForeignKey(Message, verbose_name="Сообщение", on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name="Получатель", on_delete=models.PROTECT)
