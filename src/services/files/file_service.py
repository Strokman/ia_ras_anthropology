from anthropos.models.file import File
from flask import current_app
from os import path
from dataclasses import dataclass
from werkzeug.exceptions import NotFound, BadRequest
import boto3

def create_s3_client():
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=current_app.config['OBJECT_STORAGE_URL']
    )

    return s3

s3 = create_s3_client()


@dataclass
class FileDTO:
    filename: str
    file: File = None
    stream: bytes = None
    path: str = None
    extension: str = None
    return_filename: str = None
    as_attachment: bool = False


def get_file_from_db(repo, params: FileDTO):
    if not params.filename:
        raise BadRequest('Filename not provided')
    file: File = File.get_one_by_attr('filename', repo, params.filename)
    if not file:
        raise NotFound('Неверное имя файла')
    if path.isfile(file.path) and file.extension == 'pdf':
        return FileDTO(filename=file.filename, file=file, path=file.path, return_filename=f'{file.individ.index}.{file.extension}', extension=file.extension, as_attachment=False)
    elif file.extension != 'pdf':
        return FileDTO(filename=file.filename, file=file, path=file.path, return_filename=f'{file.individ.index}.{file.extension}', extension=file.extension, as_attachment=True)


def upload_file_to_s3(client, params):
    client.put_object(Body=params.stream.read(), Bucket=current_app.config['BUCKET'], Key=params.filename)


def get_file_s3(client, params):
    get_object_response = client.get_object(Bucket=current_app.config['BUCKET'],
                                            Key=params.filename)
    return get_object_response['Body'].read()
