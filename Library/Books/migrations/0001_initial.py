# Generated by Django 3.2.18 on 2023-04-28 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookRubric',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('time_limit', models.PositiveIntegerField(default=0)),
                ('forfeit', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_available', models.BooleanField()),
                ('image', models.ImageField(upload_to='books_images')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('authors', models.TextField()),
                ('created_year', models.PositiveIntegerField()),
                ('created_place', models.CharField(max_length=128)),
                ('pages_count', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('count', models.PositiveIntegerField()),
                ('rubric', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Books.bookrubric')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.booktype')),
            ],
        ),
    ]