from django.contrib import admin

from .models import Topic
from .models import Question
from .models import Course
from .models import QuizQuestion
from .models import Subject


admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(QuizQuestion)
admin.site.register(Subject)

