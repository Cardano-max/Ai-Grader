# Imports the Google Cloud client library
from google.cloud import storage
import os
from src.utils.basic import get_file_size
from uuid import uuid4
# Instantiates a client
class StorageManager():
    def __init__(self):
        self.storage_client= storage.Client()
        self.bucket_name = "cdn.grader.risetech.ai"
        
        
    def create_bucket(self, bucket_name):
        """Creates a new bucket."""
        try:
            bucket = self.storage_client.create_bucket(bucket_name)
            return {"status" : True}
        except Exception as err:
            return {"status" : False, "message" : err.message}


    def delete_bucket(self, bucket_name):
        """Deletes a bucket. The bucket must be empty."""
        bucket = self.storage_client.get_bucket(bucket_name)
        bucket.delete()
        print('Bucket {} deleted'.format(bucket.name))

    def upload_blob(self, source_file_name, destination_blob_name, bucket_name='', public=True, delete=False):
        """Uploads a file to the bucket."""
        try:
            if bucket_name == '':
                bucket_name = self.bucket_name
            print("Source:", source_file_name)
            print("Destination:", destination_blob_name)
            bucket = self.storage_client.get_bucket(bucket_name)
            CHUNK_SIZE = 2 * 1024 * 1024
            blob = bucket.blob(destination_blob_name, chunk_size=CHUNK_SIZE)

            # set blob to public

            blob.upload_from_filename(source_file_name)

            if public:
                blob.make_public()

            if delete:
                os.remove(source_file_name)

            print('File {} uploaded to {}.'.format(
                source_file_name,
                destination_blob_name))
            return True
        except Exception as ex:
            print(str(ex))
            return False


    def download_blob(self, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            blob = bucket.blob(source_blob_name)

            blob.download_to_filename(destination_file_name)

            print('Blob {} downloaded to {}.'.format(
                source_blob_name,
                destination_file_name))
            return True
        except Exception as err:
            return {"status" : False, "message" : err}

    def delete_blob(self, blob_name):
        """Deletes a blob from the bucket."""
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            blob = bucket.blob(blob_name)

            blob.delete()

            print('Blob {} deleted.'.format(blob_name))
            return True
        except:
            return False


    def list_blobs(self, parent="", bucket_name=''):
        """Lists all the blobs in the bucket."""
        if bucket_name == '':
            bucket_name = self.bucket_name
        try:
            # Note: Client.list_blobs requires at least package version 1.17.0.
            blobs = self.storage_client.list_blobs(bucket_name, prefix=parent)
            listData = []
            for blob in blobs:
                listData.append(blob.name)
            
            return listData
        except Exception as ex:
            print("List blobs error:", ex)
            return False

    def create_folder(self, path, bucket_name):
        """ Create a new folder """
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            if path[-1] != "/":
                path += "/"
            blob = bucket.blob(path)
            if self.check_folder_exists(path, bucket_name):
                return False
                
            resp = blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
            
            return True
        except:
            return False


    def delete_folder(self, path, bucket_name):
        """ Delete a folder """
        try:
            if path[-1] != "/":
                path += "/"
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.blob(path)

            blob = bucket.blob(path)

            blob.delete()

            print('Blob {} deleted.'.format(path))
            return True
        except:
            return False

    def delete_folder_recursively(self, path, bucket_name):
        """ Delete a folder """
        try:
            if path[-1] != "/":
                path += "/"
            bucket = self.storage_client.get_bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=path)
            for blob in blobs:
                blob.delete()

            print('Blob {} deleted.'.format(path))
            return True
        except:
            return False

    def check_folder_exists(self, folderPath, bucket_name):
        """ check if path/file exists in bucket or not """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            stats = storage.Blob(bucket=bucket, name=folderPath).exists(self.storage_client)
            return stats
        except:
            return "Not working"


    def read_blob(self, blob_name, bucket_name):
        """Reads a blob from the bucket."""
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            return blob.download_as_string()
        except:
            return False

    def write_blob(self, filestr, blob_name, bucket_name):
        """Writes a blob to the bucket."""
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_string(filestr)
            return True
        except:
            return False
        

    def upload_blob_and_return_meta(self, source_file_path, destination_path, bucket_name='', public=True, delete=False, random_name=False):
        """Uploads a file to the bucket."""
        bucket_name = self.bucket_name if bucket_name == "" else bucket_name
        final = {}
        if random_name:
            uuid_name = str(uuid4()).replace("-", "")
            destination_path = destination_path + "/" + uuid_name[:6] + uuid_name[2:4] + uuid_name[8:15] + uuid_name[18:25] + uuid_name[15:18] + os.path.splitext(source_file_path)[-1]

        final = {
            'size' : get_file_size(source_file_path),
            'name' : os.path.basename(source_file_path),
            'path' : destination_path,
        }
        

        self.upload_blob(source_file_path, destination_path, bucket_name, public, delete)

        
        if public:
            final['url'] = f"https://storage.googleapis.com/{bucket_name}/{destination_path}"

        return final