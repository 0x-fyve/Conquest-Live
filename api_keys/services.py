import secrets, hashlib
from .models import APIKey
from rest_framework.exceptions import ValidationError

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
    
    @staticmethod
    def _extract_prefix(api_key):
        return api_key[:12]
    
    @staticmethod
    def create_api_key(name, project, user):
        if APIKey.objects.filter(name=name, project=project).exists():
            raise ValidationError({
                "name": [
                    "An API key with this name already exists for this project."
                ]
            })
        plaintext_key = APIKeyService._generate_secret()
        hashed_key = APIKeyService._hash_key(plaintext_key)
        prefix = APIKeyService._extract_prefix(plaintext_key)

        api_key_model = APIKey.objects.create(
            name = name,
            hashed_key = hashed_key,
            prefix = prefix,
            project=project,
            created_by = user,
            expires_at=None,
        )
        return {
        "api_key": plaintext_key,
        "api_key_model": api_key_model,
    }
        