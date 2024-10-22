from typing import Any
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import GroupRequiredMixin
from django.http import Http404
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import F

from .models import Question, Subject, QuizQuestion
from accounts.models import UserProfile
from django.contrib.auth.models import User

from random import shuffle, choice
from datetime import date

def index(request):
    """The home page for quizzer app"""
    return render(request, 'quizzer_app/index.html')


@login_required()
def quiz(request):
    """Show all questions."""
    course = UserProfile.objects.filter(user=request.user)[0].course
    picked_subject = choice(Subject.objects.filter(course=course).values_list('subject', flat=True))
    topics = Subject.objects.filter(subject=picked_subject)[0].topic.all()
    raw_questions = []
    if not course or not picked_subject or not topics:
        return Http404
    for topic in topics:
        questions = Question.objects.filter(topic=topic)
        for question in questions:
            raw_questions.append(question)
    shuffle(raw_questions)
    questions = raw_questions[:50]
    context = {'questions': questions, 'picked_subject': picked_subject}
    return render(request, 'quizzer_app/quiz.html', context)


@login_required()
def check_quiz(request):
    """Show the result of the quiz."""
    answers = request.POST.dict()
    if not answers:
        # set message
        return Http404
    answers_dict = {}
    quiz_string = ''
    subject = None

    for key, value in answers.items():
        if key == 'csrfmiddlewaretoken':
            continue
        elif key == 'subject':
            subject = value
            continue
        else:
            answers_dict[key] = value

    score = 0
    response = []
    for key, value in answers_dict.items():
        quiz_string += key
        quiz_string = quiz_string + ',' + value + ','
        picked_question = Question.objects.filter(pk=key)
        question = picked_question.values().get()['question']
        letter = picked_question.values().get()['answer']
        correct_answer = picked_question.values().get()[f'option_{letter}']
        if value == '':
            user_answer = 'no answer'
        else:
            user_answer = picked_question.values().get()[f'option_{value}']
        
        response.append({
            'question': question,
            'correct_answer': correct_answer,
            'user_answer': user_answer
        })
        if correct_answer == user_answer:
            score += 1
            picked_question.update(
                times_answered_correctly = F('times_answered_correctly') + 1
            )
        picked_question.update(
            times_answered = F('times_answered') + 1
        )
        
    score = f"{score}/{len(response)}"


    quiz = QuizQuestion(quiz_string=quiz_string, score=score, owner=request.user, subject=subject)
    quiz.save()
    
    context = {'response': response, 'score': score}
    return render(request, 'quizzer_app/check_quiz.html', context=context)


@login_required()
def make_quiz(request):
    user = User.objects.get(username = request.user)
    course = UserProfile.objects.get(user=user).course
    subjects = Subject.objects.filter(course=course)
    if not user or not course or not subjects:
        return Http404
    context = {'subjects': subjects}
    return render(request, 'quizzer_app/make_quiz.html', context=context)


@login_required()
def pick_topics(request, id):
    user_course = UserProfile.objects.get(user=request.user).course
    picked_subject = get_object_or_404(Subject, id=id)
    subject_course = picked_subject.course.all()
    if user_course not in subject_course:
        raise Http404
    if not user_course or not picked_subject or not subject_course:
        raise Http404
    else:
        request.session["quiz_status"] = "topics_picked"
        topics = picked_subject.topic.all()
        context = {"topics": topics, "picked_subject": picked_subject}
        return render(request, 'quizzer_app/pick_topics.html', context=context)


@login_required()
def custom_quiz(request):
    if request.session["quiz_status"] != "topics_picked":
        raise Http404
    request.session["quiz_status"] = "done"
    topics = request.GET.dict()
    if not topics:
        return Http404
    raw_questions = []
    subject = None
    for key, topic_id in topics.items():
        if key == 'subject':
            subject = topic_id
        else:
            picked_questions = Question.objects.filter(topic_id=topic_id)
            for question in picked_questions:
                raw_questions.append(question)
    

    shuffle(raw_questions)
    questions = raw_questions[:50]
    context = {"questions": questions, "subject": subject}
    return render(request, 'quizzer_app/custom_quiz.html', context=context)


