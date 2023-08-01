from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import RegexValidator
from django.db import models, IntegrityError
from django.db.transaction import TransactionManagementError


class Message(models.Model):
    text = models.TextField("Текст сообщения")

    def __str__(self):
        return f'{self.text}'


class Client(models.Model):
    phone = models.CharField("Номер телефона", max_length=12, unique=True,
                             validators=(RegexValidator(regex=r'\+7(\d{10})'),))
    operator_code = models.CharField("Код оператора", max_length=3)
    teg = models.SlugField("Тег")

    def __str__(self):
        return f'{self.phone}'

    def save(self, *args, **kwargs):
        for filter_criterion in self.teg, self.operator_code:
            try:
                obj, created = Tag.objects.get_or_create(filter_data=filter_criterion)
                if created:
                    obj.save()
            except IntegrityError:
                continue
            except MultipleObjectsReturned:
                continue
            except Exception as e:
                raise e
        return super().save(*args, **kwargs)


class Tag(models.Model):
    filter_data = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.filter_data}'


class Mailing(models.Model):
    date_start = models.DateTimeField("Дата создания рассылки")
    date_end = models.DateTimeField("Дата окончания рассылки")
    message = models.ForeignKey(Message, verbose_name="Сообщение",
                                related_name='mailing', on_delete=models.PROTECT)
    client_filter = models.ManyToManyField(Tag, verbose_name="Данные для фильтрации",
                                           related_name='mailing_filter')

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Report(models.Model):
    send_date = models.DateTimeField("Дата и время отправки", auto_now_add=True)
    message = models.ForeignKey(Message, verbose_name="Сообщение",
                                related_name='report', on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name="Получатель",
                               related_name='report', on_delete=models.PROTECT)
