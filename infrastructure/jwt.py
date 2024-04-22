from datetime import timedelta, datetime

import jwt

from infrastructure import env


def generate_token_by_user_id(
    user_id: int,
):
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
        algorithm="HS256",
    )
    return token
