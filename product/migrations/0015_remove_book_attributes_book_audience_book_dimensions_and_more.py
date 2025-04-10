# Generated by Django 5.1.8 on 2025-04-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_book_discount_book_stock_alter_book_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='attributes',
        ),
        migrations.AddField(
            model_name='book',
            name='audience',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='dimensions',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='format',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='page_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Weight (g)'),
        ),
        migrations.AlterField(
            model_name='book',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Discount percentage (0-100)', max_digits=5, verbose_name='Discount (%)'),
        ),
    ]
