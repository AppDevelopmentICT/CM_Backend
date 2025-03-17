import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from .database import create_connection
from fastapi.responses import JSONResponse
from utils.environment import *
from jinja2 import Environment, FileSystemLoader
from utils.utils import SECRET_KEY, ALGORITHM

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def check_is_user_sales(id: str):
    if id is None or id == '':
        return False
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT user_roles
            FROM users
            WHERE id=%s
            """, (id,)
        )
        temp_data = cursor.fetchone()
        if temp_data is None:
            return False
        
        user_roles = temp_data[0]
        if user_roles == 'Sales':
            return True
        else:
            return False
    except Exception as error:
        return JSONResponse({"message": "Failed to verify user", "error": str(error)}, status_code=500)
    finally:
        cursor.close()
        conn.close()
        
def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token["id"]
    except InvalidTokenError as e:
        print(f"Token is invalid: {e}")
    except Exception as e:
        return False
    
def encode_jwt(payload: dict):
    try:
        encoded_token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
        return encoded_token
    except InvalidTokenError as e:
        print(f"Token is invalid: {e}")
    except Exception as e:
        return False
    
def check_is_user_admin(id: str):
    if id is None or id == '':
        return False
    
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT user_roles
            FROM users
            WHERE id=%s
            """, (id,)
        )
        temp_data = cursor.fetchone()
        if temp_data is None:
            return False
        
        user_roles = temp_data[0]
        if user_roles == 'Super Admin':
            return True
        else:
            return False
    except Exception as error:
        return JSONResponse({"message": "Failed to verify user", "error": str(error)}, status_code=500)
    finally:
        cursor.close()
        conn.close()