from dataclasses import dataclass
from datetime import datetime


@dataclass
class Car:
    id: int
    brand: str
    model: str
    body_type: str
    price: int
    year: int
    created_at: datetime
    updated_at: datetime

