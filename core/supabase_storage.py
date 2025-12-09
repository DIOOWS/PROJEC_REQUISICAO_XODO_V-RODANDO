import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "xodo-storage"  # você vai criar no painel


def upload_image(file_obj, folder="products"):
    """
    Envia uma imagem ao Supabase Storage e retorna a URL pública.
    """

    filename = file_obj.name.replace(" ", "_")
    path = f"{folder}/{filename}"

    # Upload
    supabase.storage.from_(BUCKET).upload(
        path, file_obj, {"content-type": file_obj.content_type}
    )

    # Gera URL pública
    public_url = supabase.storage.from_(BUCKET).get_public_url(path)
    return public_url
