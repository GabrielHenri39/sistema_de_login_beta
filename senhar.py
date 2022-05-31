from hashlib import sha256

def senhar_segreda(texto) -> str:
    return sha256(texto.encode('ascii')).hexdigest()