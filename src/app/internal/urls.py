from django.urls import path

from .transport.web.handlers import me_info

urlpatterns = [
    path("me", me_info),
]
