def global_settings(request):
    from .models_config import SystemConfig

    try:
        config = SystemConfig.objects.first()
        system_logo = config.logo_url if config else ""
    except Exception:
        system_logo = ""

    try:
        if request.user.is_authenticated and request.user.is_staff:
            from .models import Order
            pending_orders = Order.objects.filter(is_read=False).count()
        else:
            pending_orders = 0
    except:
        pending_orders = 0

    return {
        "pending_orders": pending_orders,
        "SYSTEM_LOGO": system_logo,
    }
