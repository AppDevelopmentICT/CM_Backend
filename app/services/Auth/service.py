import jwt
# import pyotp
import requests

from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from utils.database import create_connection
from utils.utils import verify_password
from utils.environment import ALGORITHM, SECRET_KEY, POCKETBASE
from services.AuditLog.services import add_log
from utils.utils import decode_jwt

def create_account(body: dict, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email from users WHERE email=%s", (body['email'],))
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute("INSERT INTO users (id, username, password, email, user_roles, isapprover) VALUES(%s, %s, %s, %s, %s, %s)",
                    (body['id'], body['username'], body['password'], body['email'], body['user_roles'], body['isApprover']))
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="POST", action_detail="Created a new account", entity_name="User")

        return JSONResponse({"message": "Account Created"}, status_code=201)
    else:
        if row[0] == body['email']:
            return JSONResponse({"message": "User with this email already registered"}, status_code=200)    

#TODO: Add Password Verif
def login(body: dict):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (body['email'],))
    user = cursor.fetchone()
    
    if user is None:
        return JSONResponse({"message": "User Not Found"}, status_code=204)
    
    exp_time = datetime.utcnow() + timedelta(days=3)
    
    access_key = jwt.encode(
        {
            "sub": user[0],
            "username": user[1],
            "email": user[3],
            "roles": user[4],
            "exp": exp_time
        },
        SECRET_KEY, algorithm=ALGORITHM
    )
    
    return JSONResponse({"access_key": access_key}, status_code=200)

def get_user(auth_token: str):
    user_id = decode_jwt(auth_token)
    print(user_id)
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT * FROM users WHERE id=%s
            """, (user_id, )
        )
        data = cursor.fetchone()
        print(data)
        return JSONResponse({
            "id": user_id,
            "username": data[1],
            "roles": data[4]
        }, status_code=200)
    except Exception as e:
        return JSONResponse({"message": "Failed getting user data", "error": e}, status_code=400)

# def get_key():
#     otp = pyotp.random_base32()
#     return otp

# TODO: Add error handling
def get_user_key(id):
    user_data = requests.get(POCKETBASE+f"/api/collections/users/records/{id}")
    return user_data.json()['secret_key']

# def verify_otp(request, secret_key):
#     totp = pyotp.TOTP(secret_key)
#     if totp.now() == str(request.input_otp):
#         return JSONResponse({"message": "Succesfull Login"}, status_code=200)
#     else:
#         return JSONResponse({"message": "OTP not verified"}, status_code=401)
