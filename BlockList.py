
BLOCKLIST = set()  

def add_token_to_blocklist(jti: str):
    """Ajoute un token à la blocklist"""
    BLOCKLIST.add(jti)

def is_token_revoked(jti: str) -> bool:
    """Vérifie si un token est révoqué"""
    return jti in BLOCKLIST

def remove_token_from_blocklist(jti: str):
    """Retire un token de la blocklist"""
    BLOCKLIST.discard(jti)
