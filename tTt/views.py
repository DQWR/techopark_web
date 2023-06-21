import os
from math import ceil
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from .forms import ProfileEditForm
from . import models
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from random import randint
from datetime import datetime, timedelta
from .forms import LoginForm
from .forms import SignUpForm
from .models import Profile, Question, Like, Answer, Tag
from random import sample, choice
from django.shortcuts import get_object_or_404
from django.db.models import Count
import random
import logging
from django.db.models import F


logger = logging.getLogger(__name__)

@login_required(login_url='log_in', redirect_field_name='continue')
def index(request):
    questions = Question.objects.get_new_questions()
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    all_tags_count = Tag.objects.count()
    print('Users:', User.objects.count())
    print('Questions:', Question.objects.count())
    print('Answers:',  Answer.objects.count())
    print('Tags:', all_tags_count)
    print('Likes:', Like.objects.count())
    return render(request, 'index.html', context)
    # populate_likes_count()




@login_required(login_url='log_in', redirect_field_name='continue')
def best_questions(request):
    questions = Question.objects.get_best_questions()
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'best_questions.html', context)

@login_required(login_url='log_in', redirect_field_name='continue')
def tagged_questions(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    questions = Question.objects.get_tag(tag_id)
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'tag': tag,
        'page_obj': page_obj
    }
    return render(request, 'tagged_questions.html', context)

@login_required(login_url='log_in', redirect_field_name='continue')
def like_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        Question.objects.filter(id=question_id).update(likes_count=F('likes_count') + 1)

    return redirect('index')


@login_required(login_url='log_in', redirect_field_name='continue')
def dislike_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        Question.objects.filter(id=question_id).update(likes_count=F('likes_count') - 1)

    return redirect('index')

@login_required(login_url='log_in', redirect_field_name='continue')
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Создаем объект Paginator. Первый аргумент - это список объектов, которые мы хотим разбить на страницы. Второй аргумент - количество объектов на странице.
    paginator = Paginator(question.answers.all(), 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'question': question,
        'page_obj': page_obj,
    }
    return render(request, 'question.html', context)

@login_required(login_url='log_in', redirect_field_name='continue')
def like_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        page_number = request.POST.get('page')
        answer = Answer.objects.get(id=answer_id)
        answer.likes_count += 1
        answer.save()

        # Подготовьте URL-адрес для редиректа
        redirect_url = reverse('question', kwargs={'question_id': answer.question_id})

        # Добавьте номер страницы в URL-адрес
        if page_number:
            redirect_url += f'?page={page_number}'

        return redirect(redirect_url)

    return redirect('index')


@login_required(login_url='log_in', redirect_field_name='continue')
def dislike_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        page_number = request.POST.get('page')
        answer = Answer.objects.get(id=answer_id)
        answer.likes_count -= 1
        answer.save()

        # Подготовьте URL-адрес для редиректа
        redirect_url = reverse('question', kwargs={'question_id': answer.question_id})

        # Добавьте номер страницы в URL-адрес
        if page_number:
            redirect_url += f'?page={page_number}'

        return redirect(redirect_url)

    return redirect('index')

def ask(request):
    return render(request, 'ask.html')


@login_required(login_url='log_in', redirect_field_name='continue')
def add_question(request):
    if request.method == 'POST':
        # Process the form data and create a new question
        title = request.POST.get('title')
        text = request.POST.get('text')
        tags = request.POST.get('tags')

        # Check if title and text are provided
        if not title or not text:
            messages.error(request, 'You must provide both title and text.')
            return redirect('ask')

        question = Question(title=title, body=text, user=request.user)
        question.save()

        tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)

        return redirect(reverse('question', args=[question.id]))
    else:
        return redirect('ask')
def tagged_questions(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    questions = Question.objects.filter(tags=tag)
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'tag': tag,
        'page_obj': page_obj
    }
    return render(request, 'tagged_questions.html', context)


@login_required(login_url='log_in', redirect_field_name='continue')
def add_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        text = request.POST.get('text')

        answer = Answer.objects.create(
            body=text,
            user=request.user,
            question_id=question_id
        )

        total_answers = Answer.objects.filter(question_id=question_id).count()

        answers_per_page = 5
        last_page = (total_answers - 1) // answers_per_page + 1

        redirect_url = reverse('question', kwargs={'question_id': question_id})

        redirect_url += f'?page={last_page}'

        return redirect(redirect_url)

    return redirect('index')


