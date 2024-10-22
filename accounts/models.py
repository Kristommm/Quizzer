from django.db import models
from django.contrib.auth.models import User
from quizzer_app.models import Course

COURSES = [
    ("Mechanical Engineering", "Mechanical Engineering"),
    ("Civil Engineering", "Civil Engineering"),
    ("Electrical Engineering", "Electrical Engineering")
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.course}"