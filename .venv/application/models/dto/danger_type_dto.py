from pydantic import BaseModel


class DangerTypeDTO(BaseModel):
    """ DTO для добавления нового типа """
    id: int
    type: str
