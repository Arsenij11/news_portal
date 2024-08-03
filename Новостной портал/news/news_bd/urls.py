from django.urls import path
from django.views.decorators.cache import cache_page
# Импортируем созданные нами представления
from .views import PostList, PostDetail, PostSearch,NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete, CategoryListView, subscribe, successfuldelete



urlpatterns = [path('', cache_page(60)(PostList.as_view()), name='post_list'),
            path('<int:id>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
            path('search', PostSearch.as_view(), name='post_search'),
            path('news/create', NewsCreate.as_view(), name='news_create'),
            path('news/<int:pk>/edit', NewsEdit.as_view(), name='news_edit'),
            path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
            path('news/successful_delete', successfuldelete, name='successful_delete'),
            path('articles/create', ArticleCreate.as_view(), name='article_create'),
            path('articles/<int:pk>/edit', ArticleEdit.as_view(), name='article_edit'),
            path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
            path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
            path('categories/<int:pk>/subscribe', subscribe, name='subscribe')]