import secrets
import hashlib
import os

def gerar_chave_privada():
    size = int(os.getenv("PRIVATE_KEY_SIZE"))
    return secrets.token_hex(size)

def gerar_chave_publica():
    size = int(os.getenv("PUBLIC_KEY_SIZE"))
    return secrets.token_hex(size)

def hash_chave_privada(chave_privada):
    return hashlib.sha256(chave_privada.encode()).hexdigest()
