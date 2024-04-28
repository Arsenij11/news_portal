from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news import settings
from .models import Post, Category, PostCategory
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

def send_notifications(preview, pk, title, subscribers, name_category):
    html_content = render_to_string('post_created_email.html', {'text': preview, 'link': f'{settings.SITE_URL}/news/{pk}', 'name_category': name_category})
    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=[subscribers])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_last_news(data,email):
    text_content = f'Вот последние новости за неделю:\n\n'
    html_content = f'Вот последние новости за неделю:<br><br>'
    for text, pk_and_title in data.items():
        pk = pk_and_title[0]
        title = pk_and_title[1]
        text_content += f'{title}\n\n{text}Читать продолжение в источнике: {settings.SITE_URL}/news/{pk}\n\n\n'
        html_content += f'<b>{title}</b><br><br>{text}<a href = "{settings.SITE_URL}/news/{pk}">Читать продолжение в источнике</a><br><br><br>'
    msg = EmailMultiAlternatives(subject='Последние новости за неделю', body=text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def notify_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    post_categories = PostCategory.objects.filter(post_id_id=pk)
    categories = []
    for post_category in post_categories:
        categories.append(Category.objects.get(pk=post_category.category_id_id))
    subscribers = {}

    for category in categories:
        subscribers[category.category_name] = []
        all_subs = category.subscribers.all()
        email_subs = [s.email for s in all_subs]
        for i in email_subs:
            subscribers[category.category_name].append(i)


    for name_category,emails in subscribers.items():
        for email in emails:
            send_notifications(post.preview(), post.pk, post.title, email, name_category)

@shared_task
def last_news():
    posts = Post.objects.filter(type_post='NE').exclude(time_post__lt=timezone.now()-timedelta(weeks=1))
    data = {}
    for post in posts:
        data[post.preview()] = [post.pk, post.title]
    all_users = User.objects.all()
    emails = [s.email for s in all_users]
    for email in emails:
        send_last_news(data,email)

