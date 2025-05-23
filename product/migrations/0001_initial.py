# Generated by Django 5.1.7 on 2025-03-14 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=511)),
                ('value', models.CharField(max_length=511)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=511)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=511)),
                ('address', models.TextField()),
                ('website', models.URLField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=511)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('publish_year', models.IntegerField(blank=True, null=True)),
                ('cover_img', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.author')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='BookAtribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.atribute')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.book')),
            ],
        ),
    ]
