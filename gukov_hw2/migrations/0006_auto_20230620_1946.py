# Generated by Django 3.2.12 on 2023-06-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gukov_hw2', '0005_like_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='like',
        ),
        migrations.AddField(
            model_name='like',
            name='like_count',
            field=models.IntegerField(default=551756),
        ),
    ]
