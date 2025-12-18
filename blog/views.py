# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Article

class BlogHomeView(ListView):
    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'articles'
    queryset = Article.objects.filter(is_published=True)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'