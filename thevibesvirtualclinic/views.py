from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View

# from bus.models import Bus, CompanyAlias
# from trips.models import Trips, BusPark
from doctors.models import Speciality
from services.models import Post
from articles.models import Article


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        speciality = Speciality.objects.all()
        post = Post.objects.all()
        daily_articles = Article.objects.all()[:4]
        return render(request, 'index.html', context={"speciality":speciality, "post":post, "daily_articles":daily_articles})


# class CompanyAliasList(LoginRequiredMixin, ListView):
#     queryset = CompanyAlias.objects.all()
#
#     def get_context_data(self, *args, **kwargs):
#         return super(CompanyAliasList, self).get_context_data(*args, **kwargs)
#
#
# class BusList(LoginRequiredMixin, ListView):
#     queryset = Bus.objects.all()
#
#     def get_context_data(self, *args, **kwargs):
#         return super(BusList, self).get_context_data(*args, **kwargs)
