from domain.user.interfaces import IUserPasswordService


class UserPasswordService(IUserPasswordService):

    def hash_password(self, password: str) -> str:
        hashed_password = password[::-1]
        return hashed_password 
    
    def check_password(
        self, 
        plain_password: str, 
        hashed_password: str,
    ) -> bool:
        hashed_plain_password = self.hash_password(plain_password)
        return hashed_plain_password == hashed_password
