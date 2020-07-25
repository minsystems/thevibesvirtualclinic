import hashlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from bookings.models import Booking
from doctors.models import HospitalAlias
from services.models import Consultations, Services


class ConsultationsList(LoginRequiredMixin, ListView):
    queryset = Consultations.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ConsultationsList, self).get_context_data(*args, **kwargs)
        context['currentDateTime'] = timezone.now()
        return context

    def get_queryset(self):
        return Consultations.objects.filter(active=True)


class ConsultationsDetails(LoginRequiredMixin, DetailView):
    queryset = Consultations.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ConsultationsDetails, self).get_context_data(*args, **kwargs)
        context['currentDateTime'] = timezone.now()
        return context

    def render_to_response(self, context, **response_kwargs):
        if context:
            if self.request.user.first_name and self.request.user.last_name:
                pass
            else:
                return HttpResponseRedirect(self.request.user.profile.get_absolute_url())
        return super(ConsultationsDetails, self).render_to_response(context, **response_kwargs)

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Consultations.objects.get(slug=slug)
        except Consultations.DoesNotExist:
            return redirect(reverse('404_'))
        except Consultations.MultipleObjectsReturned:
            qs = Consultations.objects.filter(slug=slug)
            instance = qs.first()
        except:
            return redirect(reverse('404_'))
        return instance


class ConsultationsSearchResultView(View):
    def get(self, request, *args, **kwargs):
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')

        if query1 and query2:
            trips = Consultations.objects.filter(Q(from_locale__icontains=query1) | Q(to_locale__icontains=query2))
        else:
            trips = Consultations.objects.all()
        context = {
            'trips': trips,
            'query1': query1,
            'query2': query2
        }
        return render(request, "services/result.html", context)


class HospitalServices(DetailView):
    model = HospitalAlias

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(HospitalServices, self).get_context_data(*args, **kwargs)
        return context


class ServiceList(LoginRequiredMixin, ListView):
    model = Services

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ServiceList, self).get_context_data(*args, **kwargs)
        return context
