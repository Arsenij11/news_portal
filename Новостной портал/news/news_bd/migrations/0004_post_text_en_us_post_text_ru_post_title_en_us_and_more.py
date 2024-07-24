# Generated by Django 5.0.7 on 2024-07-15 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_bd', '0003_category_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='type_post_en_us',
            field=models.CharField(choices=[('AR', 'Статья'), ('NE', 'Новость')], default='NE', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='type_post_ru',
            field=models.CharField(choices=[('AR', 'Статья'), ('NE', 'Новость')], default='NE', max_length=2, null=True),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
