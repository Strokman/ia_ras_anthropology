from anthropos.models.file import File
from os import path
from dataclasses import dataclass
from werkzeug.exceptions import NotFound, BadRequest


@dataclass
class FileDTO:
    filename: str
    file: File = None
    path: str = None
    extension: str = None
    return_filename: str = None
    as_attachment: bool = False


def get_file_from_db(repo, params: FileDTO):
    if not params.filename:
        raise BadRequest('Filename not provided')
    file: File = File.get_one_by_attr('filename', params.filename)
    if not file:
        raise NotFound('Неверное имя файла')
    if path.isfile(file.path) and file.extension == 'pdf':
        return FileDTO(filename=file.filename, file=file, path=file.path, return_filename=f'{file.individ.index}.{file.extension}', extension=file.extension, as_attachment=False)
    elif file.extension != 'pdf':
        return FileDTO(filename=file.filename, file=file, path=file.path, return_filename=f'{file.individ.index}.{file.extension}', extension=file.extension, as_attachment=True)
