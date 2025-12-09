from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect

from .models import Product, Requisition, Order, OrderItem
from .services.upload_storage import upload_image
from .admin_config import SystemConfigAdmin



# -----------------------------
#  PRODUCT ADMIN
# -----------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "requisition")
    fields = ["name", "requisition", "image_url"]
    readonly_fields = ["image_url"]
    change_form_template = "admin/upload_product_image.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = Product.objects.get(id=object_id)

        if request.method == "POST" and "file" in request.FILES:
            url = upload_image(request.FILES["file"], "products")
            obj.image_url = url
            obj.save()
            messages.success(request, "Imagem enviada ao Supabase!")
            return redirect(request.path)

        return super().change_view(request, object_id)


# -----------------------------
#  REQUISITION ADMIN
# -----------------------------
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ["name", "icon_url"]
    readonly_fields = ["icon_url"]
    change_form_template = "admin/upload_requisition_icon.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = Requisition.objects.get(id=object_id)

        if request.method == "POST" and "file" in request.FILES:
            url = upload_image(request.FILES["file"], "requisitions")
            obj.icon_url = url
            obj.save()
            messages.success(request, "Ícone enviado ao Supabase!")
            return redirect(request.path)

        return super().change_view(request, object_id)


# Registrar tudo no admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Requisition, RequisitionAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
