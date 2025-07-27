
import boto3

def upload_to_s3(file_path, bucket_name, profile_name='myprofile', region='eu-central-1'):
    """
    Uploads a file to an S3 bucket using credentials stored in ~/.aws/credentials.

    :param file_path: Local path to the file
    :param bucket_name: Target S3 bucket
    :param profile_name: AWS profile to use
    :param region: AWS region (e.g. 'eu-central-1')
    """
    # Create a session using the given profile and region
    session = boto3.Session(profile_name=profile_name, region_name=region)

    # Create an S3 client from the session
    s3 = session.client('s3')

    # Extract just the filename (or customize the S3 object path)
    object_name = f"backups/{file_path.split('/')[-1]}"

    # Perform the upload
    s3.upload_file(file_path, bucket_name, object_name)

    print(f"✅ File uploaded to S3 bucket '{bucket_name}' as '{object_name}'")