def bender(request):
    latest_tags = Tag.objects.order_by('-id')[:4]  # Получаем последние 4 тега (можете изменить количество)
    context = {'latest_tags': latest_tags}
    return render(request, 'bender.html', context)

def notfound(request, exception):
    return render(request, '404.html', {}, status=404)

@csrf_protect
def log_in(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                request.session.modified = True  # Обновление сеанса пользователя
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', context={'form':login_form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.photo = form.cleaned_data.get('photo')
            profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required
def settings(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user=user, data=request.POST)

        if form.is_valid() and password_form.is_valid():
            # Обновление имени пользователя
            user.username = form.cleaned_data['nickname']
            user.save()

            # Обновление фотографии пользователя
            form.save()

            # Обновление пароля пользователя
            new_password = password_form.cleaned_data['new_password1']
            if new_password:
                user.set_password(new_password)
                user.save()

            request.session.modified = True  # Обновление сеанса пользователя

            return redirect('index')
    else:
        form = ProfileEditForm(instance=profile)
        password_form = PasswordChangeForm(user=user)

    return render(request, 'settings.html', {'form': form, 'password_form': password_form})


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        raise Http404("Page not found")
    return paginated_objects


def notfound(request, exception):
    return render(request, 'error.html', status=404)

def populate_likes_count():
    answers = Answer.objects.all()
    total_questions = answers.count()
    processed_questions = 0

    for answer in answers:
        answer.likes_count = random.randint(0, 100)
        answer.save()

        processed_questions += 1
        progress = processed_questions / total_questions * 100
        print(f"Processed question {processed_questions}/{total_questions} ({progress:.2f}%)")


def add_random_likes():
    questions = Question.objects.all()
    total_questions = questions.count()
    processed_questions = 0

    for question in questions:
        like = Like(user=random.choice(User.objects.all()), question=question)
        like.save()
        like.like_count = random.randint(0, 1000000)
        like.save()

        processed_questions += 1
        progress = processed_questions / total_questions * 100
        print(f"Processed question {processed_questions}/{total_questions} ({progress:.2f}%)")
def handle():
    ratio = 10000
    # Создаем пользователей
    # users = []
    # for i in range(ratio):
    #     user = User.objects.create_user(username=f'userdwq_1h{i}', email=f'userww{i}@example.com', password='password')
    #     users.append(user)
    #     print(f'user{i}')
    #
    # # Создаем тэги
    # tags = []
    # for i in range(ratio):
    #     tag = models.Tag.objects.create(name=f'tagv_q{i}')
    #     tags.append(tag)
    #     print(f'tag{i}')
    users = User.objects.all()
    tags = models.Tag.objects.all()

    # Создаем вопросы
    questions = models.Question.objects.all()
    # for i in range(ratio * 33):
    #     question = models.Question.objects.create(
    #         title=f'Title5 v5 n{i}',
    #         body=f'Body5 {i}',
    #         created_at=datetime.now() - timedelta(days=randint(0, 365)),
    #         user=users[randint(0, ratio - 1)]
    #     )
    #     question.tags.set([tags[randint(0, ratio - 1)]])
    #     questions.append(question)
    #     print(f'question{i}')

    # Создаем ответы
    answers = models.Answer.objects.all()
    # for i in range(ratio * 100):
    #     answer = models.Answer.objects.create(
    #         body=f'Bodym {i}',
    #         created_at=datetime.now() - timedelta(days=randint(0, 365)),
    #         user=users[randint(0, ratio - 1)],
    #         question=questions[randint(0, ratio * 10 - 1)]
    #     )
    #     answers.append(answer)
    #     print(f'answer{i}')

    # Создаем оценки пользователей
    likes = []
    # for i in range(ratio * 15):
    #     like = models.Like.objects.create(
    #         user=users[randint(0, ratio - 1)],
    #         question=questions[randint(0, ratio * 10 - 1)],
    #         answer=answers[randint(0, ratio * 100 - 1)],
    #         is_like=True,
    #         is_dislike=False
    #     )
    #     likes.append(like)
    #     print(f'likse{i}')

