from pydantic import BaseModel
from typing import Optional

class PagamentoSchema(BaseModel):

    id_metodo_pagamento: int
    id_corrida: int

    valor: float
    datahora_transacao: Optional[str] = None

    class Config:
        from_attributes = True