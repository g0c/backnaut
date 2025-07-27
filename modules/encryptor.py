# Version: 1.0.2
# Modul za kriptografsku zaštitu podataka (ISO 27001 kontrola).
# Koristi AES-256 u EAX modu s automatskim paddingom lozinke i integritetnim tagom.

from Crypto.Cipher import AES
import os

# Svrha: Enkripcija arhive pomoću AES-256 standarda otpornog na ransomware presretanja
def encrypt_file(input_path, password):
    """
    Kriptira datoteku pomoću AES algoritma i vraća putanju do .enc datoteke.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Izvorišna datoteka za enkripciju ne postoji: {input_path}")

    # ISO 27001 Popravak: Osiguravanje da ključ ima točno 32 bajta (AES-256) bez obzira na duljinu lozinke
    # Kratke lozinke se nadopunjuju s nul-bajtovima, a duge se režu
    key = password.encode('utf-8')
    if len(key) < 32:
        key = key.ljust(32, b'\0')
    else:
        key = key[:32]

    # Kreiranje novog šifrarnika s generiranim jedinstvenim nonceom (kriptografski sol)
    cipher = AES.new(key, AES.MODE_EAX)
    
    with open(input_path, 'rb') as f:
        data = f.read()
        
    # Generiranje šifriranog teksta i autentifikacijskog taga za provjeru integriteta
    ciphertext, tag = cipher.encrypt_and_digest(data)
    out_path = input_path + ".enc"
    
    # Zapisivanje nonce-a, taga i šifriranog sadržaja (potrebno za kasniju dekripciju)
    with open(out_path, 'wb') as out:
        out.write(cipher.nonce + tag + ciphertext)
        
    return out_path