@login_required
def my_quizzes(request):
    quizzes = QuizQuestion.objects.filter(owner=request.user).order_by('date_taken')
    if not quizzes:
        return Http404
    context = {"quizzes": quizzes}
    return render(request, 'quizzer_app/my_quizzes.html', context=context)


@login_required
def my_quiz(request, id):
    quiz = get_object_or_404(QuizQuestion, pk=id)
    if quiz.owner != request.user:
        raise Http404
    quiz_list = quiz.quiz_string.split(',')
    quiz_list.pop()
    quiz_questions = []
    for i in range(len(quiz_list)):
        if i % 2 == 0:
            question = Question.objects.filter(id=int(quiz_list[i])).values().get()['question']
            letter = Question.objects.filter(id=int(quiz_list[i])).values().get()['answer']
            correct_answer = Question.objects.filter(id=int(quiz_list[i])).values().get()[f'option_{letter}']
            if quiz_list[i+1] == '':
                user_answer = 'no answer'
            else:
                user_answer = Question.objects.filter(id=int(quiz_list[i])).values().get()[f'option_{quiz_list[i+1]}']
            quiz_questions.append({
                'question': question,
                'correct_answer': correct_answer,
                'user_answer': user_answer
            })
    context = {'quiz_questions':quiz_questions , 'score': quiz.score}
    return render(request, 'quizzer_app/my_quiz.html', context=context)

@login_required
def my_stats(request):
    data = {}
    average_per_subject = {}
    overall_quiz_string = ''
    current_date = date.today()
    
    user_course = UserProfile.objects.get(user=request.user).course
    subjects = list(Subject.objects.filter(course=user_course).values_list('subject', flat=True))
    quizzes = QuizQuestion.objects.filter(owner=request.user).values('quiz_string')

    if not user_course or not subjects or not quizzes:
        return Http404

    for subject in subjects:
        total_score = 0
        scores = QuizQuestion.objects.filter(owner=request.user, subject=subject).values_list('score')
        for score in scores:
            total_score += int(score[0].split('/')[0])
        try:
            average_per_subject[subject]='{0:.2f}'.format(total_score/(50*len(scores)) * 100)
        except ZeroDivisionError:
            average_per_subject[subject] = 0
    
    for quiz in quizzes:
        overall_quiz_string += quiz['quiz_string']
    overall_quiz_string = overall_quiz_string.split(',')
    overall_quiz_string.pop()

    for subject in subjects:
        data[subject] = {}
        topics = list(Subject.objects.filter(subject=subject)[0].topic.all().values_list('topic', flat=True))
        for i in range(len(overall_quiz_string)):
            if i % 2 == 0:
                question = Question.objects.get(id=overall_quiz_string[i])
                question_topic = question.topic.topic
                if question_topic in topics:
                    answer = overall_quiz_string[i+1]
                    correct_answer = question.answer
                    if question_topic not in data[subject].keys():
                        data[subject][question_topic] = {'total':  1}
                        if answer == correct_answer:
                            data[subject][question_topic]['total_correct'] = 1
                        else:
                            data[subject][question_topic]['total_correct'] = 0
                    else:
                        data[subject][question_topic]['total'] += 1
                        if answer == correct_answer:
                            data[subject][question_topic]['total_correct'] += 1

    context = {'data': data, 'current_date': current_date, 'average_per_subject': average_per_subject}
    return render(request, 'quizzer_app/my_stats.html', context=context)

