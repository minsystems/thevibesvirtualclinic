from django.views import generic
from .models import Article


class ArticleList(generic.CreateView, generic.ListView):
    fields = ("title", "description", "image_url", "body", "draft")
    model = Article
    context_object_name = 'articles'
    paginate_by = 3
    template_name = "articles/article_list.html"


class ArticleDetail(generic.DetailView):
    model = Article

    def get_object(self):
        view_count_obj = super(ArticleDetail, self).get_object()
        view_count_obj.view_count += 1
        view_count_obj.save()
        return view_count_obj
