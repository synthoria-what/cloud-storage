from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from datetime import datetime
import uuid



class S3Client():
    def __init__(self,
                 secret_key: str,
                 access_key: str,
                 bucket_name: str,
                 endpoint_url: str):
        self.config = {"aws_secret_access_key": secret_key,
                       "aws_access_key_id": access_key,
                       "endpoint_url": endpoint_url}
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, object_name: str, file_data: bytes, user_id: int):
        async with self.get_client() as client:
            try:
                await client.put_object(Bucket=self.bucket_name,
                                        Key=f"users/{user_id}/{object_name}",
                                        Body=file_data,
                                        Metadata={"user-id": str(user_id), 
                                                  "Created-at": str(datetime.today())
                                                  })
                return True
            except Exception as ex:
                print(print(ex))
                return False


    async def get_object(self, object_name: str):
        async with self.get_client() as client:
            return client.get_object(Key=object_name)
        
    async def get_objects(self, user_id: int):
        async with self.get_client() as client:
            response = await client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"users/{user_id}"
            )
            return response