@login_required
def monthly_stats(request, year, month):
    data = {}
    average_per_subject = {}
    overall_quiz_string = ''
    try:
        base_date = date(year=year, month=month, day=1)
    except ValueError:
        raise Http404
    else:
        if base_date.month < 12 and base_date.month > 1:
            next_month = date(year=year, month=base_date.month + 1, day=1)
            previous_month = date(year=year, month=base_date.month - 1, day=1)
        elif base_date.month == 1:
            next_month = date(year=year, month=base_date.month + 1, day=1)
            previous_month = date(year=year-1, month=12, day=1)
        elif base_date.month == 12:
            next_month = date(year=year+1, month=1, day=1)
            previous_month = date(year=year, month=base_date.month-1, day=1)

        user_course = UserProfile.objects.get(user=request.user).course
        subjects = list(Subject.objects.filter(course=user_course).values_list('subject', flat=True))
        quizzes = QuizQuestion.objects.filter(owner=request.user, date_taken__year=year, date_taken__month=month).values('quiz_string')

        # Get average per subject

        for subject in subjects:
            total_score = 0
            scores = QuizQuestion.objects.filter(owner=request.user, subject=subject, date_taken__year=year, date_taken__month=month).values_list('score')
            for score in scores:
                total_score += int(score[0].split('/')[0])
            try:
                average_per_subject[subject]='{0:.2f}'.format(total_score/(50*len(scores)) * 100)
            except ZeroDivisionError:
                average_per_subject[subject] = 0
        
        for quiz in quizzes:
            overall_quiz_string += quiz['quiz_string']
        overall_quiz_string = overall_quiz_string.split(',')
        overall_quiz_string.pop()

        for subject in subjects:
            data[subject] = {}
            topics = list(Subject.objects.filter(subject=subject)[0].topic.all().values_list('topic', flat=True))
            for i in range(len(overall_quiz_string)):
                if i % 2 == 0:
                    question = Question.objects.get(id=overall_quiz_string[i])
                    question_topic = question.topic.topic
                    if question_topic in topics:
                        answer = overall_quiz_string[i+1]
                        correct_answer = question.answer
                        if question_topic not in data[subject].keys():
                            data[subject][question_topic] = {'total':  1}
                            if answer == correct_answer:
                                data[subject][question_topic]['total_correct'] = 1
                            else:
                                data[subject][question_topic]['total_correct'] = 0
                        else:
                            data[subject][question_topic]['total'] += 1
                            if answer == correct_answer:
                                data[subject][question_topic]['total_correct'] += 1

        context = {'data': data, 'base_date': base_date, 'previous_month': previous_month, 'next_month': next_month, 'average_per_subject': average_per_subject }

        return render(request, 'quizzer_app/monthly_stats.html', context=context)


@login_required
def my_quiz(request, id):
    quiz = get_object_or_404(QuizQuestion, pk=id)
    if quiz.owner != request.user:
        raise Http404
    quiz_list = quiz.quiz_string.split(',')
    quiz_list.pop()
    quiz_questions = []
    for i in range(len(quiz_list)):
        if i % 2 == 0:
            question = Question.objects.filter(id=int(quiz_list[i])).values().get()['question']
            letter = Question.objects.filter(id=int(quiz_list[i])).values().get()['answer']
            correct_answer = Question.objects.filter(id=int(quiz_list[i])).values().get()[f'option_{letter}']
            if quiz_list[i+1] == '':
                user_answer = 'no answer'
            else:
                user_answer = Question.objects.filter(id=int(quiz_list[i])).values().get()[f'option_{quiz_list[i+1]}']
            quiz_questions.append({
                'question': question,
                'correct_answer': correct_answer,
                'user_answer': user_answer
            })
    context = {'quiz_questions':quiz_questions , 'score': quiz.score}
    return render(request, 'quizzer_app/my_quiz.html', context=context)


# class QuestionCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
#     model = Question
#     fields = ['topic', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer']
#     template_name = 'quizzer_app/question_create_form.html'
#     success_url = 'question_create_form'
#     group_required = [u'contributors']

#     def form_valid(self, form):
#         form.instance.contributor = self.request.user
#         return super().form_valid(form)

# class QuestionListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
#     model = Question
#     paginate_by = 20
#     context_object_name = 'question_list'
#     template_name = 'quizzer_app/questions.html'
#     group_required = [u'contributors']

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         return super().get_context_data(**kwargs)
    

# class QuestionDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
#     model = Question
#     context_object_name = 'question'
#     template_name = 'quizzer_app/question_detail.html'
#     group_required = [u'contributors']

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         return super().get_context_data(**kwargs)