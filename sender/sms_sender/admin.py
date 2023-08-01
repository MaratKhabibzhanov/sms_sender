from django.contrib import admin

from sms_sender.models import Message, Client, Mailing, Tag, Report

admin.site.register(Message)
admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Tag)
admin.site.register(Report)
