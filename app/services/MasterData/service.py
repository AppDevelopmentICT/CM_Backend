import uuid
import requests

from . import schema
from fastapi.responses import JSONResponse
from utils.utils import decode_jwt, encode_jwt
from utils.database import create_connection
from utils.environment import POCKETBASE
from services.AuditLog.services import add_log

def add_customer(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customer(customer_id, customer_name, customer_fullname, customer_field, employee)
            VALUES(%s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), request.customer_name, request.customer_fullname, request.customer_field, request.employee))
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="POST", action_detail="Added a new customer entry to master data", entity_name="Customer")
        return JSONResponse({"message": "Success adding customer master data"}, status_code=201)
    except Exception as err:
        return JSONResponse({"message": "Error while adding customer master data", "error": str(err)}, status_code=500)
    
def get_customer_list():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM customer
            """
        )
        list_raw_data = cursor.fetchall()
        data = []
        for customer in list_raw_data:
            data.append({
                'customer_id': customer[0],
                'customer_name': customer[1],
                'customer_fullname': customer[2],
                'customer_field': customer[3],
                'employee': customer[4]
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch customer master data", "error": str(err)}, status_code=500)

def get_customer_by_id(id: str):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM customer WHERE customer_id=%s
            """, (id,)
        )
        customer = cursor.fetchone()
        data = {
                'customer_id': customer[0],
                'customer_name': customer[1],
                'customer_fullname': customer[2],
                'customer_field': customer[3],
                'employee': customer[4]
            }
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while finding customer master data", "error": str(err)}, status_code=500)

