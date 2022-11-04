from passlib.hash import pbkdf2_sha256 as sha256


def hashPassword(password: str):
    return sha256.hash(password)


def verifyPassword(plain_password, hashed_password):
    return sha256.verify(plain_password, hashed_password)
