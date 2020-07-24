from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View

# from bus.models import Bus, CompanyAlias
# from trips.models import Trips, BusPark


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        # partners = CompanyAlias.objects.all().count()
        # buses = Bus.objects.all().count()
        # trips = Trips.objects.all().count()
        # parks = BusPark.objects.all()
        # booked_trips = Trips.objects.filter(active=False).count()
        # user_bookings = request.user.booking_set.all().first()
        # user_bookings_count = request.user.booking_set.all().count()
        # context = {
        #     'buses': buses,
        #     'alias': partners,
        #     'trips': trips,
        #     'parks': parks,
        #     'booked_trips': booked_trips,
        #     'user_bookings': user_bookings,
        #     'user_bookings_count': user_bookings_count,
        # }
        return render(request, 'index.html', context={})


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
