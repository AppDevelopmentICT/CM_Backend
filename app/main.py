from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from services.Auth.api import auth_router
from services.MasterData.api import master_data_router
from services.Project.api import project_router
from services.Product.api import product_router
from services.Dashboard.api import dashboard_router
from services.Maintenance.api import maintenance_router
from services.AuditLog.api import audit_route
from utils.environment import API_VERSION

tags_metadata = [
    {
        "name": "Authorization",
        "description": "API to handle auth service for users, such as login, registed, access management, etc"
    }
]

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Contract Management Backend",
#         version=API_VERSION,
#         summary="API Endpoint for manage process on the application",
#         description="Here's a longer description of the custom **OpenAPI** schema",
#         routes=app.routes,
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


app = FastAPI()
# app.openapi = custom_openapi
app.include_router(auth_router)
app.include_router(audit_route)
app.include_router(project_router)
app.include_router(product_router)
app.include_router(dashboard_router)
app.include_router(maintenance_router)
app.include_router(master_data_router)

ALLOWED_ORIGINS = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"]
)