from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timedelta
from typing import List

class ProjectType(str, Enum):
    contract = "Contract"
    purchase_order = "Purchase Order"
    spk = "SPK"
    other = "Other"

class SendEmail(BaseModel):
    email_subject: str = Field(description="Email Subject")
    receiver: List[str] = Field(description="List of email addresses of the receivers")
    # data: any = Field(description="Email Body")
    template: int = Field(description="Choose email template")

class Project(BaseModel):
    cost_sheets: str = Field(description="Reference number for the cost sheets.", example='123/2003/09')
    project_name: str = Field(description="Name of the project.", example='Membuat Aplikasi Contract Manangement')
    project_type: str = Field(description="Type of the project.", example=ProjectType.contract)
    description: str = Field(description="Detailed description of the project.")
    contract_number: str = Field(description="Contract number associated with the project.", example='08/XX/19/2023')
    internal_cost: int = Field(description="Internal cost incurred for the project.", example=120000000)
    selling_prices: int = Field(description="Selling price of the project.", example=500000000)
    customer_id: str = Field(description="Unique identifier for the customer.", example='71629acd-7e45-403f-ae1b-1ac65fa9575a')
    created_by: str = Field(description="Identifier of the user who created the project.", example='vph3cnfmwdkzr57')
    sales_person: str = Field(description="Identifier of the sales person responsible for the project.", example='zqazvowi0f5dskt')
    on_site_engineer: bool = Field(description="Indicates if an on-site engineer is required for the project.", example=False)
    project_status: str = Field(description="Current status of the project.", example='Pending')

class UpdateProject(BaseModel):
    cost_sheets: str = Field(description="Updated reference number for the cost sheets.", example='123/2043/09')
    project_name: str = Field(description="Updated name of the project.", example='Change Name')
    project_type: str = Field(description="Updated type of the project.", example=ProjectType.contract)
    description: str = Field(description="Updated detailed description of the project.")
    contract_number: str = Field(description="Updated contract number associated with the project.", example='08/XX/19/2023')
    internal_cost: int = Field(description="Updated internal cost incurred for the project.", example=120000000)
    selling_prices: int = Field(description="Updated selling price of the project.", example=500000000)
    customer_id: str = Field(description="Updated unique identifier for the customer.", example='71629acd-7e45-403f-ae1b-1ac65fa9575a')
    sales_person: str = Field(description="Updated identifier of the sales person responsible for the project.", example='zqazvowi0f5dskt')
    on_site_engineer: bool = Field(description="Indicates if an on-site engineer is still required for the project.", example=False)
    project_status: str = Field(description="Updated current status of the project.", example='Pending')

class ImportProject(BaseModel):
    customer_name: str = Field(description="Customer Name", example='PT XYZ')
    cost_sheets: str = Field(description="Cost Sheet", example='123/2043/09')
    sales_email: str = Field(description="Sales Email", example='sales@mail.com')
    customer_name: str = Field(description="Sales Name", example='Sales Man')
    project_name: str = Field(description="Project Name", example='Project X')
    project_type: str = Field(description="Project Type", example='Contract')
    product_brand: str = Field(description="Product Brand", example='Oracle')
    product_name: str = Field(description="Product Name", example='Oracle X')
    serial_number: str = Field(description="Serial Number", example='121212')
    product_quantity: int = Field(description="Product Quantity", example='2')
    start_date: datetime = Field(description="Start date of project", example=datetime.now())
    end_date: datetime = Field(description="End date of project", example=datetime.now())
    cm_by: str = Field(description="CM By", example='ICT')
    severity1_response_time: str = Field(description="Severity 1 Response Time", example='1')
    severity1_resolution_time: str = Field(description="Severity 1 Resolution Time", example='1')
    severity2_response_time: str = Field(description="Severity 2 Response Time", example='2')
    severity2_resolution_time: str = Field(description="Severity 2 Resolution Time", example='2')
    severity3_response_time: str = Field(description="Severity 3 Response Time", example='3')
    severity3_resolution_time: str = Field(description="Severity 3 Resolution Time", example='3')
    severity4_response_time: str = Field(description="Severity 4 Response Time", example='4')
    severity4_resolution_time: str = Field(description="Severity 4 Resolution Time", example='4')
    preventive_maintenance: str = Field(description="Preventive Maintenance", example='ICT')
    maintenance_period: str = Field(description="Maintenance Period", example='Semester')
    internal_cost: str = Field(description="Internal Cost", example='500000')
    selling_cost: str = Field(description="Selling Cost", example='500000')
    selling_cost: str = Field(description="Selling Cost", example='500000')


