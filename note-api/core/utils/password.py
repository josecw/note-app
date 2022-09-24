from passlib.hash import pbkdf2_sha256


def hash(pwd: str) -> str:
    return pbkdf2_sha256.hash(pwd)


def verify(target: str, input: str) -> bool:
    return pbkdf2_sha256.verify(target, input)
