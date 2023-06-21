"""gukov_hw2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tTt import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('bender/', views.bender, name='bender'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.signup, name='register'),
    path('settings/', views.settings, name='settings'),
    path('best_questions/', views.best_questions, name='best_questions'),
    path('like_question/', views.like_question, name='like_question'),
    path('dislike_question/', views.dislike_question, name='dislike_question'),
    path('tagged_questions/<int:tag_id>/', views.tagged_questions, name='tagged_questions'),
    path('like-answer/', views.like_answer, name='like_answer'),
    path('dislike-answer/', views.dislike_answer, name='dislike_answer'),
    path('add-answer/', views.add_answer, name='add_answer'),
    path('add_question/', views.add_question, name='add_question'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'tTt.views.notfound'