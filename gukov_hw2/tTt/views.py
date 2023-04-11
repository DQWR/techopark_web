from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render
from . import models
from django.http import HttpResponse


# Create your views here.
def index(request):
    # context = {"questions": models.QUESTIONS}
    pag = models.QUESTIONS
    context = {'objects': paginate(pag, request, 5)}
    return render(request, 'index.html', context)


def question(request, question_id):
    context = {"objects": models.QUESTIONS[question_id]}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'ask.html')


def bender(request, tag):
    context = {"objects": models.QUESTIONS[tag]}
    return render(request, 'question.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')


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

