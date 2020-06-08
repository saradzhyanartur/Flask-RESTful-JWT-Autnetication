from usersAPI.resources.user import (
        UserRegister, User, UserLogin, AccessTokenRefresh, AccessTokenRevoke,
        RefreshTokenRevoke
    )

class Route:

    def __init__(self, resource: 'Resource', path: str, description: str = "API endpoint") -> None:
        self.resource = resource
        self.path = path
        self.description = description

    def __repr__(self) -> str:
        return f"Route: {self.path}, Description: {self.description}"

exposed = [
    Route(UserRegister, '/user/register'),
    Route(User, '/user/<int:user_id>'),

    Route(UserLogin, '/auth/login'),
    Route(AccessTokenRefresh, '/auth/access_refresh'),
    Route(AccessTokenRevoke, '/auth/access_revoke'),
    Route(RefreshTokenRevoke, '/auth/refresh_revoke')
]