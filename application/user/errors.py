class UserNotFoundError(Exception):
  
  def __init__(self):
    super().__init__(f"user not found")
