from fastapi import APIRouter, Header
from . import schema, service as APIServices
from typing import Annotated

master_data_router = APIRouter()

@master_data_router.post('/customer', tags=['Customer'])
async def add_customer(request: schema.Customer, user_token: Annotated[str, Header()]):
    add_customer_response = APIServices.add_customer(request, user_token)
    return add_customer_response

@master_data_router.get('/customer', tags=['Customer'])
async def get_customer_list():
    get_customer_list_response = APIServices.get_customer_list()
    return get_customer_list_response

@master_data_router.get('/customer/{id}', tags=['Customer'])
async def get_customer_by_id(id: str):
    get_customer_by_id_response = APIServices.get_customer_by_id(id)
    return get_customer_by_id_response

@master_data_router.delete('/customer/{id}', tags=['Customer'])
async def delete_customer(id: str, user_token: Annotated[str, Header()]):
    delete_customer_response = APIServices.delete_customer(id, user_token)
    return delete_customer_response

@master_data_router.patch('/customer/{id}', tags=['Customer'])
async def update_customer(request: schema.Customer, id: str, user_token: Annotated[str, Header()] ):
    update_customer_response = APIServices.update_customer(request, id, user_token)
    return update_customer_response

@master_data_router.get('/user', tags=['User'])
async def get_user_list():
    get_user_list_response = APIServices.get_user_list()
    return get_user_list_response

@master_data_router.get('/all_user', tags=['User'])
async def get_all_user(user_id: Annotated[str, Header()]):
    get_all_user_response = APIServices.get_all_user(user_id)
    return get_all_user_response

@master_data_router.get('/user/{id}', tags=['User'])
async def get_user_by_id(id: str):
    get_user_by_id_response = APIServices.get_user_by_id(id)
    return get_user_by_id_response

@master_data_router.delete('/user/{id}', tags=['User'])
async def delete_user(id: str, user_token: Annotated[str, Header()]):
    delete_user_response = APIServices.delete_user(id, user_token)
    return delete_user_response

@master_data_router.get('/user/pb/{email}', tags=['User'])
async def get_user_by_email(email: str):
    get_user_by_email_response = APIServices.get_user_by_email(email)
    return get_user_by_email_response

@master_data_router.patch('/user/{id}', tags=['User'])
async def update_user(id: str, request: schema.User, user_token: Annotated[str, Header()]):
    update_user_response = APIServices.update_user(id, request, user_token)
    return update_user_response

@master_data_router.get('/principal', tags=['Principal'])
async def get_principal_list():
    get_principal_list_response = APIServices.get_principal_list()
    return get_principal_list_response

@master_data_router.get('/principal/{id}', tags=['Principal'])
async def get_principal_by_id(id: str):
    get_principal_by_id_response = APIServices.get_principal_by_id(id)
    return get_principal_by_id_response

@master_data_router.post('/principal', tags=['Principal'])
async def add_principal(request: schema.Principal, user_token: Annotated[str, Header()]):
    add_principal_response = APIServices.add_principal(request, user_token)
    return add_principal_response

@master_data_router.delete('/principal/{id}', tags=['Principal'])
async def delete_principal(id: str, user_token: Annotated[str, Header()]):
    delete_principal_response = APIServices.delete_principal(id, user_token)
    return delete_principal_response

@master_data_router.patch('/principal/{id}', tags=['Principal'])
async def update_principal(request: schema.Principal, id: str, user_token: Annotated[str, Header()] ):
    update_principal_response = APIServices.update_principal(request, id, user_token)
    return update_principal_response

@master_data_router.get('/cm_by', tags=['Master Data'])
async def get_cm_by():
    get_cm_by_response = APIServices.get_cm_by()
    return get_cm_by_response

@master_data_router.post('/cm_by', tags=['Master Data'])
async def add_cm_by(request: schema.CM_By, user_token: Annotated[str, Header()]):
    add_cm_by_response = APIServices.add_cm_by(request, user_token)
    return add_cm_by_response

@master_data_router.delete('/cm_by/{name}', tags=['Master Data'])
async def delete_cm_by(name: str, user_token: Annotated[str, Header()]):
    delete_cm_by_response = APIServices.delete_cm_by(name, user_token)
    return delete_cm_by_response

@master_data_router.get('/pm_by', tags=['Master Data'])
async def get_pm_by():
    get_pm_by_response = APIServices.get_pm_by()
    return get_pm_by_response

@master_data_router.post('/pm_by', tags=['Master Data'])
async def add_pm_by(request: schema.PM_By, user_token: Annotated[str, Header()]):
    add_pm_by_response = APIServices.add_pm_by(request, user_token)
    return add_pm_by_response

@master_data_router.delete('/pm_by/{name}', tags=['Master Data'])
async def delete_pm_by(name: str, user_token: Annotated[str, Header()]):
    delete_pm_by_response = APIServices.delete_pm_by(name, user_token)
    return delete_pm_by_response

@master_data_router.get('/periode', tags=['Master Data'])
async def get_periode():
    get_periode_response = APIServices.get_periode()
    return get_periode_response

@master_data_router.post('/periode', tags=['Master Data'])
async def add_periode(request: schema.Periode, user_token: Annotated[str, Header()]):
    add_periode_response = APIServices.add_periode(request, user_token)
    return add_periode_response

@master_data_router.delete('/periode/{periode}', tags=['Master Data'])
async def delete_periode(periode: str, user_token: Annotated[str, Header()]):
    delete_periode_response = APIServices.delete_periode(periode, user_token)
    return delete_periode_response

@master_data_router.get('/category', tags=['Master Data'])
async def get_category():
    get_category_response = APIServices.get_category()
    return get_category_response

@master_data_router.post('/category', tags=['Master Data'])
async def add_category(request: schema.Category, user_token: Annotated[str, Header()]):
    add_category_response = APIServices.add_category(request, user_token)
    return add_category_response

@master_data_router.delete('/category/{category}', tags=['Master Data'])
async def delete_category(category: str, user_token: Annotated[str, Header()]):
    delete_category_response = APIServices.delete_category(category, user_token)
    return delete_category_response

@master_data_router.get('/implementation_by', tags=['Master Data'])
async def get_implementation():
    get_implementation_response = APIServices.get_implementation()
    return get_implementation_response

@master_data_router.post('/implementation_by', tags=['Master Data'])
async def add_implementation(request: schema.Implementation, user_token: Annotated[str, Header()]):
    add_implementation_response = APIServices.add_implementation(request, user_token)
    return add_implementation_response

@master_data_router.delete('/implementation_by/{implementation}', tags=['Master Data'])
async def delete_implementation(implementation: str, user_token: Annotated[str, Header()]):
    delete_implementation_response = APIServices.delete_implementation(implementation, user_token)
    return delete_implementation_response