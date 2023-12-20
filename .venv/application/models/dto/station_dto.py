from pydantic import BaseModel


class StationDTO(BaseModel):
    """ DTO для добавления новой станции """
    id: int
    name: str
