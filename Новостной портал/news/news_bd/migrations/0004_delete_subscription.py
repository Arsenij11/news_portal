# Generated by Django 4.2.9 on 2024-05-22 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_bd', '0003_category_subscribers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
