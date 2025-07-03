import uuid
import smtplib
from jinja2 import Environment, FileSystemLoader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.environment import MAIL_FROM, MAIL_SERVER, MAIL_PORT
from utils.utils import check_is_user_sales
from utils.database import create_connection
from fastapi.responses import JSONResponse
from datetime import datetime
from utils.environment import *
from services.AuditLog.services import add_log
from utils.utils import decode_jwt

# async def send_email(email_subject: str, receiver: list[str], data, template: int):
#     print(receiver)
#     env = Environment(loader=FileSystemLoader("./template/"))
#     print(env.get_template)
#     if template == 1:
#         template = env.get_template("assigned_template.html")
#     elif template == 2:
#         template = env.get_template("project_updated.html")
#     elif template == 3:
#         template = env.get_template("project_responded.html")
#     else:
#         raise ValueError("Invalid template number provided.")
#     html_content = template.render(data=data)
#     conf = ConnectionConfig(
#         MAIL_USERNAME = MAIL_USERNAME,
#         MAIL_PASSWORD = MAIL_PASSWORD,
#         MAIL_FROM = MAIL_FROM,
#         MAIL_PORT = MAIL_PORT,
#         MAIL_SERVER = MAIL_SERVER,
#         MAIL_STARTTLS = True,
#         MAIL_SSL_TLS = False,
#         USE_CREDENTIALS = True,
#         VALIDATE_CERTS = True
#     )
#     message = MessageSchema(
#         subject=email_subject,
#         recipients=receiver, #TODO: Add Helpdesk Email
#         body=html_content,
#         subtype=MessageType.html)

#     fm = FastMail(conf)
#     await fm.send_message(message)

