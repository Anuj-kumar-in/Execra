import base64
from cryptography.fernet import Fernet
from core.config import settings

def _get_fernet() -> Fernet:
    """Initialize and return a Fernet instance using the configured ENCRYPTION_KEY."""
    if not settings.ENCRYPTION_KEY:
        raise ValueError("ENCRYPTION_KEY is not set in configuration")
    
    # Check if the key is a hex string (length 64) and convert it,
    # otherwise assume it might be a valid Fernet key.
    key = settings.ENCRYPTION_KEY
    if len(key) == 64:
        try:
            key_bytes = bytes.fromhex(key)
            key = base64.urlsafe_b64encode(key_bytes).decode('utf-8')
        except ValueError:
            pass
            
    return Fernet(key)

def encrypt(data: str) -> str:
    """Encrypt a string and return base64-encoded encrypted string."""
    if data is None:
        return data
        
    f = _get_fernet()
    encrypted_bytes = f.encrypt(data.encode("utf-8"))
    return base64.urlsafe_b64encode(encrypted_bytes).decode("utf-8")

def decrypt(data: str) -> str:
    """Decode a base64-encoded string and decrypt it to plaintext."""
    if data is None:
        return data
        
    f = _get_fernet()
    encrypted_bytes = base64.urlsafe_b64decode(data.encode("utf-8"))
    decrypted_bytes = f.decrypt(encrypted_bytes)
    return decrypted_bytes.decode("utf-8")
