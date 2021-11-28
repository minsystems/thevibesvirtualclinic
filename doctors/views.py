from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from accounts.models import User
from notifications.models import Notification
# from transactions.models import Transaction
from transactions.models import Transaction
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
        context['key'] = "pk_live_62ad848d9d919a21a100dd6fef0bf6c457a70683"
        return context

    def post(self, *args, **kwargs):
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
        return JsonResponse({'message': 'Payment successful'}, status=201)


class SpecialityListView(generic.ListView):
    model = Speciality
    context_object_name = 'specialties'
    paginate_by = 8
    template_name = "doctors/doctor_list.html"
