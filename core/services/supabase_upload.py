import os
from core.supabase_client import supabase
from django.conf import settings
from datetime import datetime

def upload_to_supabase(file_obj, folder="products"):
    file_ext = os.path.splitext(file_obj.name)[1]
    file_name = f"{folder}/{datetime.now().timestamp()}{file_ext}"

    file_bytes = file_obj.read()

    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        file_name,
        file_bytes,
        {"content-type": file_obj.content_type}
    )

    public_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)
    return public_url
