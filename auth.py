from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Configuration configurations
SECRET_KEY = 'failsafe_secret'  # In production, load this securely from an environment variable!
ALGORITHM = 'HS256'

# Initialize password hashing engine
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password: str) -> str:
    """Converts a plain text password into a secure, irreversible hash."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if an incoming password matches the saved database hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    """Generates a signed JSON Web Token (JWT) valid for 2 hours."""
    # Copy data to avoid mutating original dictionary state externally
    payload = data.copy()

    # Calculate expiration lifespan bounds
    expire = datetime.utcnow() + timedelta(hours=2)

    # Append expiration timestamp metadata claim to payload
    payload.update({'exp': expire})

    # Encode and digitally sign the session token
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt