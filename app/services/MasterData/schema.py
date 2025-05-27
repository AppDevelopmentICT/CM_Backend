from pydantic import BaseModel, Field

class Customer(BaseModel):
    customer_name: str = Field(description="Short name or alias for the customer.", examples=['Bank BNI'])
    customer_fullname: str = Field(description="Full name of the customer.", examples=['Bank Nasional Indonesia'])
    customer_field: str = Field(description="Industry or sector in which the customer operates.", examples=['Banking'])
    employee: str = Field(description="Size range of the customer’s organization in terms of employees.", examples=['10-50 Employees'])
    
class User(BaseModel):
    username: str = Field(description="User's login name.", examples=['John'])
    isApprover: bool = Field(description="Indicates if the user has approver rights.", examples=[False])
    email: str = Field(description="User's email address.", examples=['john@infracom-tech.com'])
    user_roles: str = Field(description="Roles assigned to the user.", examples=['Sales'])
    
class CM_By(BaseModel):
    name: str = Field(description="Name of the Configuration Manager (CM) responsible for the project.", examples=['ICT'])

class PM_By(BaseModel):
    name: str = Field(description="Name of the Project Manager (PM) responsible for the project.", examples=['ICT'])

class Periode(BaseModel):
    periodic: str = Field(description="Time period for reporting or activities, e.g., Monthly, Quarterly, Semester.", examples=['Semester'])

class Category(BaseModel):
    category: str = Field(description="Type or classification of items or services, e.g., Hardware, Software.", examples=['Hardware'])

class Principal(BaseModel):
    principal_name: str = Field(description="Name of the principal or main vendor/supplier.", examples=['Mendix'])

class Implementation(BaseModel):
    implementation_by: str = Field(description="Name of the Implementation or main vendor/supplier.", examples=['Mendix'])
