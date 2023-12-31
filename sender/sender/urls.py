"""sender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from sms_sender.views import MessageViewSet, ClientViewSet, MailingViewSet, ReportViewSet, CodeViewSet, TegViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'api/messages', MessageViewSet)
router.register(r'api/clients', ClientViewSet)
router.register(r'api/mailing', MailingViewSet)
router.register(r'api/report', ReportViewSet)
router.register(r'api/code', CodeViewSet)
router.register(r'api/teg', TegViewSet)

urlpatterns += router.urls
