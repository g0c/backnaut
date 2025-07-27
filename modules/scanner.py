# Version: 1.0.1
# Modul za skeniranje lokalnog datotečnog sustava.
# Rekurzivno pretražuje ciljne mape i primjenjuje sigurnosne filtere za ekstenzije.

import os

# Svrha: Rekurzivni obilazak mapa i prikupljanje datoteka koje nisu izuzete pravilima
def scan_folder(folder, excluded_exts):
    """
    Vraća listu svih datoteka unutar mape, ignorirajući datoteke s izuzetim ekstenzijama.
    """
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Izvorišna mapa za skeniranje ne postoji: {folder}")

    matched = []
    
    # Normalizacija ekstenzija u mala slova kako bismo izbjegli probleme s '.TMP' vs '.tmp'
    čiste_ekstenzije = [ext.lower().strip() for ext in excluded_exts]

    # Rekurzivno prolaženje kroz stablo mapa (os.walk)
    for root, _, files in os.walk(folder):
        for f in files:
            _, ext = os.path.splitext(f)
            # Provjera podudara li se ekstenzija datoteke s nekom od zabranjenih
            if ext.lower() not in čiste_ekstenzije:
                matched.append(os.path.join(root, f))
                
    return matched