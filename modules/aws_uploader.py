# Version: 1.0.2
# Modul za komunikaciju s AWS S3 pohranom.
# Dinamički kreira strukturu mapa po klijentima i sigurno prenosi kriptirane arhive.

import boto3
import os

# Svrha: Sigurno slanje datoteke na AWS S3 u mapu specifičnu za pojedinog klijenta
def upload_to_s3(file_path, bucket_name, region, klijent_ime="test_klijent", profile_name="default"):
    """
    Učitava datoteku na AWS S3 bucket unutar korisničke mape klijenta.
    """
    try:
        # Inicijalizacija AWS sesije na temelju parametara iz konfiguracije klijenta
        session = boto3.Session(profile_name=profile_name, region_name=region)
        s3 = session.client('s3')

        # Osiguravamo izolaciju datoteka uzimanjem samo naziva datoteke bez lokalnih putanja diska
        čisti_naziv_datoteke = os.path.basename(file_path)
        
        # Dinamičko kreiranje S3 ključa (putanje) ovisno o klijentu koji je pokrenuo backup
        object_name = f"klijenti/{klijent_ime}/backups/{čisti_naziv_datoteke}"

        # Izvršavanje prijenosa na AWS infrastrukturu
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"[SUCCESS] Datoteka uspješno poslana na S3: {object_name}")
        
    except Exception as e:
        raise Exception(f"AWS S3 Upload Greška: {str(e)}")