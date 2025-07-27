from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(input_path, password):
    key = password.encode()[:32]  # Simple key derivation
    cipher = AES.new(key, AES.MODE_EAX)
    with open(input_path, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    out_path = input_path + ".enc"
    with open(out_path, 'wb') as out:
        out.write(cipher.nonce + tag + ciphertext)
    return out_path