import hashlib


class TokenService:

    def __init__(self, prefix: str):
        self.prefix = prefix

    def make_token(self, idul: str) -> str:
        idul_hash = hashlib.md5(idul.encode()).hexdigest()

        return f'{self.prefix}{idul_hash}'

    def is_token_valid(self, token: str) -> bool:
        return self.prefix in token
