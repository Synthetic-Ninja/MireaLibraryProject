# Generated by Django 3.2.18 on 2023-05-07 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0003_alter_booktype_time_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_empty',
            field=models.BooleanField(default=False),
        ),
    ]
