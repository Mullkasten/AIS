from pydantic import BaseModel
from typing import (
    Deque, Dict, List, Optional, Sequence, Set, Tuple, Union
)

from datetime import datetime


class DangerDTO(BaseModel):
    """ DTO для добавления, обновления и получения информации об активности.
        Если данные, передаваемые клиенту сильно отличаются от данных,
        которые принимает REST API сервера, необходимо разделять DTO
        для запросов и ответов, например, WeatherRequestDTO, WeatherResponseDTO """
    id: int
    magnitude: int
    frequency: int
    type: int
    station: int
    updated_on: Optional[datetime]
