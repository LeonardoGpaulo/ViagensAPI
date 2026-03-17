from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MotoristaVeiculoSchema(BaseModel):
    id_motorista: Optional[int] = None
    id_veiculo: Optional[int] = None
    datahora_inicio: Optional[datetime] = None
    datahora_fim: Optional[datetime] = None

    class config():
        from_attributes = True