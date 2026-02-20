from django.contrib import admin
from .models import Exam, Question, Result

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Result)