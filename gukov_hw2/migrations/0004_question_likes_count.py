# Generated by Django 3.2.12 on 2023-06-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gukov_hw2', '0003_auto_20230524_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]
