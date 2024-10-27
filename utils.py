from passlib.context import CryptContext




pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash(password: str):
    return pwd_context.hash(password)

#comoaring two hashes
#fn responsible for 2 hashes
#gonna take raw pass or pass attempt , its going to hash
#it for usand compare with hash in db
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)