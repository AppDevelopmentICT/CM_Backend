from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from . import schema, service as AuthService
from utils import utils
from typing import Annotated

auth_router = APIRouter()

@auth_router.post("/register", tags=['Authorization'])
async def create_account(request: schema.RegisterRequest, user_token: Annotated[str, Header()]):
    body = {
        "id": request.id,
        "username": request.username,
        "password": utils.get_hashed_password(request.password),
        "email": request.email,
        "user_roles": request.user_roles,
        "isApprover": request.isApprover    
    }
    create_account_response = AuthService.create_account(body, user_token)
    return create_account_response

@auth_router.post("/login", tags=['Authorization'])
async def login(request: schema.LoginRequest):
    body = {
        "email": request.email,
        "password": utils.get_hashed_password(request.password)
    }
    login_response = AuthService.login(body)
    return login_response

@auth_router.get("/profile", tags=['Authorization'])
async def get_user(auhtorization: Annotated[str, Header(description="JWT token for authentication")]):
    get_user_response = AuthService.get_user(auhtorization)
    return get_user_response

@auth_router.get("/secret-key", tags=['Authorization'])
async def get_key(id: Annotated[str, Header(description="Only admin can request")]):
    if utils.check_is_user_admin(id):
        get_key_response = AuthService.get_key()
        return get_key_response
    else:
        return JSONResponse({"message": "Unauthorized user"}, status_code=401)

@auth_router.get("/get-user-secret", tags=['Authorization'])
async def get_user_key(id: Annotated[str, Header(description="User request id")]):
    get_key_response = AuthService.get_user_key(id)
    return get_key_response

# @auth_router.post('/verify-otp', tags=['Authorization'])
# async def verify_otp(request: schema.RequestOTP, secret_key: Annotated[str, Header(description="Secret Key")]):
#     verify_otp_response = AuthService.verify_otp(request, secret_key)
#     return verify_otp_response