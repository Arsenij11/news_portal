from django.contrib import admin
from .models import Post, Author, Category, Comment
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки
# Register your models here.

# Настройка таблиц
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','text','type_post','time_post','post_rating']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text','time_comment','comment_rating']


# Настройка перевода
class PostTranslationAdmin(TranslationAdmin):
    model = Post

class CategoryTranslationAdmin(TranslationAdmin):
    model = Category

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)