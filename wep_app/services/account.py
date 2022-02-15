from .token import TokenService


class AccountService:

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def is_idul_valid(self, idul: str) -> bool:
        try:
            int(idul[5:])
        except (TypeError, ValueError):
            return False

        return idul[:5].isalpha()

    def make_new_account(self, idul: str):
        # pseudo token creation
        return self.token_service.make_token(idul)

    def retrieve_token(self, idul: str):
        return self.token_service.make_token(idul)

    def auth(self, token: str) -> bool:
        return self.token_service.is_token_valid(token)
