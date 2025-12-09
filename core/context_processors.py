from .models_config import SystemConfig

def global_settings(request):
    cfg = SystemConfig.objects.first()
    return {
        "SYSTEM_LOGO": cfg.logo_url if cfg else ""
    }
