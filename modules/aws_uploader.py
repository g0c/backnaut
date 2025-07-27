import boto3

session = boto3.Session(profile_name='myprofile')

def upload_to_s3(file_path, bucket, profile_name='myprofile', region='eu-central-1'):
    # Extract just the filename (or customize the S3 object path)
    s3 = session.client('s3')
    #s3 = boto3.client('s3', region_name=region, aws_access_key_id, aws_secret_access_key)
    s3.upload_file(file_path, bucket, f"backups/{file_path}")

