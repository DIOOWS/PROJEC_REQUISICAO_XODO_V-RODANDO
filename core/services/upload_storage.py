import os
import uuid
from supabase import create_client, Client
from django.conf import settings


def get_client() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def upload_image(file, folder: str) -> str:
    """
    Envia imagem ao Supabase e retorna URL pública.
    folder = "products" ou "requisitions" ou "system"
    """
    supabase = get_client()

    ext = file.name.split(".")[-1]
    filename = f"{folder}/{uuid.uuid4()}.{ext}"

    supabase.storage.from_("xodo-storage").upload(
        filename,
        file,
        file_options={"content-type": file.content_type},
    )

    public_url = supabase.storage.from_("xodo-storage").get_public_url(filename)

    return public_url
