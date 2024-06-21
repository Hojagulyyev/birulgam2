import json

from domain.user_session.interfaces import IUserSessionRepository
from domain.user_session.entities import UserSession

from infrastructure import env
from infrastructure.redis import cache


class UserSessionRedisRepository(IUserSessionRepository):

    async def get_by_access_token(self, access_token: str) -> UserSession | None:
        user_session_in_str = cache.get(f"access_tokens{access_token}")
        if not user_session_in_str:
            return None
        
        user_session_in_dict = json.loads(str(user_session_in_str))
        user_session = UserSession(
            _user_id=user_session_in_dict["user_id"],
            _company_id=user_session_in_dict["company_id"],
            _access_token=access_token,
        )
        return user_session
        
    async def set_by_access_token(self, access_token: str, user_session: UserSession) -> UserSession:
        user_session_in_dict = {
            "user_id": user_session.user_id,
            "company_id": (
                user_session.company_id
                if user_session.company_exists()
                else 0
            ),
            "access_token": user_session.access_token,
        }
        user_session_in_str = json.dumps(user_session_in_dict)
        cache.set(
            f"access_tokens{access_token}",
            user_session_in_str,
            ex=env.ACCESS_TOKEN_TTL,
        )
        return user_session
    
    async def delete_by_access_token(self, access_token: str) -> None:
        cache.delete(f"access_tokens{access_token}")
    
    async def make_empty(self) -> UserSession:
        return UserSession(
            _user_id=0,
            _company_id=0,
            _access_token="",
        )
