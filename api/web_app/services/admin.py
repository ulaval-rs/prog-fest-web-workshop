from .token import TokenService
from ..constants import ADMIN_TOKEN
from ..dao import Dao


class AdminService:

    def __init__(self, dao: Dao, token_service: TokenService):
        self.dao = dao
        self.token_service = token_service

    def is_admin(self, token: str) -> bool:
        return ADMIN_TOKEN == token

    def reset_users(self) -> None:
        self.dao.reset_users()
