from datetime import timedelta, datetime

import jwt

from infrastructure import env


class TokenService:
    algorithm = "HS256"

    @classmethod
    def generate_token_by_user_id(
        cls,
        user_id: int,
    ) -> str:
        token = jwt.encode(
            {
                'user_id': user_id,
                'exp': (
                    datetime.now() + 
                    timedelta(seconds=env.ACCESS_TOKEN_EXPIRATION_TIME_IN_SECONDS)
                ),
                'iat': datetime.now(),
            },
            env.SECRET,
            algorithm=cls.algorithm,
        )
        return token
    
    @classmethod
    def is_token_expired(cls, token: str):
        try:
            jwt.decode(
                token,
                algorithms=[cls.algorithm],
                key=env.SECRET,
                verify=True,
            )
            return False
        except jwt.exceptions.ExpiredSignatureError:
            return True
