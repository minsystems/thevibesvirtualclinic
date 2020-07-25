from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views import View
# from .forms import ArticleForm, CommentForm, CategoryForm, ReplyForm
from .models import Category, Article, Comment, Reply


class ArticleList(generic.CreateView, generic.ListView):
    fields = ("category", "title", "description", "image", "body", "draft")
    model = Article
    context_object_name = 'articles'
    paginate_by = 3
    template_name = "articles/article_list.html"

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        # latest_articles = Article.objects.all().order_by("-")
        context['latest_article'] = Article.objects.all().first()  # get(created__in=timezone.now)
        return context


class ArticleDetail(generic.DetailView):
    model = Article

    def get_object(self):
        view_count_obj = super(ArticleDetail, self).get_object()
        view_count_obj.view_count += 1
        view_count_obj.save()
        return view_count_obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article_ = self.get_queryset()  # use to generate related articles if needed
        slug = self.kwargs.get(self.slug_url_kwarg)  # use to get slug and modify slug data
        context['comments'] = Comment.objects.filter(article=self.object)
        # get the reply for a particular comment
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            print(data)
            comment_detail = data["comment_detail"]
            Comment.objects.create(article=self.get_object(), by=request.user, content=comment_detail)
            # comment.save()
            # print(comment.)
            return JsonResponse({'message': 'comment updated'}, status=200)
        return JsonResponse({'message': 'error during comment update'}, status=400)


class DashBoard(View):
    def get(self, request, *args, **kwargs):
        view = ArticleList.as_view(template_name="articles/admin_page.html")
        return view(request, *args, **kwargs)


class CommentDetail(generic.DetailView):
    model = Comment

    def get_context_data(self, **kwargs):
        context = super(CommentDetail, self).get_context_data(**kwargs)
        comment_obj = Comment.objects.get(pk=self.pk_url_kwarg)
        context['replies'] = comment_obj.reply_set.all()
        print(type(context['replies']))
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            print(data)
            reply_detail = data["reply_detail"]
            Reply.objects.create(comment=self.get_object(), replied_by=request.user, content=reply_detail)
            return JsonResponse({'message': 'your reply to {} was successful'.format(reply_detail)}, status=200)
        return JsonResponse({'message': 'error during reply'}, status=400)


class ArticleCreate(LoginRequiredMixin, generic.CreateView):
    model = Article
    fields = ("category", "title", "description", "image", "body", "draft")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleCreate, self).form_valid(form)


class ArticleUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Article
    fields = ("category", "title", "description", "image", "body", "draft")

    # Here we print out the name of the page updated
    def get_page_title(self):
        obj = self.get_object()
        return "Update {}".format(obj.name)


class ArticleDelete(LoginRequiredMixin, generic.DeleteView):
    model = Article
    success_url = reverse_lazy("article_dashboard")

    # Here we overide the delete function to only work if a user is a superuser
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(author=self.request.user)
        return self.model.objects.all()


class ArticleCategory(generic.ListView):
    model = Article
    template_name = "articles/article_category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Article.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(ArticleCategory, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CategoryCreate(generic.CreateView):
    model = Category
    template_name = 'articles/category_form.html'
    fields = ('name',)

    def form_valid(self, form):
        form.instance = self.request.user
        form.save()
        return super(CategoryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('articles:article_create')
