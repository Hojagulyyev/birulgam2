from domain.user_session.entities import UserSession


class UserSessionMap:

    @classmethod
    def serialize_one(cls, user_session: UserSession):
        return {
            'user_id': user_session.user_id,
            'company_id': (
                user_session.company_id
                if user_session.company_exists()
                else 0
            ),
        }
