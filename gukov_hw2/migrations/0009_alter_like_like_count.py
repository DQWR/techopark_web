# Generated by Django 3.2.12 on 2023-06-20 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gukov_hw2', '0008_alter_like_like_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like_count',
            field=models.IntegerField(default=824563),
        ),
    ]
