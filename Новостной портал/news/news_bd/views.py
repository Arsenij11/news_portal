from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Category
from .filters import Postfilter
from .forms import Newsform, Articleform
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
# from .tasks import notify_about_new_post
from django.core.cache import cache # импортируем наш кэш
from django.utils import timezone
import pytz #  импортируем стандартный модуль для работы с часовыми поясами
from django.shortcuts import redirect
from django.utils.translation import gettext

class PostList(ListView):
    model = Post
    ordering = '-time_post'
    context_object_name = 'posts'
    template_name = 'news.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_time"] = timezone.localtime(timezone.now())
        context["timezones"] = pytz.common_timezones
        return context
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')

class PostDetail(DetailView):
    model = Post
    template_name = 'concrete_news.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["id"]}', None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["id"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_time"] = timezone.localtime(timezone.now())
        context["timezones"] = pytz.common_timezones
        return context
    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(f'/news/{self.kwargs["id"]}')

class PostSearch(ListView):
    model = Post
    ordering = '-time_post'
    context_object_name = 'posts'
    template_name = 'news_search.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = Postfilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context["current_time"] = timezone.localtime(timezone.now())
        context["timezones"] = pytz.common_timezones
        return context
        
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news/search')

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_bd.add_post')
    raise_exception = True
    model = Post
    form_class = Newsform
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'NE'
        news.save()
        # notify_about_new_post.apply_async([news.id])
        return super().form_valid(form)



class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_bd.change_post')
    model = Post
    form_class = Newsform
    template_name = 'news_create.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id':post.pk}

        if self.request.path == f'/news/news/{post.pk}/edit' and post.type_post != 'NE':
            return render(self.request, template_name='invalid_news_edit.html', context=context)

        return super(NewsEdit, self).dispatch(request, *args, **kwargs)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_bd.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('successful_delete')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}

        if self.request.path == f'/news/news/{post.pk}/delete' and post.type_post != 'NE':
            return render(self.request, template_name='invalid_news_edit.html', context=context)

        return super(NewsDelete, self).dispatch(request, *args, **kwargs)


class ArticleCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news_bd.add_post')
    model = Post
    form_class = Articleform
    template_name = 'article_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'AR'
        return super().form_valid(form)

class ArticleEdit(PermissionRequiredMixin,UpdateView):
    permission_required = ('news_bd.change_post')
    model = Post
    form_class = Articleform
    template_name = 'article_create.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}

        if self.request.path == f'/news/articles/{post.pk}/edit' and post.type_post != 'AR':
            return render(self.request, template_name='invalid_articles_edit.html', context=context)
        return super(ArticleEdit, self).dispatch(request, *args, **kwargs)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_bd.delete_post')
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('successful_delete')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}

        if self.request.path == f'/news/articles/{post.pk}/delete' and post.type_post != 'AR':
            return render(self.request, template_name='invalid_articles_edit.html', context=context)
        return super(ArticleDelete, self).dispatch(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Post
    template_name = 'subscriptions.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_post')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        context["current_time"] = timezone.localtime(timezone.now())
        context["timezones"] = pytz.common_timezones
        return context
    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(f'/news/categories/{self.kwargs["pk"]}')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id = pk)
    category.subscribers.add(user)

    message = gettext("Вы успешно подписались на рассылку новостей категории ")
    return render(request, 'subscribe.html', {'category': category, 'message':message})

def successfuldelete(request):
    return render(request, 'successful_deleting.html')
