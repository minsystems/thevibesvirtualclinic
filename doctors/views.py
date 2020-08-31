from django.shortcuts import render
from django.views import generic

from .models import Speciality


class SpecialtyListView(generic.ListView):
    model = Speciality
    context_object_name = 'specialties'
    paginate_by = 8
    template_name = "doctors/doctor_list.html"
