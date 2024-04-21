from domain.user.interfaces import IUserPasswordService


class UserPasswordService(IUserPasswordService):

    async def hash_password(self, password: str):
        hashed_password = hash(password)
        return hashed_password 
    
    async def check_password(
        self, 
        plain_password: str, 
        hashed_password: str,
    ):
        return self.hash_password(plain_password) == hashed_password
