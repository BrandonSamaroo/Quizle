from django.contrib import admin

from .models import Topic,Quiz,Score,Question, UserExtras

# Register your models here.
admin.site.register(Topic)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Score)
admin.site.register(UserExtras)
