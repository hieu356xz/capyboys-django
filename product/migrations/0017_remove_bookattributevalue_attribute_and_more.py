# Generated by Django 5.1.8 on 2025-04-10 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_migrate_eav_to_columns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookattributevalue',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='bookattributevalue',
            name='book',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='BookAttributeValue',
        ),
    ]
