from django.contrib import admin

from sms_sender.models import Message, Client, Mailing, Teg, Report, Code

admin.site.register(Message)
admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Teg)
admin.site.register(Code)
admin.site.register(Report)
