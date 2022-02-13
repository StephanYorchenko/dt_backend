from django.urls import path

from .transport.handlers import me_info

urlpatterns = [
    path("me", me_info),
]