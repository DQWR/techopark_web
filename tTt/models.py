from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.forms import UserCreationForm


class CustomUser(AbstractUser):
    test_field = models.CharField(max_length=4)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Уникальное значение для поля groups
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Уникальное значение для поля user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        app_label = 'gukov_hw2'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'gukov_hw2'

# class Profile(models.Model):
#     class Meta:
#         app_label = 'gukov_hw2'
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.user.username} profile'


# Create your models here.


QUESTIONS = [
    {
        'id': f'{i}',
        'title': f'Question {i}',
        'text': f'Text {i}',
    } for i in range(23)
]
TAG = [
    {
        'text': f'{i}'
    }for i in range(23)
]


class QuestionManager(models.Manager):
    def get_best_questions(self):
        return self.order_by('-rating')

    def get_new_questions(self):
        return self.order_by('-created_at')

    def get_tag(self, tag_id):
        return self.filter(tag_id=tag_id)


class Question(models.Model):
    class Meta:
        app_label = 'gukov_hw2'
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(default=0)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    class Meta:
        app_label = 'gukov_hw2'
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.body


class Tag(models.Model):
    class Meta:
        app_label = 'gukov_hw2'
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Like(models.Model):
    class Meta:
        app_label = 'gukov_hw2'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    is_dislike = models.BooleanField(default=False)
