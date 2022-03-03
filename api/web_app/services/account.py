from .token import TokenService
from ..dao import Dao


class UserExistsError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class AccountService:

    def __init__(self, dao: Dao, token_service: TokenService):
        self.dao = dao
        self.token_service = token_service

    def does_user_exists(self, idul: str) -> bool:
        return idul in self.dao.users

    def add_user(self, idul: str) -> None:
        if self.does_user_exists(idul):
            raise UserExistsError

        token = self.token_service.make_token(idul)
        self.dao.users[idul] = token

    def authenticate(self, idul: str) -> str:
        return self.token_service.make_token(idul)

    def is_authorized(self, token: str) -> bool:
        for value in self.dao.users.values():
            if token == value:
                return True

        return False

    def retrieve_token(self, idul: str) -> str:
        if not self.does_user_exists(idul):
            raise UserDoesNotExistError

        return self.dao.users[idul]

    def is_idul_valid(self, idul: str) -> bool:
        try:
            int(idul[5:])
        except (TypeError, ValueError):
            return False

        return idul[:5].isalpha()