def delete_customer(id: str, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM customer WHERE customer_id=%s
            """, (id,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a Customer from master data", entity_name="Customer")
        return JSONResponse({"message": "Successful removing the data"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while delete customer master data", "error": str(err)}, status_code=500)

def update_customer(request, id, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE customer
            SET customer_name=%s, customer_fullname=%s, customer_field=%s, employee=%s
            WHERE customer_id=%s
            """, (request.customer_name, request.customer_fullname, request.customer_field, request.employee, id)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="UPDATE", action_detail="Edited a customer from master data", entity_name="Customer")
        return JSONResponse({"message": "Successful editting the data"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while edit customer master data", "error": str(err)}, status_code=500)

def get_user_list():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM users
            WHERE user_roles = 'Sales'
            """
        )
        users = cursor.fetchall()
        data = []
        for user in users:
            data.append({
                'id': user[0],
                'username': user[1] 
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch customer master data", "error": str(err)}, status_code=500)

def get_all_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * 
            FROM users
            """
        )
        users = cursor.fetchall()
        data = []
        for user in users:
            response = requests.get(f"{POCKETBASE}/api/collections/users/records/{user[0]}")
            temp_pb = response.json()
            data.append({
                'id': user[0],
                'username': user[1],
                'user_roles': user[4],
                'email': user[3],
                'isapprover': user[5],
                'isLogin': temp_pb.get('loginAccount')
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch customer master data", "error": str(err)}, status_code=500)


def get_user_by_id(id: str):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM users WHERE id=%s
            """, (id,)
        )
        user = cursor.fetchone()
        data = {
                'user_id': user[0],
                'username': user[1],
                'password': user[2],
                'email': user[3],
                'user_roles': user[4],
                'isapprover': user[5],
            }
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while finding user master data", "error": str(err)}, status_code=500)

def get_user_by_email(email: str):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM users WHERE email=%s
            """, (email,)
        )
        user = cursor.fetchone()
        payload = {
            'id': user[0],
            'roles': user[4]
        }
        data = {
            'user_id': user[0],
            'user_roles': user[4],
            'user_token': encode_jwt(payload)
        }
        add_log(user[0], action_type="LOGIN", action_detail="Logged into website", entity_name="User")
        conn.close()
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while finding user master data", "error": str(err)}, status_code=500)

def update_user(id, request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE users
            SET username=%s, isApprover=%s, email=%s
            WHERE id=%s
            """, (request.username, request.isApprover, request.email, id)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="UPDATE", action_detail="Made changes to a user detail", entity_name="User")
        return JSONResponse({"message": "Success updating users"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while updating data",  "error": err}, status_code=500)

def get_cm_by():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM master_cm_by
            """
        )
        cm_list = cursor.fetchall()
        data = []
        for cm in cm_list:
            data.append({
                'name': cm[0]
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch Corrective Maintenance master data", "error": str(err)}, status_code=500)

def add_cm_by(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM master_cm_by WHERE name=%s", (request.name,))
        data = cursor.fetchall()
        if not(len(data)==0):
            return JSONResponse({"message": f"Data {request.name} already exist"})
        try:
            cursor.execute(
                """
                INSERT INTO master_cm_by(name)
                VALUES(%s)
                """, (request.name,)
            )
            conn.commit()
            conn.close()
            user_id = decode_jwt(user_token)
            add_log(user_id, action_type="POST", action_detail="Added a new CM entry to master data", entity_name="Corrective Maintenance")
            return JSONResponse({"message": "Success adding data"}, status_code=200)
        except Exception as err:
            return JSONResponse({"message": "Error while adding Corrective Maintenance master data", "error": str(err)}, status_code=500)
    
    except Exception as err:
        return JSONResponse({"message": "Error while finding identic data", "error": str(err)}, status_code=500)

def delete_cm_by(name, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM master_cm_by
            WHERE name=%s
            """, (name,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a CM from master data", entity_name="Corrective Maintenance")
        return JSONResponse({"message": f"Success delete {name} from table"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": f"Error while delete {name} from Corrective Maintenance master data", "error": str(err)}, status_code=500)

def get_pm_by():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM master_pm_by
            """
        )
        pm_list = cursor.fetchall()
        data = []
        for pm in pm_list:
            data.append({
                'name': pm[0]
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch Preventive Maintenance master data", "error": str(err)}, status_code=500)

def add_pm_by(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM master_pm_by WHERE name=%s", (request.name,))
        data = cursor.fetchall()
        if not(len(data)==0):
            return JSONResponse({"message": f"Data {request.name} already exist"})
        try:
            cursor.execute(
                """
                INSERT INTO master_pm_by(name)
                VALUES(%s)
                """, (request.name,)
            )
            conn.commit()
            conn.close()
            user_id = decode_jwt(user_token)
            add_log(user_id, action_type="POST", action_detail="Added a new PM entry to master data", entity_name="Preventive Maintenance")
            return JSONResponse({"message": "Success adding data"}, status_code=200)
        except Exception as err:
            return JSONResponse({"message": "Error while adding Preventive Maintenance master data", "error": str(err)}, status_code=500)
    except Exception as err:
        return JSONResponse({"message": "Error while finding identic data", "error": str(err)}, status_code=500)

def delete_pm_by(name, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM master_pm_by
            WHERE name=%s
            """, (name,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a PM from master data", entity_name="Preventive Maintenance")
        return JSONResponse({"message": f"Success delete {name} from table"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": f"Error while delete {name} from Preventive Maintenance master data", "error": str(err)}, status_code=500)

def get_periode():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM master_periode
            """
        )
        periode_list = cursor.fetchall()
        data = []
        for periode in periode_list:
            data.append({
                'periode': periode[0]
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch Time Periode master data", "error": str(err)}, status_code=500)

def add_periode(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM master_periode WHERE periodic=%s", (request.periodic,))
        data = cursor.fetchall()
        if not(len(data)==0):
            return JSONResponse({"message": f"Data {request.periodic} already exist"})
        try:
            cursor.execute(
                """
                INSERT INTO master_periode(periodic)
                VALUES(%s)
                """, (request.periodic,)
            )
            conn.commit()
            conn.close()
            user_id = decode_jwt(user_token)
            add_log(user_id, action_type="POST", action_detail="Added a new periode entry to master data", entity_name="Periode")
            return JSONResponse({"message": "Success adding data"}, status_code=200)
        except Exception as err:
            return JSONResponse({"message": "Error while adding Time Periode master data", "error": str(err)}, status_code=500)
    except Exception as err:
        return JSONResponse({"message": "Error while finding identic data", "error": str(err)}, status_code=500)

def delete_periode(periode, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM master_periode
            WHERE periodic=%s
            """, (periode,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a period from master data", entity_name="Periode")
        return JSONResponse({"message": f"Success delete {periode} from table"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": f"Error while delete {periode} from Time Periode master data", "error": str(err)}, status_code=500)

def get_category():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM master_product_category
            """
        )
        category_list = cursor.fetchall()
        data = []
        for category in category_list:
            data.append({
                'category': category[0]
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch Product Category master data", "error": str(err)}, status_code=500)

def add_category(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM master_product_category WHERE category=%s", (request.category,))
        data = cursor.fetchall()
        if not(len(data)==0):
            return JSONResponse({"message": f"Data {request.category} already exist"})
        try:
            cursor.execute(
                """
                INSERT INTO master_product_category(category)
                VALUES(%s)
                """, (request.category,)
            )
            conn.commit()
            conn.close()
            user_id = decode_jwt(user_token)
            add_log(user_id, action_type="POST", action_detail="Added a new product category entry to master data", entity_name="Category")
            return JSONResponse({"message": "Success adding data"}, status_code=200)
        except Exception as err:
            return JSONResponse({"message": "Error while adding Product Category master data", "error": str(err)}, status_code=500)
    except Exception as err:
        return JSONResponse({"message": "Error while finding identic data", "error": str(err)}, status_code=500)

def delete_category(category, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM master_product_category
            WHERE category=%s
            """, (category,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a product category from master data", entity_name="Category")
        return JSONResponse({"message": f"Success delete {category} from table"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": f"Error while delete {category} from Product Category master data", "error": str(err)}, status_code=500) 

def get_implementation():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM master_implementation
            """
        )
        implementation_list = cursor.fetchall()
        data = []
        for implementation in implementation_list:
            data.append({
                'implementation_type': implementation[0]
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch Product implementation master data", "error": str(err)}, status_code=500)

def add_implementation(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM master_implementation WHERE implementation_type=%s", (request.implementation_by,))
        data = cursor.fetchall()
        if not(len(data)==0):
            return JSONResponse({"message": f"Data {request.implementation_by} already exist"})
        try:
            cursor.execute(
                """
                INSERT INTO master_implementation(implementation_type)
                VALUES(%s)
                """, (request.implementation_by,)
            )
            conn.commit()
            conn.close()
            user_id = decode_jwt(user_token)
            add_log(user_id, action_type="POST", action_detail="Added a new product implementation entry to master data", entity_name="Implementation")
            return JSONResponse({"message": "Success adding data"}, status_code=200)
        except Exception as err:
            return JSONResponse({"message": "Error while adding Product Implementation master data", "error": str(err)}, status_code=500)
    except Exception as err:
        return JSONResponse({"message": "Error while finding identic data", "error": str(err)}, status_code=500)

def delete_implementation(implementation, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM master_implementation
            WHERE implementation_type=%s
            """, (implementation,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a product implementation from master data", entity_name="Implementation")
        return JSONResponse({"message": f"Success delete {implementation} from table"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": f"Error while delete {implementation} from Product implementation master data", "error": str(err)}, status_code=500) 

def get_principal_list():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM principal
            """
        )
        principal_list = cursor.fetchall()
        data = []
        for principal in principal_list:
            data.append({
                'principal_id': principal[0],
                'principal_name': principal[1],
            })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch principal master data", "error": str(err)}, status_code=500)

def get_principal_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM principal WHERE principal_id=%s
            """, (id,)
        )
        principal = cursor.fetchone()
        data = {
                'principal_id': principal[0],
                'principal_name': principal[1],
            }
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch principal master data", "error": str(err)}, status_code=500)

def add_principal(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM principal WHERE principal_name=%s", (request.principal_name,))
        data = cursor.fetchall()
        if not(len(data)==0):
            return JSONResponse({"message": f"Data {request.principal_name} already exist"})
        try:
            cursor.execute(
                """
                INSERT INTO principal(principal_id, principal_name)
                VALUES(%s, %s)
                """, (str(uuid.uuid4()), request.principal_name)
            )
            conn.commit()
            conn.close()
            user_id = decode_jwt(user_token)
            add_log(user_id, action_type="POST", action_detail="Added a new brand entry to master data", entity_name="Principal")
            return JSONResponse({"message": "Success adding data"}, status_code=200)
        except Exception as err:
            return JSONResponse({"message": "Error while adding new principal data", "error": str(err)}, status_code=500)
    except Exception as err:
        return JSONResponse({"message": "Error while finding identic data", "error": str(err)}, status_code=500)

def delete_principal(id, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM principal
            WHERE principal_id=%s
            """, (id,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a brand from master data", entity_name="Principal")
        return JSONResponse({"message": "Data deleted"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while deleted data", "error": str(err)}, status_code=500)
    
def delete_user(id, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM users
            WHERE id=%s
            """, (id,)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="DELETE", action_detail="Deleted a user from master data", entity_name="User")
        return JSONResponse({"message": "User Deleted"}, status_code=200) 
    except Exception as err:
        return JSONResponse({"message": "Error while deleted data", "error": str(err)}, status_code=500) 