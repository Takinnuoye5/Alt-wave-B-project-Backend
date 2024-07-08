from fastapi import APIRouter
from typing import List
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from flutter_app.schemas.users import Country
from flutter_app.services.users import UserService


router = APIRouter()
user_service = UserService()

@router.get("/countries", response_model=List[Country])
async def get_countries():
    countries = UserService.get_static_countries()
    return JSONResponse(content=[country.dict() for country in countries])