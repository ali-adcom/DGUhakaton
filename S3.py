from botocore.session import get_session

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
    
    def get_client(self):
        with self.session.create_client("s3", **self.config) as client:
            yield client
    
    def upload_file(
            self,
            file_path: str,
    ):
        object_name = file_path.split("/")[-1]  # /users/artem/cat.jpg
        with self.get_client() as client:
            with open(file_path, "rb") as file:
                client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )