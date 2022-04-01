from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/signup', views.signup, name='signup'),
    path('', views.index, name='index'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)