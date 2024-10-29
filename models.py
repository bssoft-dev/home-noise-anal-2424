from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Itech_Sensings_2424(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # 자동 넘버링
    device_id: str
    temp: float
    humidity: float
    co2: int
    voc: int
    pm1: int
    pm2_5: int
    pm10: int
    vibration: float
    noise_level: str
    noise_type: str
    utime: int
    insert_datetime: datetime

class Itech_Sensings_2424Receive(SQLModel, table=False):
    temp: float = None
    humidity: float = None
    co2: int = None
    voc: int = None
    pm1: int = None
    pm2_5: int = None
    pm10: int = None
    vibration: float = None
    noise_level: str = ''
    noise_type: str = ''
    