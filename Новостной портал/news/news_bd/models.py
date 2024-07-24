from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache # импортируем наш кэш
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)
    def update_rating(self):
        post_rating = 0.0
        comments_rating = 0.0
        posts_comments_rating = 0.0

        posts = Post.objects.filter(author= self)
        for p in posts:
            post_rating += p.post_rating

        comments = Comment.objects.filter(user=self.user)

        for c in comments:
            comments_rating += c.comment_rating

        posts_comments = Comment.objects.filter(post__author = self)

        for pc in posts_comments:
            posts_comments_rating += pc.comment_rating

        self.user_rating = post_rating * 3 + comments_rating + posts_comments_rating
        self.save()
    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name

class Post(models.Model):
    Article = 'AR'
    News = 'NE'
    types = [(Article,'Статья'),(News,'Новость')]

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    type_post = models.CharField(max_length=2, choices=types, default=News)
    time_post = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    post_rating = models.FloatField(default=0.0)

    def like(self):
        self.post_rating= self.post_rating + 1.0
        self.save()
    def dislike(self):
        self.post_rating = self.post_rating - 1.0
        self.save()
    def preview(self):
        self.post_preview = self.text[:124] + '...'
        return self.post_preview
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его
    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete = models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating = self.comment_rating + 1.0
        self.save()
    def dislike(self):
        self.comment_rating = self.comment_rating - 1.0
        self.save()
    def __str__(self):
        return self.text

