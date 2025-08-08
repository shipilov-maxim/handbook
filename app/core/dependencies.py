from fastapi import Security
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings
from app.core.exceptions import NoAPIKey, WrongAPIKey

api_key_header = APIKeyHeader(name="API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise NoAPIKey
    if api_key != settings.api_key:
        raise WrongAPIKey
