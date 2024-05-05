from botocore.exceptions import ClientError
from config import Config as config
import boto3
# from file.services.file_handler import FileHandler
# from file.models import File
import threading


def create_s3_client():
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        region_name='ru-central1',
        endpoint_url=config.OBJECT_STORAGE_URL
    )
    return s3


class S3FileHandler:

    def __init__(self, file):
        self.client = create_s3_client()
        self.file = file

    def upload_file_to_s3(self):
        # try:
            # self.client.put_object(Body=self.file.file.read(),
            #                         Bucket=settings.BUCKET,
            #                         Key=self.file.object_storage_key,
            #                         )
        t = threading.Thread(target=self.upload)
        t.start()
        # except ClientError as e:
        #     self.logger.error(e)
        #     raise e
        # except AttributeError as e:
        #     self.logger.error(e)
        #     raise e
        # return True

    def get_file_from_s3(self):
        try:
            get_object_response = self.client.get_object(
                Bucket=config.BUCKET,
                Key=self.file.object_storage_key
                )   
            return get_object_response['Body']
        except ClientError as e:
            pass

    def delete_file_from_s3(self):
        try:
            self.client.delete_object(Bucket=config.BUCKET,
                                    Key=self.file.object_storage_key)
        except ClientError as e:
            pass
        return True

    def upload(self):
        self.client.put_object(Body=self.file.file.read(),
                        Bucket=config.BUCKET,
                        Key=self.file.object_storage_key,
                        )
