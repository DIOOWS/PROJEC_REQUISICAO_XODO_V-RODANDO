from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect

from .models_config import SystemConfig
from .services.upload_storage import upload_image


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    fields = ["logo_url"]
    readonly_fields = ["logo_url"]

    change_form_template = "admin/upload_system_logo.html"

    def change_view(self, request, object_id=None, form_url="", extra_context=None):
        obj = SystemConfig.objects.first()

        if request.method == "POST" and "file" in request.FILES:
            url = upload_image(request.FILES["file"], "system")
            obj.logo_url = url
            obj.save()

            messages.success(request, "Logo atualizada com sucesso!")
            return redirect(request.path)

        return super().change_view(request, object_id, form_url, extra_context)
