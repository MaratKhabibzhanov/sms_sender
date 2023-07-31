from django.core.validators import RegexValidator
from django.db import models
from django.db.transaction import TransactionManagementError


class Message(models.Model):
    send_date = models.DateTimeField("Дата создания")
    text = models.TextField("Текст сообщения")

    def __str__(self):
        return f'{self.text}'


class Client(models.Model):
    phone = models.CharField("Номер телефона", max_length=12, validators=(RegexValidator(regex=r'\+7(\d{10})'),))
    operator_code = models.CharField("Код оператора", max_length=3)
    teg = models.SlugField("Тег")

    def save(self, *args, **kwargs):
        try:
            tags = Tag(operator_code=None, teg=self.teg)
            tags.save()
        except TransactionManagementError:
            pass
        return super().save(*args, **kwargs)


class Tag(models.Model):
    operator_code = models.CharField(max_length=3, unique=True, null=True)
    teg = models.SlugField(unique=True, null=True)


class Mailing(models.Model):
    date_start = models.DateTimeField("Дата создания рассылки")
    date_end = models.DateTimeField("Дата окончания рассылки")
    message = models.ForeignKey(Message, verbose_name="Сообщение", related_name='mailing', on_delete=models.PROTECT)
    operator_code = models.ForeignKey(Tag, to_field='operator_code', verbose_name="Код оператора",
                                      related_name='mailing_code', on_delete=models.PROTECT)
    teg = models.ForeignKey(Tag, to_field='teg', verbose_name="Тег",
                            related_name='mailing_teg', on_delete=models.PROTECT)
