from modules import scanner, compressor, encryptor, temp, aws_uploader
import json, os, datetime

config = json.load(open('config.json'))
log_path = os.path.join("logs", "backup.log")

def log(msg):
    with open(log_path, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

try:
    files = scanner.scan_folder(config["source_folder"], config["exclude_extensions"])
    zip_path = compressor.zip_files(files)
    enc_path = encryptor.encrypt_file(zip_path, config["encryption_password"])
    #aws_uploader.upload_to_s3(enc_path, config["s3_bucket"], config["aws_access_key_id"],config["aws_secret_access_key"], config["aws_region"])
    aws_uploader.upload_to_s3(enc_path, config["s3_bucket"], config["aws_region"])
    #aws_uploader.upload_to_s3(enc_path, config["s3_bucket"], config["aws_region"])
    log("Backup completed successfully.")
    
except Exception as e:
    print(zip_path, enc_path)
    log(f"Backup failed: {str(e)}")