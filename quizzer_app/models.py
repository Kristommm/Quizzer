from django.contrib.auth.models import User
import uuid

from django.db import models


OPTIONS = [
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
    ("d", "D")
]

COURSES = [
    ("Mechanical Engineering", "Mechanical Engineering"),
    ("Civil Engineering", "Civil Engineering"),
    ("Electrical Engineering", "Electrical Engineering")
]


class Course(models.Model):
    """Course of the student"""
    course = models.CharField(max_length=100, choices=COURSES)

    def __str__(self):
        return self.course

class Topic(models.Model):
    """Topic of the question"""
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.topic
    
class Subject(models.Model):
    """Course of the student"""
    subject = models.CharField(max_length=100)
    topic = models.ManyToManyField(Topic)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.subject


class Question(models.Model):
    """Questions to be asked in the quiz"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    question = models.TextField()
    option_a = models.CharField(max_length=100, null=True)
    option_b = models.CharField(max_length=100, null=True)
    option_c = models.CharField(max_length=100, null=True)
    option_d = models.CharField(max_length=100, null=True)
    answer = models.CharField(max_length=1, choices=OPTIONS)
    contributor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    times_answered = models.IntegerField(default=0)
    times_answered_correctly = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question[:50]}..."


class QuizQuestion(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
    quiz_string = models.TextField(null=True)
    score = models.CharField(max_length=10, null=True)
    date_taken = models.DateTimeField(auto_now_add=True, null=True)
    subject = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return f'{self.owner}, {self.score}'