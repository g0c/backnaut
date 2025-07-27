import boto3

session = boto3.Session(profile_name='myprofile')
s3 = session.client('s3')

def upload_to_s3(file_path, bucket, access_key, secret_key, region):
    s3 = boto3.client('s3', region_name=region,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    s3.upload_file(file_path, bucket, f"backups/{file_path}")