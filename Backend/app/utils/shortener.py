import random
import string

def generate_short_id(length: int = 6) -> str:
    """Gera um short_id aleatório de letras e números"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))