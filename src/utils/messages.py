from dataclasses import dataclass


@dataclass
class ModelMessage:
    found_all: str = 'Models founded'
    found: str = 'Model found'
    not_found: str = 'Model not found'
    created: str = 'Model Created'


@dataclass
class SecurityMessage:
    invalid_token: str = 'Invalid token'
