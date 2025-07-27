import zipfile

def zip_files(file_list):
    zip_path = "backup.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_list:
            zipf.write(file)
    return zip_path