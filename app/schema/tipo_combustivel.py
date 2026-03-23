from pydantic import BaseModel
from typing import Optional

class TipoCombustivelSchema(BaseModel):
    descricao: Optional[str] = None
    fator_carbono: Optional[float] = None