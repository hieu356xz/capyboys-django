# Generated by Django 5.1.7 on 2025-03-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_add_initial_data_to_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_img',
            field=models.ImageField(blank=True, max_length=511, null=True, upload_to='covers/'),
        ),
    ]
