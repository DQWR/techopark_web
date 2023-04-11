from django.db import models

# Create your models here.
QUESTIONS = [
    {
        'id': f'{i}',
        'title': f'Question {i}',
        'text': f'Text {i}',
    }for i in range(23)
]
