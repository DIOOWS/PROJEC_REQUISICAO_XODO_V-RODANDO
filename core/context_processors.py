from .models import Order

def global_settings(request):
    if request.user.is_authenticated and request.user.is_staff:
        pending_orders = Order.objects.filter(is_read=False).count()
    else:
        pending_orders = 0

    return {
        "pending_orders": pending_orders
    }
