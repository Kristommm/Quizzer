"""Defines URL patters for quizzer app."""

from django.urls import path

from . import views
# from .views import QuestionCreateView, QuestionListView, QuestionDetailView

app_name = 'quizzer_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Quiz page
    path('quiz/', views.quiz, name='quiz'),
    # Select quiz page
    path('make_quiz/', views.make_quiz, name='make_quiz'),
    # Select subjects
    path('pick_topics/<int:id>', views.pick_topics, name='pick_topics'),
    # Check quiz page
    path('check_quiz/', views.check_quiz, name='check_quiz'),
    # Custom quiz
    path('custom_quiz/', views.custom_quiz, name='custom_quiz'),
    # Quizzes List View
    path('my_quizzes', views.my_quizzes, name='my_quizzes'),
    # Select quiz
    path('my_quiz/<int:id>', views.my_quiz, name='my_quiz'),
    # # Create questions
    # path('question_create_form', QuestionCreateView.as_view(), name='question_create_form'),
    # # List of question
    # path('questions', QuestionListView.as_view(), name='questions'),
    # # Detail of question
    # path('question_detail/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
    # Stats
    path('my_stats/', views.my_stats, name='my_stats'),
    # Monthly Stats
    path('monthly_stats/<int:year>/<int:month>', views.monthly_stats, name='monthly_stats'),
]
