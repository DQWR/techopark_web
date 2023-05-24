import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from .forms import ProfileEditForm
from . import models
from django.http import HttpResponse
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from random import randint
from datetime import datetime, timedelta
from .forms import LoginForm
from .forms import SignUpForm
from .models import Profile
from random import sample, choice


@login_required(login_url='log_in', redirect_field_name='continue')
def index(request):
    likes_count = models.Like.objects.all()
    # all_tags = list(models.Tag.objects.all())  # Получаем все тэги
    # random_tags = sample(all_tags, 2) if len(all_tags) >= 2 else all_tags  # Получаем два случайных тэга
    # pag = models.Question.objects.get_best_questions()
    # all_answers = list(models.Answer.objects.all())  # Получаем все ответы
    # random_answer = choice(all_answers) if all_answers else None  # Получаем один случайный ответ
    # all_likes = list(models.Like.objects.all())  # Получаем все "likes"
    # random_user = choice(all_likes).user.username if all_likes else ""  # Получаем случайное имя пользователя


    context = {
        "questions": models.QUESTIONS,
        # "random_tags": random_tags,
        # "random_answer": random_answer,
        # "random_user": random_user,
        # "objects": paginate(pag, request, 5)
    }

    return render(request, 'index.html', context)


def question(request, question_id):
    context = {"objects": models.QUESTIONS[question_id]}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'ask.html')


def bender(request):
    # context = {"objects": models.QUESTIONS[tag]}
    return render(request, 'bender.html')


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
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', context={'form':login_form})


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.photo = form.cleaned_data.get('photo')
            profile.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required
def settings(request):
    user = request.user
    profile = user.profile
    if hasattr(user, 'profile'):
        profile = user.profile
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Обновление имени пользователя
            user.username = form.cleaned_data['nickname']
            user.save()

            # Обновление пароля пользователя
            password = form.cleaned_data['password']
            if password:
                user.set_password(password)
                user.save()

            form.save()
            return redirect('index')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'settings.html', {'form': form})


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

