from unicodedata import name
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/profile/<int:pk>", views.Profile.as_view(), name="profile")
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)