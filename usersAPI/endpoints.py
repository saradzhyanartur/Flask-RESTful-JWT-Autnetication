from usersAPI.resources.user import (
        UserRegister, User, UserLogin, TokenRefresh, UserLogout
    )

class Route:

    def __init__(self, resource: 'Resource', path: str, description: str = "API endpoint") -> None:
        self.resource = resource
        self.path = path
        self.description = description

    def __repr__(self) -> str:
        return f"Route: {self.path}, Description: {self.description}"

exposed = [
    Route(UserRegister, '/register'),
    Route(User, '/user/<int:user_id>'),
    Route(UserLogin, '/login'),
    Route(TokenRefresh, '/refresh'),
    Route(UserLogout, '/logout'),
]