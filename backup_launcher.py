# Version: 1.0.1
# Glavna pokretačka skripta za Backnaut hibridni backup sustav.
# Upravlja procesom skeniranja, kompresije, AES enkripcije i sigurnog slanja na AWS S3.

from modules import scanner, compressor, encryptor, aws_uploader
import json
import os
import datetime

# Svrha: Učitavanje korisničkih postavki i konfiguracija za backup
config = json.load(open('config.json'))
log_path = os.path.join("logs", "backup.log")

# Svrha: Centralizirano zapisivanje operativnih događaja i grešaka u log datoteku
def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

# Inicijalizacija varijabli na None kako bi se izbjegao NameError u slučaju ranog prekida
zip_path = None
enc_path = None

# Središnji izvršni pipeline za obradu i slanje podataka
try:
    # 1. Korak: Skeniranje izvorišne mape uz primjenu filtera za ekskluziju datoteka
    files = scanner.scan_folder(config["source_folder"], config["exclude_extensions"])
    
    # 2. Korak: Kompresija prikupljenih datoteka u privremenu ZIP arhivu
    zip_path = compressor.zip_files(files)
    
    # 3. Korak: Enkripcija ZIP arhive robusnim AES algoritmom pomoću lozinke iz konfiguracije
    enc_path = encryptor.encrypt_file(zip_path, config["encryption_password"])
    
    # 4. Korak: Sigurno slanje kriptirane datoteke na klijentov AWS S3 bucket
    # Koristi se IAM ugrađena rola ili konfiguracijski regijski parametri bez eksponiranja ključeva
    aws_uploader.upload_to_s3(enc_path, config["s3_bucket"], config["aws_region"])
    
    log("Backup completed successfully.")
    print("[BACKNAUT] Backup uspješno završen i poslan na AWS S3!")
    
except Exception as e:
    # Ispis putanja u konzolu samo ako su datoteke stvarno bile kreirane do trenutka greške
    print(f"[DEBUG INFO] Status datoteka prije pada -> ZIP: {zip_path}, ENC: {enc_path}")
    
    # Zapisivanje stvarne greške u log datoteku radi ISO 27001 revizije
    log(f"Backup failed: {str(e)}")
    print(f"[ERROR] Backup je prekinut zbog greške: {str(e)}")