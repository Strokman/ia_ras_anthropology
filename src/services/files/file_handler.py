from uuid import uuid4
import os
from src.services.files.s3file_handler import S3FileHandler


class FileHandler:

    def __init__(self, file,
                 parent_obj, file_type: str, key=None) -> None:
        self.file = file
        self.parent_obj = parent_obj
        self.file_type = file_type
        self.filename = f'{uuid4()}{self.extension}'
        self.object_storage_key = self.object_storage_key_generator()

    @property
    def extension(self):
        rv = os.path.splitext(self.file.filename)[1]
        return rv

    @property
    def original_filename(self):
        original_filename = os.path.splitext(
            self.file.filename)[0].replace('/', '-').replace('.', '-')
        return original_filename + self.extension

    def object_storage_key_generator(self):
        return f'{self.parent_obj.__class__.__name__}/{self.parent_obj.id}/{self.file_type}/{self.filename}'

    def to_orm(self, model):
        uploader = S3FileHandler(self)
        instance = model.create(filename=self.filename,
                            extension=self.extension,
                            original_filename=self.original_filename,
                            object_storage_key=self.object_storage_key,
                            site_id=self.parent_obj.id
                            )
        uploader.upload_file_to_s3()
        return instance