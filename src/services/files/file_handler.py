from uuid import uuid4
import os



class FileHandler:

    def __init__(self, file,
                 parent_obj) -> None:
        self.file = file
        self.parent_obj = parent_obj
        self.filename = f'{uuid4()}{self.extension}'

    @property
    def extension(self):
        rv = os.path.splitext(self.file.name)[1]
        return rv

    @property
    def original_filename(self):
        original_filename = os.path.splitext(
            self.file.name)[0].replace('/', '-').replace('.', '-')
        return original_filename + self.extension

    @property
    def object_storage_key(self):
        return f'{self.parent_obj._meta.db_table}/{self.parent_obj.id}/{self.model._meta.model_name}/{self.filename}'

    def to_orm(self):
        uploader = S3FileHandler(self)
        instance = self.model(filename=self.filename,
                            extension=self.extension,
                            original_name=self.original_filename,
                            object_storage_key=self.object_storage_key
                            )
        uploader.upload_file_to_s3()
        instance.save()
        attr = getattr(self.parent_obj, f'{self.model._meta.model_name}_set')
        attr.add(instance)
        return True