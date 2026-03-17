from pydantic import BaseModel
from typing import Optional

class MotoristaSchema(BaseModel):
    id_usuario: Optional[int] = None
    media_avaliacao: Optional[float] = None
    cnh: Optional[int] = None

    class config():
        from_attributes = True