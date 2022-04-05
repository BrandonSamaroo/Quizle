from unicodedata import name
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/signup', views.signup, name='signup'),
    path("", views.home, name="home"),
    path("accounts/profile/<int:pk>", views.Profile.as_view(), name="profile"),
    path("topics/", views.Topics.as_view(), name="topics"),
    path("search/", views.search, name="search"),
    path("createquiz/", views.create_quiz, name="create_quiz"),
    path("createquiz/questions/", views.create_quiz_questions, name="create_quiz_questions"),
    path("createquiz/post/", views.create_quiz_post, name="create_quiz_post"),
    path('topics/<int:topic_id>/unassoc_topic/', views.unassoc_topic, name='unassoc_topic'),
    # path("topics/follow/", views.follow_topic, name='follow_topic')
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)