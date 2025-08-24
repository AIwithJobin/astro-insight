from pydantic import BaseModel
from datetime import date

class BirthData(BaseModel):
    name: str
    birth_date: date
    birth_time: str 
    birth_place: str 
    language: str = "en"