async def send_email(email_subject: str, receiver: list[str], data: dict, template: int):
    env = Environment(loader=FileSystemLoader("./template/"))
    
    # Choose the correct template
    if template == 1:
        template = env.get_template("assigned_template.html")
    elif template == 2:
        template = env.get_template("project_updated.html")
    elif template == 3:
        template = env.get_template("project_responded.html")
    else:
        raise ValueError("Invalid template number provided.")
    
    html_content = template.render(data=data)
    print(", ".join(receiver))
    # Set up email MIME structure
    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM  # Use environment variable
    msg['To'] = ", ".join(receiver)
    msg['Subject'] = email_subject
    msg.attach(MIMEText(html_content, "html"))
    
    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(MAIL_SERVER, port=int(MAIL_PORT)) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(MAIL_USERNAME, MAIL_PASSWORD)  # Use environment variables
            server.sendmail(msg['From'], receiver, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

async def add_project(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    project_id = str(uuid.uuid4())
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("SELECT COUNT(*) FROM project WHERE cost_sheets = %s", (request.cost_sheets,))
        cost_sheet_count = cursor.fetchone()[0]
        if cost_sheet_count > 0:
            return JSONResponse({"message": "Duplicate cost sheet found."}, status_code=400)
        
        cursor.execute("SELECT COUNT(*) FROM project WHERE contract_number = %s", (request.contract_number,))
        contract_number_count = cursor.fetchone()[0]
        if contract_number_count > 0:
            return JSONResponse({"message": "Duplicate contract number found."}, status_code=400)
        
        cursor.execute(
            """
            INSERT INTO project(project_id, customer_id, created_by, cost_sheets, project_name, 
            project_type, description, contract_number, internal_cost, selling_prices, sales_person, 
            status, created_at, on_site_engineer, approved_by)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (project_id, request.customer_id, request.created_by, request.cost_sheets, 
                  request.project_name, request.project_type, request.description, 
                  request.contract_number, request.internal_cost, request.selling_prices, 
                  request.sales_person, request.project_status, formatted_datetime, request.on_site_engineer, None)
        )    
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="POST/CREATE", action_detail="Added new project entry with project name '" + request.project_name + "'", entity_name="Project")
        return JSONResponse({"message": f"{request.project_name} has been added to project list", "project_id": project_id}, status_code=201)
    except Exception as err:
        conn.rollback()
        conn.close()
        return JSONResponse({"message": "Error while adding new data", "error": str(err)}, status_code=500)

async def import_project(request, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    project_id = str(uuid.uuid4())
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("SELECT COUNT(*) FROM project WHERE cost_sheets = %s", (request.cost_sheets,))
        cost_sheet_count = cursor.fetchone()[0]

        if cost_sheet_count > 0:
            return JSONResponse({"message": "Duplicate cost sheet found."}, status_code=400)
        
        cursor.execute("SELECT COUNT(*) FROM project WHERE contract_number = %s", (request.contract_number,))
        contract_number_count = cursor.fetchone()[0]

        if contract_number_count > 0:
            return JSONResponse({"message": "Duplicate contract number found."}, status_code=400)
        
        cursor.execute(
            """
            INSERT INTO project(project_id, customer_id, created_by, cost_sheets, project_name, 
            project_type, description, contract_number, internal_cost, selling_prices, sales_person, 
            status, created_at, on_site_engineer, approved_by)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (project_id, request.customer_id, request.created_by, request.cost_sheets, 
                  request.project_name, request.project_type, request.description, 
                  request.contract_number, request.internal_cost, request.selling_prices, 
                  request.sales_person, request.project_status, formatted_datetime, request.on_site_engineer, None)
        )    

        conn.commit()
        conn.close()
        
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="POST/CREATE", action_detail="Added new project entry with project name '" + request.project_name + "'", entity_name="Project")

        return JSONResponse({"message": f"{request.project_name} has been added to project list", "project_id": project_id}, status_code=201)
    except Exception as err:
        conn.rollback()
        conn.close()
        
        return JSONResponse({"message": "Error while adding new data", "error": str(err)}, status_code=500)

async def submit_project(id, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE project
            SET status='Pending'
            WHERE project_id=%s
            """,(id,)
        )
        cursor.execute(
            """
            SELECT users.username, users.email, customer.customer_name, project.project_name
            FROM project
            INNER JOIN users ON project.sales_person=users.id
            INNER JOIN customer ON project.customer_id=customer.customer_id
            WHERE project.project_id=%s
            """, (id,)
        )
        temp_data = cursor.fetchone()
        data = {
            "sales_person": temp_data[0],
            "project_id": id,
            "customer_name": temp_data[2], 
            "project_name": temp_data[3]
        }
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        add_log(user_id, action_type="UPDATE", action_detail="Submitted a project with project name '" + temp_data[3] + "'", entity_name="Project")
        await send_email("Assigned New Project", [temp_data[1]], data, template=1)
        return JSONResponse({"message": "Product submitted"}, status_code=200)
    except Exception as err:
        conn.rollback()
        conn.close()
        return JSONResponse({"message": "Error while adding new data", "error": str(err)}, status_code=500)

def get_project_list(user, page):
    conn = create_connection()
    cursor = conn.cursor()
    verify_sales = check_is_user_sales(user)
    data = []
    total_rows = 0

    try:
        if verify_sales:
            cursor.execute(
                """
                SELECT 
                    project_id, 
                    COALESCE(project.cost_sheets, 'N/A') AS cost_sheets, 
                    project.project_name, 
                    users.username, 
                    customer.customer_name, 
                    project.status, 
                    project.created_at  
                FROM project
                INNER JOIN users ON project.sales_person = users.id
                INNER JOIN customer ON project.customer_id = customer.customer_id
                WHERE sales_person = %s 
                  AND project.status IN ('Pending', 'Approved', 'Rejected')
                ORDER BY project.created_at DESC
                """, (user,)
            )
        else:
            cursor.execute(
                """
                SELECT 
                    project_id, 
                    COALESCE(project.cost_sheets, 'N/A') AS cost_sheets, 
                    project.project_name, 
                    users.username, 
                    customer.customer_name, 
                    project.status, 
                    project.created_at  
                FROM project
                INNER JOIN users ON project.sales_person = users.id
                INNER JOIN customer ON project.customer_id = customer.customer_id
                ORDER BY project.created_at DESC
                """
            )

        project_raw_data = cursor.fetchall()
        for project in project_raw_data:
            try:
                cursor.execute(
                    """
                    SELECT product_name
                    FROM product
                    WHERE project_id = %s
                    """, (project[0],)
                )
                product = cursor.fetchall()
                product_info = (
                    str(len(product)) + " Products" if len(product) > 1 
                    else product[0][0] if len(product) == 1 
                    else "No Products"
                )

                data.append({
                    "project_id": project[0],
                    "costsheet": project[1],
                    "project_name": project[2],
                    "sales_person": project[3],
                    "customer_name": project[4],
                    "project_status": project[5],
                    "product": product_info
                })
            except Exception as err:
                return JSONResponse(
                    {"message": "Error fetching product data", "error": str(err)},
                    status_code=500
                )

        if page == 1:
            try:
                cursor.execute(
                    """
                    SELECT COUNT(project_id) from project
                    """
                )
                total_rows = cursor.fetchone()[0]
            except Exception as err:
                return JSONResponse(
                    {"message": "Error while fetching project data", "error": str(err)},
                    status_code=500
                )
        conn.close()
        return JSONResponse({"total_rows": total_rows, "data": data}, status_code=200)

    except Exception as err:
        return JSONResponse(
            {"message": "Error while fetching project data", "error": str(err)},
            status_code=500
        )

def get_project_export_data(user_token):
    conn = create_connection()
    cursor = conn.cursor()
    data = []
    total_rows = 0
    user_id = decode_jwt(user_token)

    print(user_id)

    cursor.execute(
            """
            SELECT id, user_roles FROM users WHERE id=%s
            """, (user_id, )
        )
    user = cursor.fetchone()
    user_id = user[0]
    user_roles = user[1]

    try:
        if user_roles == 'Sales Admin' or user_roles == 'Helpdesk':
            cursor.execute(
                """
                SELECT 
                    customer.customer_fullname,
                    users.username,
                    COALESCE(project.cost_sheets, 'N/A') AS cost_sheets,
                    project.project_name,
                    project.project_type,
                    project.contract_number,
                    project.internal_cost,
                    project.selling_prices,
                    project.on_site_engineer,
                    product.product_category,
                    principal.principal_name,
                    product.product_name,
                    product.serial_number,
                    product.si_number,
                    product.quantity,
                    product.start_date,
                    product.end_date,
                    preventive_maintenance.pm_by,
                    preventive_maintenance.start_date,
                    preventive_maintenance.end_date,
                    preventive_maintenance.pm_periode,
                    preventive_maintenance.quantity,
                    corrective_maintenance.cm_by,
                    corrective_maintenance.start_date,
                    corrective_maintenance.end_date,
                    corrective_maintenance.quantity,
                    implementation_table.implementation_type,
                    implementation_table.start_date,
                    implementation_table.end_date,
                    sla_table.severity_1_response_time,
                    sla_table.severity_1_resolution_time,
                    sla_table.severity_2_response_time,
                    sla_table.severity_2_resolution_time,
                    sla_table.severity_3_response_time,
                    sla_table.severity_3_resolution_time,
                    sla_table.severity_4_response_time,
                    sla_table.severity_4_resolution_time,
                    project.description,
                    project.created_at
                FROM (
                    SELECT DISTINCT product_id
                    FROM product
                ) p
                INNER JOIN product ON p.product_id = product.product_id
                LEFT JOIN preventive_maintenance 
                    ON product.preventive_maintenance = preventive_maintenance.pm_id
                LEFT JOIN corrective_maintenance 
                    ON product.corrective_maintenance = corrective_maintenance.cm_id
                LEFT JOIN implementation_table 
                    ON product.implementation_id = implementation_table.implementation_id
                LEFT JOIN sla_table 
                    ON product.sla_id = sla_table.sla_id
                INNER JOIN principal 
                    ON product.principal_id = principal.principal_id
                LEFT JOIN project 
                    ON product.project_id = project.project_id
                INNER JOIN users 
                    ON project.sales_person = users.id
                INNER JOIN customer 
                    ON project.customer_id = customer.customer_id
                ORDER BY project.created_at DESC
                """,
            )
            
        else:
            cursor.execute(
                """
                SELECT 
                    customer.customer_fullname,
                    users.username,
                    COALESCE(project.cost_sheets, 'N/A') AS cost_sheets,
                    project.project_name,
                    project.project_type,
                    project.contract_number,
                    project.internal_cost,
                    project.selling_prices,
                    project.on_site_engineer,
                    product.product_category,
                    principal.principal_name,
                    product.product_name,
                    product.serial_number,
                    product.si_number,
                    product.quantity,
                    product.start_date,
                    product.end_date,
                    preventive_maintenance.pm_by,
                    preventive_maintenance.start_date,
                    preventive_maintenance.end_date,
                    preventive_maintenance.pm_periode,
                    preventive_maintenance.quantity,
                    corrective_maintenance.cm_by,
                    corrective_maintenance.start_date,
                    corrective_maintenance.end_date,
                    corrective_maintenance.quantity,
                    implementation_table.implementation_type,
                    implementation_table.start_date,
                    implementation_table.end_date,
                    sla_table.severity_1_response_time,
                    sla_table.severity_1_resolution_time,
                    sla_table.severity_2_response_time,
                    sla_table.severity_2_resolution_time,
                    sla_table.severity_3_response_time,
                    sla_table.severity_3_resolution_time,
                    sla_table.severity_4_response_time,
                    sla_table.severity_4_resolution_time,
                    project.description,
                    project.created_at
                FROM (
                    SELECT DISTINCT product_id
                    FROM product
                ) p
                INNER JOIN product ON p.product_id = product.product_id
                LEFT JOIN preventive_maintenance 
                    ON product.preventive_maintenance = preventive_maintenance.pm_id
                LEFT JOIN corrective_maintenance 
                    ON product.corrective_maintenance = corrective_maintenance.cm_id
                LEFT JOIN implementation_table 
                    ON product.implementation_id = implementation_table.implementation_id
                LEFT JOIN sla_table 
                    ON product.sla_id = sla_table.sla_id
                INNER JOIN principal 
                    ON product.principal_id = principal.principal_id
                LEFT JOIN project 
                    ON product.project_id = project.project_id
                INNER JOIN users 
                    ON project.sales_person = users.id
                INNER JOIN customer 
                    ON project.customer_id = customer.customer_id
                WHERE project.sales_person = %s
                ORDER BY project.created_at DESC
                """, (user_id, )
            )

        project_raw_data = cursor.fetchall()

        for project in project_raw_data:
            data.append({
                "customer_name": project[0],
                "sales_name": project[1],
                "cost_sheet": project[2],
                "project_name": project[3],

                "project_type": project[4],
                "contract_number": project[5],
                "internal_cost": project[6],
                "selling_cost": project[7],
                "managed_service": project[8],

                "product_type": project[9],
                "product_brand": project[10],
                "product_name": project[11],
                "serial_number": project[12],
                "si_number": project[13],
                "product_quantity": project[14],
                "product_start_date": str(project[15]),
                "product_end_date": str(project[16]),

                "pm_by": project[17],
                "pm_start_date": str(project[18]),
                "pm_end_date": str(project[19]),
                "maintenance_period": project[20],
                "pm_quantity": project[21],
                
                "cm_by": project[22],
                "cm_start_date": str(project[23]),
                "cm_end_date": str(project[24]),
                "cm_quantity": project[25],
                
                "i_by": project[26],
                "i_start_date": str(project[27]),
                "i_end_date": str(project[28]),
                
                # sla
                "severity1_response_time": project[29],
                "severity1_resolution_time": project[30],
                "severity2_response_time": project[31],
                "severity2_resolution_time": project[32],
                "severity3_response_time": project[33],
                "severity3_resolution_time": project[34],
                "severity4_response_time": project[35],
                "severity4_resolution_time": project[36],
                
                "project_description": project[37],
                "created_date": str(project[38]),
            })

        cursor.execute(
            """
            SELECT COUNT(project_id) from project
            """
        )
        total_rows = cursor.fetchone()[0]
            
        conn.close()
        return JSONResponse({"total_rows": total_rows, "user": user_id ,"data": data}, status_code=200)

    except Exception as err:
        return JSONResponse(
            {"message": "Error while fetching project export data", "error": str(err)},
            status_code=500
        )
    
def get_project_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT project.*, customer.customer_name, users.username, customer.customer_id
            FROM project
            INNER JOIN customer ON project.customer_id=customer.customer_id
            INNER JOIN users ON project.sales_person=users.id
            WHERE project.project_id=%s
            """,(id,)
        )
        project_temp_data = cursor.fetchone()
        
        data = {
            "project_id": id,
            "customer_id": project_temp_data[19],
            "customer_name": project_temp_data[17],
            "cost_sheets": project_temp_data[3],
            "project_name": project_temp_data[4],
            "project_type": project_temp_data[5],
            "project_status": project_temp_data[11],
            "description": project_temp_data[6],
            "contract_number": project_temp_data[7],
            "internal_cost": project_temp_data[8],
            "selling_prices": project_temp_data[9],
            "created_by": project_temp_data[2],
            "sales_person": project_temp_data[18],
            "sales_person_id": project_temp_data[10],
            "on_site_engineer": project_temp_data[13],
            "product_info": []
        }
        try:
            cursor.execute(
                """
                SELECT product.*, preventive_maintenance.*, corrective_maintenance.*, implementation_table.*, sla_table.*, principal.*
                FROM product
                LEFT JOIN preventive_maintenance ON product.preventive_maintenance=preventive_maintenance.pm_id
                LEFT JOIN corrective_maintenance ON product.corrective_maintenance=corrective_maintenance.cm_id
                LEFT JOIN implementation_table ON product.implementation_id=implementation_table.implementation_id
                LEFT JOIN sla_table ON product.sla_id=sla_table.sla_id
                INNER JOIN principal ON product.principal_id=principal.principal_id
                WHERE product.project_id=%s
                """, (id,)
            )
            product_temp_data = cursor.fetchall()
            for product in product_temp_data:
                data["product_info"].append({
                    "product_id": product[0],
                    "project_id": product[1],
                    "principal_id": product[4],
                    "principal_name": product[47],
                    "product_name": product[5],
                    "product_category": product[6],
                    "serial_number": product[7],
                    "si_number": product[8],
                    "quantity": product[9],
                    "start_date": str(product[10]),
                    "end_date": str(product[11]),
                    "preventive_maintenance": {
                        "pm_id": product[14],
                        "pm_by": product[15],
                        "start_date": str(product[16]),
                        "end_date": str(product[17]),
                        "pm_periode": product[18],
                        "is_parent": product[20],
                        "quantity": product[21],   
                    },
                    "corrective_maintenance": {
                        "cm_id": product[22],
                        "cm_by": product[23],
                        "start_date": str(product[24]),
                        "end_date": str(product[25]),
                        "is_parent": product[27],
                        "quantity": product[28],
                    },
                    "implementation": {
                        "implementation_id": product[29],
                        "implementation_type": product[30],
                        "is_parent": product[32],
                        "start_date": str(product[33]),
                        "end_date": str(product[34]),
                    },
                    "sla": {
                        "sla_id": product[35],
                        "severity_1_response_time": product[36],
                        "severity_1_resolution_time": product[37],
                        "severity_2_response_time": product[38],
                        "severity_2_resolution_time": product[39],
                        "severity_3_response_time": product[40],
                        "severity_3_resolution_time": product[41],
                        "severity_4_response_time": product[42],
                        "severity_4_resolution_time": product[43],
                        "is_parent": product[45],
                    },
                })
        except Exception as err:
            return JSONResponse({"message": "Error while fetch product data", "error": str(err)}, status_code=500)
        conn.close()
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch project data", "error": str(err)}, status_code=500)

def delete_project_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT project.*
            FROM project
            WHERE project.project_id = %s
            """,
            (id,),
        )
        project_temp_data = cursor.fetchone()

        if not project_temp_data:
            return JSONResponse({"message": "Project not found"}, status_code=404)

        # Delete product data
        cursor.execute("DELETE FROM product WHERE project_id = %s", (id,))
        
        # Delete the project
        cursor.execute("DELETE FROM project WHERE project_id = %s", (id,))

        conn.commit()
        conn.close()

        return JSONResponse(
            {
                "message": "Project and associated product data deleted successfully",
            },
            status_code=200,
        )
    except Exception as err:
        # Rollback the transaction in case of error
        conn.rollback()
        return JSONResponse(
            {"message": "Error while deleting project or product data", "error": str(err)},
            status_code=500,
        )
    finally:
        # Ensure connection is always closed
        if conn:
            conn.close()

async def update_project(request, id, user_token):
    conn = create_connection()
    cursor = conn.cursor()
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    try:
        # cursor.execute("SELECT COUNT(*) FROM project WHERE project_name = %s", (request.project_name,))
        # project_name_count = cursor.fetchone()[0]
        # if project_name_count > 0:
        #     cursor.execute("SELECT project_id FROM project WHERE project_name = %s", (request.project_name,))
        #     project_id_value = cursor.fetchone()[0]
        #     if project_id_value == id:
        #         pass
        #     else:
        #         return JSONResponse({"message": "Duplicate project name found."}, status_code=400)

        cursor.execute("SELECT COUNT(*) FROM project WHERE cost_sheets = %s", (request.cost_sheets,))
        cost_sheet_count = cursor.fetchone()[0]
        if cost_sheet_count > 0:
            cursor.execute("SELECT project_id FROM project WHERE cost_sheets = %s", (request.cost_sheets,))
            project_id_value = cursor.fetchone()[0]
            if project_id_value == id:
                pass
            else:
                return JSONResponse({"message": "Duplicate cost sheet found."}, status_code=400)
        
        
            
        # cursor.execute("SELECT COUNT(*) FROM project WHERE contract_number = %s", (request.contract_number,))
        # contract_number_count = cursor.fetchone()[0]
        # if contract_number_count > 0:
        #     cursor.execute("SELECT project_id FROM project WHERE contract_number = %s", (request.contract_number,))
        #     project_id_value = cursor.fetchone()[0]
        #     if project_id_value == id:
        #         pass
        #     else:
        #         return JSONResponse({"message": "Duplicate contract number found."}, status_code=400)
        cursor.execute(
            """
            SELECT users.username, users.email, customer.customer_name, project.project_name, project.start_date, project.end_date
            FROM project
            INNER JOIN users ON project.sales_person=users.id
            INNER JOIN customer ON project.customer_id=customer.customer_id
            WHERE project.project_id=%s
            """, (id,)
        )
        temp_data = cursor.fetchone()
        data = {
            "sales_person": temp_data[0],
            "project_id": id,
            "customer_name": temp_data[2], 
            "project_name": temp_data[3], 
            "start_date": temp_data[4], 
            "end_date": temp_data[5]
        }        
        cursor.execute(
            """
            UPDATE project
            SET customer_id=%s, cost_sheets=%s, project_name=%s, project_type=%s, 
            description=%s, contract_number=%s, internal_cost=%s, selling_prices=%s,
            sales_person=%s, created_at=%s, status=%s, on_site_engineer=%s
            WHERE project_id=%s
            """, (request.customer_id, request.cost_sheets, request.project_name, request.project_type,
                  request.description, request.contract_number, request.internal_cost,
                  request.selling_prices, request.sales_person, formatted_datetime, request.project_status, request.on_site_engineer, id)
        )
        conn.commit()
        conn.close()
        user_id = decode_jwt(user_token)
        if request.project_status == 'Pending':
            add_log(user_id, action_type="POST", action_detail="Updated and Submitted a project with project name '" + temp_data[3] + "'", entity_name="Project")
        else:
            add_log(user_id, action_type="UPDATE", action_detail="Editted a project draft with project name '" + temp_data[3] + "'", entity_name="Project")
        await send_email("Project has beed updated", [temp_data[1]], data, template=2)
        return JSONResponse({"message": "Success updating data"}, status_code=200)
    except Exception as err:
        conn.rollback()
        return JSONResponse({"message": "Error while edit project data", "error": str(err)}, status_code=500)
    
async def approve_project(id, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE project
            SET status='Approved', approved_by=%s
            WHERE project_id=%s
            """, (user_id, id)
        )
        try:
            cursor.execute(
                """
                SELECT users.username, users.email, customer.customer_name, project.project_name, project.start_date, project.end_date, sales.email
                FROM project
                LEFT JOIN users ON project.sales_person=users.id
                LEFT JOIN users sales ON project.created_by=sales.id 
                LEFT JOIN customer ON project.customer_id=customer.customer_id
                WHERE project.project_id=%s
                """, (id,)
            )
            temp_data = cursor.fetchone()
            print(temp_data)
            data = {
                "sales_person": temp_data[0],
                "project_id": id,
                "customer_name": temp_data[2], 
                "project_name": temp_data[3], 
                "start_date": temp_data[4], 
                "end_date": temp_data[5],
                "status": "Approved"
            } 
            # TODO: Tambahin CS
            print(temp_data[6])
            await send_email("Project has beed approved", [temp_data[6],'alvin.matthew@infracom-tech.com', 'helpdesk@infracom-tech.com'], data, template=3)
        except Exception as err:
            return JSONResponse({"message": "Error while edit approved data", "error": str(err)}, status_code=500)
        conn.commit()
        conn.close()
        add_log(user_id, action_type="APPROVE", action_detail="Approved a project with project name '" + temp_data[3] + "'", entity_name="Project")
        return JSONResponse({"message": "Project Approved"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while approve this project", "error": str(err)}, status_code=500)

async def reject_project(id, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE project
            SET status='Rejected', approved_by=%s
            WHERE project_id=%s
            """, (user_id, id)
        )
        try:
            cursor.execute(
                """
                SELECT users.username, users.email, customer.customer_name, project.project_name, project.start_date, project.end_date, sales.email
                FROM project
                INNER JOIN users ON project.sales_person=users.id
                INNER JOIN users sales ON project.sales_person=users.id 
                INNER JOIN customer ON project.customer_id=customer.customer_id
                WHERE project.project_id=%s
                """, (id,)
            )
            temp_data = cursor.fetchone()
            data = {
                "sales_person": temp_data[0],
                "project_id": id,
                "customer_name": temp_data[2], 
                "project_name": temp_data[3], 
                "start_date": temp_data[4], 
                "end_date": temp_data[5],
                "status": "Rejected"
            } 
            await send_email("Project has beed rejected", [temp_data[6]], data, template=3)
        except Exception as err:
            return JSONResponse({"message": "Error while edit rejecting data", "error": str(err)}, status_code=500)
        
        conn.commit()
        conn.close()
        add_log(user_id, action_type="REJECT", action_detail="Rejected a project with project name '" + temp_data[3] + "'", entity_name="Project")
        return JSONResponse({"message": "Project Rejected"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while reject this project", "error": str(err)}, status_code=500)
    
def get_pending_project(status):
    conn = create_connection()
    cursor = conn.cursor()
    data = []
    try:
        cursor.execute(
            """
            SELECT project_id, project.cost_sheets, project.project_name, users.username, customer.customer_name  
            FROM project
            INNER JOIN users ON project.sales_person=users.id
            INNER JOIN customer ON project.customer_id=customer.customer_id
            WHERE status=%s
            ORDER BY project.created_at DESC
            """, (status,)
        )
        project_raw_data = cursor.fetchall()
        for project in project_raw_data:
            try:
                cursor.execute(
                    """
                    SELECT product_name
                    FROM product
                    WHERE project_id=%s
                    """,(project[0],)
                )
                product = cursor.fetchall()
                if len(product) > 1:
                    data.append({
                        "project_id": project[0],
                        "costsheet": project[2],
                        "project_name": project[4],
                        "sales_person": project[3],
                        "customer_name": project[1],
                        "product": str(len(product)) + " Products"
                    })
                elif len(product) == 1:
                    data.append({
                        "project_id": project[0],
                        "costsheet": project[2],
                        "project_name": project[4],
                        "sales_person": project[3],
                        "customer_name": project[1],
                        "product": product[0][0]
                    })
                else:
                    data.append({
                        "project_id": project[0],
                        "costsheet": project[2],
                        "project_name": project[4],
                        "sales_person": project[3],
                        "customer_name": project[1],
                        "product": "No Products"
                    })
            except Exception as err:
                return JSONResponse({"message": "Error fetch product data", "error": str(err)}, status_code=500)    
        conn.close()
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while fetch project data", "error": str(err)}, status_code=500)
    
def check_is_approver(user_id, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    is_approver = False
    try:
        cursor.execute(
            """
            SELECT isapprover FROM users WHERE id=%s
            """, (user_id,)
        )
        temp_data = cursor.fetchone()
        is_approver = temp_data[0]
        if is_approver:
            cursor.execute(
                """
                SELECT created_by FROM project WHERE project_id=%s
                """, (project_id,)
            )
            temp_data = cursor.fetchone()
            db_user = temp_data[0]
            if user_id == db_user:
                return JSONResponse({"isApprover": False}, status_code=200)
            
            return JSONResponse({"isApprover": True}, status_code=200)
        else:
            return JSONResponse({"isApprover": False}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while check approver validation", "error": str(err)}, status_code=500)