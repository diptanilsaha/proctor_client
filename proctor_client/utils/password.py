import bcrypt

def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        password=password.encode(),
        salt=salt
    ).decode()

def check_password_hash(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=password_hash.encode()
    )
