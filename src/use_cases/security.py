from os import environ
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.services import UserAPI
from src.utils.messages import SecurityMessage


class SecurityUseCase:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    @classmethod
    def validate(cls, token: str = Depends(oauth2_scheme)):
        token_data = cls._validate_token(token)
        email = token_data.get('email')
        response, is_invalid = UserAPI.find_user(email)
        if is_invalid:
            raise HTTPException(401, SecurityMessage.invalid_token)

        user_data = response.get('data')
        return user_data

    @classmethod
    def _validate_token(cls, token: str) -> Optional[dict]:
        try:
            data = jwt.decode(
                token,
                environ.get('SECRET_KEY'),
                environ.get('ALGORITHM')
            )
            if not data.get('email'):
                raise HTTPException(401, SecurityMessage.invalid_token)
            return data
        except JWTError as error:
            raise HTTPException(401, error)
