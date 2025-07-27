# Version: 1.0.1
# Modul za kompresiju podataka.
# Pakira sve detektirane datoteke u unificiranu ZIP arhivu spremnu za daljnju obradu.

import zipfile
import os

# Svrha: Pakiranje liste pronađenih datoteka u jednu kompaktnu ZIP datoteku
def zip_files(file_list, target_dir=None):
    """
    Kreira ZIP arhivu od prosljeđene liste datoteka na sigurnoj lokaciji.
    """
    if not file_list:
        raise ValueError("Lista datoteka za kompresiju je prazna.")

    # Ako ciljna mapa nije prosljeđena, spremamo arhivu u isti direktorij prve datoteke
    if target_dir:
        zip_path = os.path.join(target_dir, "backup.zip")
    else:
        zip_path = os.path.join(os.path.dirname(file_list[0]), "backup.zip")

    # Otvaranje ZIP toka i sekvencijalno dodavanje datoteka uz očuvanje relativne strukture
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_list:
            if os.path.exists(file):
                # arcname sprječava da se u ZIP-u kreira cijelo stablo apsolutnih putanja s diska
                zipf.write(file, arcname=os.path.basename(file))
                
    return zip_path