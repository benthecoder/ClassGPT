from collections import defaultdict

import boto3
import botocore


class S3:
    """
    Class for interacting with S3

    Args:
        bucket_name (str): Name of the S3 bucket

    Attributes:
        bucket_name (str): Name of the S3 bucket
        s3 (boto3.resource): S3 resource
        bucket (boto3.Bucket): S3 bucket

    Methods:
        list_folders: List all folders in the S3 bucket
        list_files: List all files in the S3 bucket
        folder_exists: Check if a folder exists in the S3 bucket
        file_exists: Check if a file exists in the S3 bucket
        create_folder: Create a folder in the S3 bucket
        upload_files: Upload a file to the S3 bucket
        remove_folder: Remove a folder from the S3 bucket
        remove_file: Remove a file from the S3 bucket
    """

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(bucket_name)

    def list_folders(self):
        folders = set()
        for obj in self.bucket.objects.filter():
            folders.add(obj.key.split("/")[0])

        return folders

    def list_files(self):
        classes = defaultdict(list)

        # loop through only the parent directory
        for obj in self.bucket.objects.filter():
            cname, fname = obj.key.split("/")
            if not fname.endswith(".json"):
                classes[cname].append(fname)

        return classes

    def folder_exists(self, folder_name):
        for _ in self.bucket.objects.filter(Prefix=f"{folder_name}/"):
            return True
        return False

    def file_exists(self, folder_name, file_name):
        try:
            self.s3.Object(self.bucket_name, f"{folder_name}/{file_name}").load()
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def create_folder(self, folder_name):
        if not self.folder_exists(folder_name):
            self.bucket.put_object(Key=f"{folder_name}/")

    def upload_files(self, file_obj, file_path):
        self.bucket.upload_fileobj(file_obj, file_path)

    def remove_folder(self, folder_name):
        if self.folder_exists(folder_name):
            for key in self.bucket.objects.filter(Prefix=f"{folder_name}/"):
                key.delete()

    def remove_file(self, folder_name, file_name):
        if self.folder_exists(folder_name):
            self.bucket.objects.filter(Prefix=f"{folder_name}/{file_name}").delete(
                Delete={"Objects": [{"Key": f"{folder_name}/{file_name}"}]}
            )

    def download_file(self, from_file_path, to_file_path):
        self.bucket.download_file(from_file_path, to_file_path)
