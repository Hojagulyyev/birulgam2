import json

from domain.user_session.interfaces import IUserSessionRepository
from domain.user_session.entities import UserSession

from infrastructure import env
from infrastructure.redis import cache


class UserSessionRedisRepository(IUserSessionRepository):

    async def get_by_access_token(self, access_token: str) -> UserSession:
        user_session_in_str = cache.get(f"access_tokens{access_token}")
        user_session_in_dict = json.loads(str(user_session_in_str))
        user_session = UserSession(
            user_id=user_session_in_dict["user_id"],
            company_ids=user_session_in_dict["company_ids"],
        )
        return user_session
        
    async def set_by_access_token(self, access_token: str, user_session: UserSession):
        user_session_in_dict = {
            "user_id": user_session.user_id,
            "company_ids": user_session.company_ids,
        }
        user_session_in_str = json.dumps(user_session_in_dict)
        cache.set(
            f"access_tokens{access_token}",
            user_session_in_str,
            ex=env.ACCESS_TOKEN_TTL,
        )
        return user_session
