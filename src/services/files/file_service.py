from src.repository.models.file import File
from os import environ
from dataclasses import dataclass
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
import boto3
from uuid import uuid1


def create_s3_client():
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        region_name='ru-central1',
        endpoint_url=environ.get('OBJECT_STORAGE_URL')
    )

    return s3


s3_client = create_s3_client()


@dataclass
class FileDTO:
    filename: str
    file: File = None
    stream: bytes = None
    extension: str = None
    return_filename: str = None
    as_attachment: bool = False

    @classmethod
    def create(cls, file: FileStorage):
        filename: str = secure_filename(file.filename)
        if '.' not in filename:
            filename = '.' + filename
        extension: str = filename.rsplit('.', 1)[1].lower()
        filename: str = f'{uuid1()}.{extension}'
        stream = file.stream
        return FileDTO(filename,
                       File(
                           filename=filename,
                           extension=extension),
                       stream=stream,
                       extension=extension
                       )


def get_file_from_db(repo, params: FileDTO):
    if not params.filename:
        raise BadRequest('Filename not provided')
    file: File = File.get_one_by_attr('filename', repo, params.filename)
    if not file:
        raise NotFound('Неверное имя файла')
    if file.extension == 'pdf':
        return FileDTO(filename=file.filename, file=file, return_filename=f'{file.individ.index}.{file.extension}', extension=file.extension, as_attachment=False)
    elif file.extension != 'pdf':
        return FileDTO(filename=file.filename, file=file, return_filename=f'{file.individ.index}.{file.extension}', extension=file.extension, as_attachment=True)


def upload_file_to_s3(client, params: FileDTO):
    client.put_object(Body=params.stream.read(),
                      Bucket=environ.get('BUCKET'),
                      Key=params.filename)
    return True


def get_file_from_s3(client, params):
    get_object_response = client.get_object(Bucket=environ.get('BUCKET'),
                                            Key=params.filename)
    return get_object_response['Body']


def delete_file_from_s3(client, params):
    client.delete_object(Bucket=environ.get('BUCKET'),
                         Key=params.filename)
    return True
