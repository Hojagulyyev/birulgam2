from domain.user_session.entities import UserSession

from api.gql.user_session.schemas import UserSessionSchema

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
    
    @classmethod
    def to_gql_schema(cls, user_session: UserSession):
        return UserSessionSchema(
            user_id=user_session.user_id,
            company_id=(
                user_session.company_id
                if user_session.company_exists()
                else 0
            ),
            access_token=user_session.access_token,
        )
