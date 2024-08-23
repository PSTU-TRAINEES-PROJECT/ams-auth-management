# Mock database implementation
mock_db = []

class UserRepository:
    def save_user(self, user_data: dict):
        mock_db.append(user_data)
        return user_data

    def get_user_by_email(self, email: str):
        return next((user for user in mock_db if user["email"] == email), None)
