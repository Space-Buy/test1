from fastapi import Depends,HTTPException
from auth.jwttoken import verify_token,verify_superuser_token
from http import HTTPStatus
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-superuser")

def get_superuser(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate SUPERUSER's credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
	return verify_superuser_token(token,credentials_exception,"super_user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
	return verify_token(token,credentials_exception)

