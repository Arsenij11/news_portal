# Generated by Django 5.0.7 on 2024-07-15 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_bd', '0004_post_text_en_us_post_text_ru_post_title_en_us_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_name_en_us',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name_ru',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
