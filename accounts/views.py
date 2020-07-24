from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.base import View

from accounts.models import Profile

User = get_user_model()


# Create your views here.


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        return render(request, template_name='accounts/register.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        return render(request, template_name='accounts/login.html')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            username = data['username']
            password = data['password']
            user_qs = User.objects.filter(username__iexact=username)
            if user_qs.exists():
                user = authenticate(username=username, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse({'message': 'Logged In Successfully!'}, status=200)
            return JsonResponse({'message': 'Error With User!'}, status=400)
        return JsonResponse({'message': 'Method Not Allowed!'}, status=400)


class UserProfileView(LoginRequiredMixin, DetailView):
    queryset = Profile.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        context['user_bookings'] = self.request.user.booking_set.all()
        context['currentTime'] = timezone.now()
        return context

    def render_to_response(self, context, **response_kwargs):
        if context:
            user_obj = str(self.get_object())
            if user_obj != self.request.user.username:
                return HttpResponseRedirect(reverse('404_'))
            if self.request.user.first_name and self.request.user.last_name:
                messages.success(self.request, 'Welcome to your profile, {}'.format(self.get_object().get_name()))
            else:
                messages.warning(self.request, '{}, Profile Update Is Required'.format(self.request.user.username))
        return super(UserProfileView, self).render_to_response(context, **response_kwargs)

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            return redirect(reverse('404_'))
        except Profile.MultipleObjectsReturned:
            qs = Profile.objects.filter(slug=slug)
            instance = qs.first()
        except:
            return redirect(reverse('404_'))
        return instance
