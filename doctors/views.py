from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from accounts.models import User
from notifications.models import Notification
# from transactions.models import Transaction
from transactions.models import Transaction
from .models import Speciality, SpecialityCategory
import random


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
        context['key'] = "pk_live_62ad848d9d919a21a100dd6fef0bf6c457a70683"
        return context

    def post(self, request, *args, **kwargs):
        paid_user_str = self.request.POST.get('paid_user')
        paid_ref_id = self.request.POST.get('reference_id')
        status = self.request.POST.get('status')
        paid_user = User.objects.get(username=paid_user_str)
        speciality_name = self.request.POST.get('speciality_name')
        # Add notification...
        notification = Notification(
            from_admin="Transaction Notification",
            to_user=paid_user,
            notification_type=1,
            speciality=speciality_name,
            message=f"Transaction for {speciality_name} was successful Reference ID: {paid_ref_id} Click on the chat "
            f"icon below to chat with our agent and paste you ReferenceID at the chat box to for payment confirmation "
            f"and to start consultation"
        )
        notification.save()
        # Add notification for staffs...
        if notification:
            superusers = User.objects.filter(is_superuser=True)
            for u in superusers:
                su_notification = Notification(
                    to_user=u,
                    notification_type=1,
                    speciality=speciality_name,
                    message=f"{paid_user} just made a payment for {speciality_name} with ReferenceID: {paid_ref_id}"
                )
                su_notification.save()
        # Add Transaction
        transaction = Transaction(
            transaction_name=speciality_name,
            transaction_by=paid_user,
            ref_id=paid_ref_id,
            status=status
        )
        transaction.save()
        messages.success(request, f"Payment for {paid_user} was successful your Reference code is {paid_ref_id}")
        return JsonResponse({'message': 'Payment successful'}, status=201)


class SpecialityListView(generic.ListView):
    model = Speciality
    context_object_name = 'specialties'
    paginate_by = 8
    template_name = "doctors/doctor_list.html"


class PromoNotification(LoginRequiredMixin, View):
    def post(self, request, slug, speciality_pk, *args, **kwargs):
        current_user = request.user
        speciality_name = get_object_or_404(Speciality, speciality_category__slug=slug, pk=speciality_pk)
        promo_code = f"VBCLNC-PROMO-{random.randrange(00000, 99999)}"
        superusers = User.objects.filter(is_superuser=True)
        notification = Notification(
            from_admin="Promo Transaction Notification",
            to_user=current_user,
            notification_type=1,
            speciality=speciality_name,
            message=f"You just requested for {speciality_name}. Your "
            f"PromoID: {promo_code} \n Copy this Promo code and click on the chat button "
            f"below to speak with one of our doctor \n Note: This promo stops on Dec-15-2021."
        )
        notification.save()
        for u in superusers:
            su_notification = Notification(
                to_user=u,
                notification_type=1,
                speciality=speciality_name,
                message=f"{current_user} just requested for {speciality_name} \n with "
                f"PromoID: {promo_code} "
                f"Note: This promo stops on Dec-15-2021."
            )
            su_notification.save()
        # Add Transaction...
        transaction = Transaction(
            transaction_name=speciality_name,
            transaction_by=current_user,
            ref_id=promo_code,
            status="On Promo"
        )
        transaction.save()
        messages.success(request, f"Your service request for {speciality_name} is successful & your promo code is {promo_code}")
        return redirect('dashboard')
