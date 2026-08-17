from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.db.database import get_db
from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.services.user import create_user, get_user_by_username, login_user

router = APIRouter(
    prefix="/api",
    tags=["Authentication"],
)
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    data = create_user(db, user)
    return data

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    access_token = login_user(db, data)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
def get_profile(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = get_user_by_username(db, username)
    return {
        "message": f"Welcome, {user.username}!"
    }