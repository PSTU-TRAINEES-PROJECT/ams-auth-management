from repository.user_repository import UserRepository
from schemas.users import UserCreate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: UserCreate):
        user.validate_passwords()
        
        # Check if user already exists
        existing_user = self.repository.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Simulate saving user to the database
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password  # In real life, hash the password before saving
        }
        user_name = {
            "first_name": user.first_name,
            }

        return self.repository.save_user(user_name)
