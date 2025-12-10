def global_settings(request):
    try:
        if request.user.is_authenticated and request.user.is_staff:
            from .models import Order
            pending_orders = Order.objects.filter(is_read=False).count()
        else:
            pending_orders = 0

        return { "pending_orders": pending_orders }

    except Exception as e:
        print("ERROR IN CONTEXT PROCESSOR:", str(e))
        import traceback
        traceback.print_exc()
        return { "pending_orders": 0 }
