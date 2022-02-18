from .token import TokenService


class AuthenticationService:

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def authenticate(self, idul: str) -> str:
        return self.token_service.make_token(idul)

    def is_authorized(self, token: str) -> bool:
        return self.token_service.is_token_valid(token)

    def is_idul_valid(self, idul: str) -> bool:
        try:
            int(idul[5:])
        except (TypeError, ValueError):
            return False

        return idul[:5].isalpha()
