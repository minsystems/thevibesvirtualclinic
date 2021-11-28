from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from notifications.models import Notification


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(to_user=request.user, is_seen=False).order_by('-date')
    # Notification.objects.filter(to_user=request.user.is_a_dealer, is_seen=False).update(is_seen=True)

    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/notification_list.html', context)


def notification_delete_view(request, pk):
    user = request.user
    notification = Notification.objects.filter(pk=pk, to_user=user)
    notification.update(is_seen=True)
    return redirect('notifications:list')


def notification_counts(request):
    notification_count = 0
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(to_user=request.user).exclude(is_seen=True).order_by('-date').count()
    return {
        'notification_count': notification_count,
    }