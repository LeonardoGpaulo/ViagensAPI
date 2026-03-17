from pydantic import BaseModel
from typing import Optional

class MetodoPagamentoSchema(BaseModel):
    nome_financeira: Optional[str] = None
    descricao: Optional[str] = None

    class config():
        from_attributes = True