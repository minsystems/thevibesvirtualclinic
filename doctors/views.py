from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Speciality, SpecialityCategory


class SpecialityCategoryList(generic.ListView):
    model = SpecialityCategory
    context_object_name = "speciality_categories"
    template_name = "doctors/specialty_category_list.html"
    

class SpecialityCategoryDetail(generic.DetailView):
    model = SpecialityCategory
    context_object_name = "speciality_category"
    template_name = "doctors/specialty_category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SpecialityCategoryDetail, self).get_context_data(**kwargs)
        context["specialities"] = Speciality.objects.filter(speciality_category=self.get_object())
        return context


class SpecialityListView(generic.ListView):
    model = Speciality
    context_object_name = 'specialties'
    paginate_by = 8
    template_name = "doctors/doctor_list.html"
