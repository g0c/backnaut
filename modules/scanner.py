import os

def scan_folder(folder, excluded_exts):
    matched = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not any(f.endswith(ext) for ext in excluded_exts):
                matched.append(os.path.join(root, f))
    return matched