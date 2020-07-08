import re
import secrets

token_regex = re.compile(r'[0-9a-zA-Z_-]{16}$')


def build_token():
    result = secrets.token_urlsafe()[:16]
    return result


def match_token(text):
    result = bool(token_regex.match(text))
    return result
