import secrets, hashlib

class APIKeyService:
    @staticmethod
    def _generate_secret():
        secret = secrets.token_urlsafe(32)

        return f"ck_live_{secret}"
    
    @staticmethod
    def _hash_key(api_key):
        byte_data = api_key.encode('utf-8')

        hash_object = hashlib.sha256(byte_data)

        return hash_object.hexdigest()
    