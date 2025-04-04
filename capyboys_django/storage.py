from django.core.files.storage import Storage
from supabase import create_client
from django.conf import settings

# https://github.com/jschneier/django-storages/issues/1099#issuecomment-1975178634
class SupabaseStorage(Storage):
    def __init__(self, bucket_name="blog_storage", file_overwrite=True, **kwargs):
        self.bucket_name = bucket_name
        self.file_overwrite = file_overwrite

        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.storage_client = self.supabase.storage.from_(self.bucket_name)

    def _open(self, name, mode="rb"):
        # Implement the method to open a file from Supabase
        pass

    def _save(self, name, content):
        # Implement the method to save a file to Supabase
        content_file = content.file
        content_file.seek(0)  # Move the file pointer to the beginning
        content_bytes = content_file.read()

        file_options = {
            "content-type": content.content_type,
            "upsert": str(self.file_overwrite).lower(),
        }

        data = self.supabase.storage.from_(self.bucket_name).upload(
            name, content_bytes, file_options
        )
        return data.full_path  # name/path of the file

    def exists(self, name):
        # Implement the method to check if a file exists in Supabase
        pass

    def url(self, name):
        # Implement the method to return the URL for a file in Supabase
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{name}"