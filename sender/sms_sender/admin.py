from django.contrib import admin

from sms_sender.models import Message, Client, Mailing

admin.site.register(Message)
admin.site.register(Client)
admin.site.register(Mailing)
