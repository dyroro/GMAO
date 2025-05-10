from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-date')
        return {'notifications': notifications}
    return {}

