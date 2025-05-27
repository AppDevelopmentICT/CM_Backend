import uuid

from utils.database import create_connection
from fastapi.responses import JSONResponse
from datetime import datetime

def add_maintenance_data(request, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    cmId = str(uuid.uuid4())
    pmId = str(uuid.uuid4())
    slaId = str(uuid.uuid4())
    implementationId = str(uuid.uuid4())
    try:
        if not request.preventive_maintenance == None:
            try:
                cursor.execute(
                    """
                    SELECT * 
                    FROM preventive_maintenance
                    WHERE project_id=%s
                    """, (project_id,)
                )
                temp_data = cursor.fetchall()
                row_total = len(temp_data)
                if row_total == 0:
                    cursor.execute(
                        """
                        INSERT INTO preventive_maintenance (pm_id, pm_by, start_date, end_date, pm_periode, project_id, is_parent, quantity)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (pmId, request.preventive_maintenance.pm_by, request.preventive_maintenance.start_date, request.preventive_maintenance.end_date, 
                            request.preventive_maintenance.pm_periode, project_id, True, request.preventive_maintenance.quantity)
                    )
            except Exception as err:
                return JSONResponse({"message": "Error while adding PM data", "error": str(err)}, status_code=500)
        if not request.corrective_maintenance == None:
            try:
                cursor.execute(
                    """
                    SELECT * 
                    FROM corrective_maintenance
                    WHERE project_id=%s
                    """, (project_id,)
                )
                temp_data = cursor.fetchall()
                row_total = len(temp_data)
                if row_total == 0:
                    cursor.execute(
                        """
                        INSERT INTO corrective_maintenance (cm_id, cm_by, start_date, end_date, project_id, is_parent, quantity)
                        VALUES(%s, %s, %s, %s, %s, %s, %s)
                        """, (cmId, request.corrective_maintenance.cm_by, request.corrective_maintenance.start_date, request.corrective_maintenance.end_date, 
                            project_id, True, request.corrective_maintenance.quantity)
                    )
            except Exception as err:
                return JSONResponse({"message": "Error while adding CM data", "error": str(err)}, status_code=500)
        if not request.sla == None:
            try:
                cursor.execute(
                    """
                    SELECT * 
                    FROM sla_table
                    WHERE project_id=%s
                    """, (project_id,)
                )
                temp_data = cursor.fetchall()
                row_total = len(temp_data)
                if row_total == 0:
                    cursor.execute(
                        """
                        INSERT INTO sla_table (
                            sla_id, severity_1_response_time, severity_1_resolution_time, severity_2_response_time, severity_2_resolution_time, severity_3_response_time,
                            severity_3_resolution_time, severity_4_response_time, severity_4_resolution_time, project_id, is_parent)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (slaId, request.sla.severity_1_response_time,
                            request.sla.severity_1_resolution_time, request.sla.severity_2_response_time,
                            request.sla.severity_2_resolution_time, request.sla.severity_3_response_time,
                            request.sla.severity_3_resolution_time, request.sla.severity_4_response_time,
                            request.sla.severity_4_resolution_time, project_id, True)
                    )
                 
            except Exception as err:
                return JSONResponse({"message": "Error while adding SLA data", "error": str(err)}, status_code=500)
        if not request.implementation == None:
            try:
                cursor.execute(
                    """
                    SELECT * 
                    FROM implementation_table
                    WHERE project_id=%s
                    """, (project_id,)
                )
                temp_data = cursor.fetchall()
                row_total = len(temp_data)
                if row_total == 0:
                    cursor.execute(
                        """
                        INSERT INTO implementation_table (implementation_id, implementation_type, project_id, is_parent, start_date, end_date)
                        VALUES(%s, %s, %s, %s, %s, %s)
                        """, (implementationId, request.implementation.implementation_type, project_id, True, request.implementation.start_date, request.implementation.end_date)
                    )
            except Exception as err:
                return JSONResponse({"message": "Error while adding implementation data", "error": str(err)}, status_code=500)
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success add all maintenance data", "cm_id": cmId, "pm_id": pmId, "sla_id": slaId, "implementation_id": implementationId}, status_code=201) 
    except Exception as err:
        return JSONResponse({"message": "Error while adding data", "error": str(err)}, status_code=500)

def update_maintenance_data(request, project_id, pm_id, cm_id, sla_id, implementation_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        if request.preventive_maintenance is not None:
            try:
                cursor.execute(
                    """
                    UPDATE preventive_maintenance 
                    SET pm_by = %s, start_date = %s, end_date = %s, pm_periode = %s, quantity = %s
                    WHERE project_id = %s AND is_parent = False AND pm_id=%s 
                    """, (request.preventive_maintenance.pm_by, request.preventive_maintenance.start_date,
                          request.preventive_maintenance.end_date, request.preventive_maintenance.pm_periode,
                          request.preventive_maintenance.quantity, project_id, pm_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating PM data", "error": str(err)}, status_code=500)     
        if request.corrective_maintenance is not None:
            try:
                cursor.execute(
                    """
                    UPDATE corrective_maintenance 
                    SET cm_by = %s, start_date = %s, end_date = %s, quantity = %s
                    WHERE project_id = %s AND is_parent = False AND cm_id=%s
                    """, (request.corrective_maintenance.cm_by, request.corrective_maintenance.start_date,
                          request.corrective_maintenance.end_date, request.corrective_maintenance.quantity, project_id, cm_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating CM data", "error": str(err)}, status_code=500)
        if request.sla is not None:
            try:
                cursor.execute(
                    """
                    UPDATE sla_table 
                    SET severity_1_response_time = %s, severity_1_resolution_time = %s, 
                        severity_2_response_time = %s, severity_2_resolution_time = %s, 
                        severity_3_response_time = %s, severity_3_resolution_time = %s, 
                        severity_4_response_time = %s, severity_4_resolution_time = %s
                    WHERE project_id = %s AND is_parent = False AND sla_id=%s
                    """, (request.sla.severity_1_response_time, request.sla.severity_1_resolution_time,
                          request.sla.severity_2_response_time, request.sla.severity_2_resolution_time,
                          request.sla.severity_3_response_time, request.sla.severity_3_resolution_time,
                          request.sla.severity_4_response_time, request.sla.severity_4_resolution_time, project_id, sla_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating SLA data", "error": str(err)}, status_code=500)
        if request.implementation is not None:
            try:
                cursor.execute(
                """
                UPDATE implementation_table 
                SET implementation_type = %s, start_date = %s, end_date = %s
                WHERE project_id = %s AND is_parent = False AND implementation_id=%s
                """, (request.implementation.implementation_type, request.implementation.start_date, request.implementation.end_date, project_id, implementation_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating implementation data", "error": str(err)}, status_code=500)
        try:
            cursor.execute(
                """
                UPDATE product
                SET preventive_maintenance = COALESCE(%s, preventive_maintenance),
                    corrective_maintenance = COALESCE(%s, corrective_maintenance),
                    sla_id = COALESCE(%s, sla_id),
                    implementation_id = COALESCE(%s, implementation_id)
                WHERE project_id = %s
                """, (pm_id, cm_id, sla_id, implementation_id, project_id)
            )
        except Exception as err:
            conn.rollback()
            return JSONResponse({"message": "Error while update current data", "error": str(err)}, status_code=500)
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success updating maintenance data"}, status_code=200) 
    except Exception as err:
        return JSONResponse({"message": "Error while adding data", "error": str(err)}, status_code=500)

def update_parent_maintenance(request, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        if request.preventive_maintenance is not None:
            try:
                cursor.execute(
                    """
                    UPDATE preventive_maintenance 
                    SET pm_by = %s, start_date = %s, end_date = %s, pm_periode = %s, quantity = %s
                    WHERE project_id = %s AND is_parent = True 
                    """, (request.preventive_maintenance.pm_by, request.preventive_maintenance.start_date,
                          request.preventive_maintenance.end_date, request.preventive_maintenance.pm_periode,
                          request.preventive_maintenance.quantity, project_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating PM data", "error": str(err)}, status_code=500)     
        if request.corrective_maintenance is not None:
            try:
                cursor.execute(
                    """
                    UPDATE corrective_maintenance 
                    SET cm_by = %s, start_date = %s, end_date = %s, quantity = %s
                    WHERE project_id = %s AND is_parent = True
                    """, (request.corrective_maintenance.cm_by, request.corrective_maintenance.start_date,
                          request.corrective_maintenance.end_date, request.corrective_maintenance.quantity, project_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating CM data", "error": str(err)}, status_code=500)
        if request.sla is not None:
            try:
                cursor.execute(
                    """
                    UPDATE sla_table 
                    SET severity_1_response_time = %s, severity_1_resolution_time = %s, 
                        severity_2_response_time = %s, severity_2_resolution_time = %s, 
                        severity_3_response_time = %s, severity_3_resolution_time = %s, 
                        severity_4_response_time = %s, severity_4_resolution_time = %s
                    WHERE project_id = %s AND is_parent = True
                    """, (request.sla.severity_1_response_time, request.sla.severity_1_resolution_time,
                          request.sla.severity_2_response_time, request.sla.severity_2_resolution_time,
                          request.sla.severity_3_response_time, request.sla.severity_3_resolution_time,
                          request.sla.severity_4_response_time, request.sla.severity_4_resolution_time, project_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating SLA data", "error": str(err)}, status_code=500)
        if request.implementation is not None:
            try:
                cursor.execute(
                """
                UPDATE implementation_table 
                SET implementation_type = %s, start_date = %s, end_date = %s
                WHERE project_id = %s AND is_parent = True
                """, (request.implementation.implementation_type, request.implementation.start_date, request.implementation.end_date, project_id)
                )
            except Exception as err:
                return JSONResponse({"message": "Error while updating implementation data", "error": str(err)}, status_code=500)
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success updating maintenance data"}, status_code=200) 
    except Exception as err:
        return JSONResponse({"message": "Error while adding data", "error": str(err)}, status_code=500)
    
def create_pm(request, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    try:
        cursor.execute(
            """
            SELECT * 
            FROM preventive_maintenance
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        row_total = len(temp_data)
        if row_total == 0:
            cursor.execute(
                """
                INSERT INTO preventive_maintenance (pm_id, pm_by, start_date, end_date, pm_periode, project_id, is_parent, quantity)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id, request.pm_by, request.start_date, request.end_date, 
                      request.pm_periode, project_id, True, request.quantity)
            )
        else:
            cursor.execute(
                """
                INSERT INTO preventive_maintenance (pm_id, pm_by, start_date, end_date, pm_periode, project_id, is_parent, quantity)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id, request.pm_by, request.start_date, request.end_date, 
                      request.pm_periode, project_id, False, request.quantity)
            )     
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success add pm data", "id": id}, status_code=200)  
    except Exception as err:
        return JSONResponse({"message": "Error while verify pm data", "error": str(err)}, status_code=500)

def create_cm(request, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    try:
        cursor.execute(
            """
            SELECT * 
            FROM corrective_maintenance
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        row_total = len(temp_data)
        if row_total == 0:
            cursor.execute(
                """
                INSERT INTO corrective_maintenance (cm_id, cm_by, start_date, end_date, project_id, is_parent, quantity)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                """, (id, request.cm_by, request.start_date, request.end_date, 
                      project_id, True, request.quantity)
            )
        else:
            cursor.execute(
                """
                INSERT INTO corrective_maintenance (cm_id, cm_by, start_date, end_date, project_id, is_parent, quantity)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                """, (id, request.cm_by, request.start_date, request.end_date, 
                      project_id, False, request.quantity)
            )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success add cm data", "id": id}, status_code=200)  
    except Exception as err:
        return JSONResponse({"message": "Error while verify cm data", "error": str(err)}, status_code=500)

def create_sla(request, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    try:
        cursor.execute(
            """
            SELECT * 
            FROM sla_table
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        row_total = len(temp_data)
        if row_total == 0:
            cursor.execute(
                """
                INSERT INTO sla_table (
                    sla_id, severity_1_response_time, severity_1_resolution_time, severity_2_response_time, severity_2_resolution_time, severity_3_response_time,
                    severity_3_resolution_time, severity_4_response_time, severity_4_resolution_time, project_id, is_parent)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id, request.severity_1_response_time,
                      request.severity_1_resolution_time, request.severity_2_response_time,
                      request.severity_2_resolution_time, request.severity_3_response_time,
                      request.severity_3_resolution_time, request.severity_4_response_time,
                      request.severity_4_resolution_time, project_id, True)
            )
        else:
            cursor.execute(
                """
                INSERT INTO sla_table (
                    sla_id, severity_1_response_time, severity_1_resolution_time, severity_2_response_time, severity_2_resolution_time, severity_3_response_time,
                    severity_3_resolution_time, severity_4_response_time, severity_4_resolution_time, project_id, is_parent)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id, request.severity_1_response_time,
                      request.severity_1_resolution_time, request.severity_2_response_time,
                      request.severity_2_resolution_time, request.severity_3_response_time,
                      request.severity_3_resolution_time, request.severity_4_response_time,
                      request.severity_4_resolution_time, project_id, False)
            )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success add sla data", "id": id}, status_code=200)  
    except Exception as err:
        return JSONResponse({"message": "Error while verify data", "error": str(err)}, status_code=500)

def create_implementation(request, project_id):
    conn = create_connection()
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    try:
        cursor.execute(
            """
            SELECT * 
            FROM implementation_table
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        row_total = len(temp_data)
        if row_total == 0:
            cursor.execute(
                """
                INSERT INTO implementation_table (implementation_id, implementation_type, project_id, is_parent, start_date, end_date)
                VALUES(%s, %s, %s, %s, %s, %s)
                """, (id, request.implementation_type, project_id, True, request.start_date, request.end_date)
            )
        else:
            cursor.execute(
                """
                INSERT INTO implementation_table (implementation_id, implementation_type, project_id, is_parent, start_date, end_date)
                VALUES(%s, %s, %s, %s, %s, %s)
                """, (id, request.implementation_type, project_id, False, request.start_date, request.end_date)
            )  
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Success add implementation data", "id": id}, status_code=200)  
    except Exception as err:
        return JSONResponse({"message": "Error while adding implementation data", "error": str(err)}, status_code=500)
    
def get_parent_pm(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * 
            FROM preventive_maintenance
            WHERE is_parent='True' AND project_id=%s
            """, (project_id,)
        )
        row = cursor.fetchone()
        if row is not None: 
            data = {
                "pm_id": row[0],
                "pm_by": row[1],
                "start_date": str(row[2]),
                "end_date": str(row[3]),
                "pm_periode": row[4],
                "project_id": row[5],
                "is_parent": row[6],
                "quantity": row[7]
            }
            return JSONResponse({"data": data}, status_code=200) 
        return JSONResponse({"message": "No Data Found"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while get pm data", "error": str(err)}, status_code=500)
        
def get_parent_cm(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * 
            FROM corrective_maintenance
            WHERE is_parent='True' AND project_id=%s
            """, (project_id,)
        )
        row = cursor.fetchone()
        if row is not None: 
            data = {
                "cm_id": row[0],
                "cm_by": row[1],
                "start_date": str(row[2]),
                "end_date": str(row[3]),
                "project_id": row[4],
                "is_parent": row[5],
                "quantity": row[6]
            }
            return JSONResponse({"data": data}, status_code=200)
        return JSONResponse({"message": "No data found"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while get CM data", "error": str(err)}, status_code=500)
        
def get_parent_sla(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * 
            FROM sla_table
            WHERE is_parent='True' AND project_id=%s
            """, (project_id,)
        )
        row = cursor.fetchone()
        if row is not None: 
            data = {
                "sla_id": row[0],
                "severity_1_response_time": row[1],
                "severity_1_resolution_time": row[2],
                "severity_2_response_time": row[3],
                "severity_2_resolution_time": row[4],
                "severity_3_response_time": row[5],
                "severity_3_resolution_time": row[6],
                "severity_4_response_time": row[7],
                "severity_4_resolution_time": row[8],
                "project_id": row[9],
                "is_parent": row[10],
            }
            return JSONResponse({"data": data}, status_code=200) 
        return JSONResponse({"message": "No Data Found"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while get sla data", "error": str(err)}, status_code=500)
        
def get_parent_implementation(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * 
            FROM implementation_table
            WHERE is_parent='True' AND project_id=%s
            """, (project_id,)
        )
        row = cursor.fetchone()
        if row is not None: 
            data = {
                "implementation_id": row[0],
                "implementation_type": row[1],
                "project_id": row[2],
                "is_parent": row[3],
                "start_date": str(row[4]),
                "end_date": str(row[5]),
            }
            return JSONResponse({"data": data}, status_code=200) 
        return JSONResponse({"message": "No Data Found"}, status_code=200)

    except Exception as err:
        return JSONResponse({"message": "Error while get implementation data", "error": str(err)}, status_code=500)

def update_pm(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE preventive_maintenance
            SET pm_by=%s, start_date=%s, end_date=%s, pm_periode=%s, quantity=%s
            WHERE pm_id=%s
            """, (request.pm_by, request.start_date, request.end_date, 
                  request.pm_periode, request.quantity, id)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Succesfully update pm data"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while update pm data", "error": str(err)}, status_code=500)

def update_cm(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE corrective_maintenance
            SET cm_by=%s, start_date=%s, end_date=%s, quantity=%s
            WHERE cm_id=%s
            """, (request.pm_by, request.start_date, request.end_date, 
                request.quantity, id)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Succesfully update cm data"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while update cm data", "error": str(err)}, status_code=500)

def update_sla(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE sla_table 
            SET severity_1_response_time = %s, severity_1_resolution_time = %s, 
                severity_2_response_time = %s, severity_2_resolution_time = %s, 
                severity_3_response_time = %s, severity_3_resolution_time = %s, 
                severity_4_response_time = %s, severity_4_resolution_time = %s
            WHERE sla_id
            """, (request.severity_1_response_time, request.severity_1_resolution_time,
                    request.severity_2_response_time, request.severity_2_resolution_time,
                    request.severity_3_response_time, request.severity_3_resolution_time,
                    request.severity_4_response_time, request.severity_4_resolution_time, id)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Succesfully update sla data"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while update sla data", "error": str(err)}, status_code=500)
    
def update_implementation(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE implementation_table 
            SET implementation_type = %s, start_date = %s, end_date = %s
            WHERE implementation_id=%s
            """, (request.implementation_type, request.start_date, request.end_date, id)
            )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Succesfully update implementation data"}, status_code=200)
    except Exception as err:
        return JSONResponse({"message": "Error while update implementation data", "error": str(err)}, status_code=500)

def get_list_pm_by_project(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM preventive_maintenance
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        data = {
            "master": {
                "pm_id": '',
                "pm_by": '',
                "start_date": '',
                "end_date": '',
                "pm_periode": '',
                "project_id": '',
                "is_parent": '',
                "quantity": ''
            },
            "other": []
        }
        for row in temp_data:
            if row[6] == True:
                data["master"]["pm_id"] = row[0]
                data["master"]["pm_by"] = row[1]
                data["master"]["start_date"] = str(row[2])
                data["master"]["end_date"] = str(row[3])
                data["master"]["pm_periode"] = row[4]
                data["master"]["project_id"] = row[5]
                data["master"]["is_parent"] = row[6]
                data["master"]["quantity"] = row[7]
            else:
                data["other"].append({
                    "pm_id": row[0],
                    "pm_by": row[1],
                    "start_date": str(row[2]),
                    "end_date": str(row[3]),
                    "pm_periode": row[4],
                    "project_id": row[5],
                    "is_parent": row[6],
                    "quantity": row[7]
                })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        JSONResponse({"message": "Error while get all pm data", "error": err}, status_code=500)

def get_list_cm_by_project(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM corrective_maintenance
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        data = {
            "master": {
                "cm_id": '',
                "cm_by": '',
                "start_date": '',
                "end_date": '',
                "project_id": '',
                "is_parent": '',
                "quantity": ''
            },
            "other": []
        }
        for row in temp_data:
            if row[5] == True:
                data["master"]["pm_id"] = row[0]
                data["master"]["pm_by"] = row[1]
                data["master"]["start_date"] = str(row[2])
                data["master"]["end_date"] = str(row[3])
                data["master"]["project_id"] = row[4]
                data["master"]["is_parent"] = row[5]
                data["master"]["quantity"] = row[6]
            else:
                data["other"].append({
                    "pm_id": row[0],
                    "pm_by": row[1],
                    "start_date": str(row[2]),
                    "end_date": str(row[3]),
                    "project_id": row[4],
                    "is_parent": row[5],
                    "quantity": row[6]
                })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        JSONResponse({"message": "Error while get all cm data", "error": err}, status_code=500)

def get_list_sla_by_project(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM sla_table
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        data = {
            "master": {
                "sla_id": '',
                "severity_1_response_time": '',
                "severity_1_resolution_time": '',
                "severity_2_response_time": '',
                "severity_2_resolution_time": '',
                "severity_3_response_time": '',
                "severity_3_resolution_time": '',
                "severity_4_response_time": '',
                "severity_4_resolution_time": '',
                "project_id": '',
                "is_parent": '',
            },
            "other": []
        }
        for row in temp_data:
            if row[10] == True:
                data["master"]["sla_id"] = row[0]
                data["master"]["severity_1_response_time"] = row[1]
                data["master"]["severity_1_resolution_time"] = row[2]
                data["master"]["severity_2_response_time"] = row[3]
                data["master"]["severity_2_resolution_time"] = row[4]
                data["master"]["severity_3_response_time"] = row[5]
                data["master"]["severity_3_resolution_time"] = row[6]
                data["master"]["severity_4_response_time"] = row[7]
                data["master"]["severity_4_resolution_time"] = row[8]
                data["master"]["project_id"] = row[9]
                data["master"]["is_parent"] = row[10]
            else:
                data["other"].append({
                    "sla_id": row[0],
                    "severity_1_response_time": row[1],
                    "severity_1_resolution_time": str(row[2]),
                    "severity_2_response_time": str(row[3]),
                    "severity_2_resolution_time": row[4],
                    "severity_3_response_time": row[5],
                    "severity_3_resolution_time": row[6],
                    "severity_4_response_time": row[7],
                    "severity_4_resolution_time": row[8],
                    "project_id": row[9],
                    "is_parent": row[10],
                })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        JSONResponse({"message": "Error while get all sla data", "error": err}, status_code=500)

def get_list_implementation_by_project(project_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM implementation_table
            WHERE project_id=%s
            """, (project_id,)
        )
        temp_data = cursor.fetchall()
        data = {
            "master": {
                "implementation_id": '',
                "implementation_type": '',
                "periode": '',
                "project_id": '',
                "is_parent": '',
            },
            "other": []
        }
        for row in temp_data:
            if row[4] == True:
                data["master"]["implementation_id"] = row[0]
                data["master"]["implementation_type"] = row[1]
                data["master"]["periode"] = str(row[2])
                data["master"]["project_id"] = row[3]
                data["master"]["is_parent"] = row[4]
            else:
                data["other"].append({
                    "implementation_id": row[0],
                    "implementation_type": row[1],
                    "periode": row[2],
                    "project_id": row[3],
                    "is_parent": row[4],
                })
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        JSONResponse({"message": "Error while get all implementation data", "error": err}, status_code=500)
        
