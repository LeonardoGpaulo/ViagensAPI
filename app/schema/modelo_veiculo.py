from pydantic import BaseModel
from typing import Optional

class ModeloVeiculoSchema(BaseModel):
    nome: Optional[str] = None
    fabricante: Optional[str] = None
    cor: Optional[str] = None
    ano: Optional[int] = None
    capacidade: Optional[int] = None
    propriedade: Optional[str] = None
    id_tipo_combustivel: Optional[int] = None
    
    class config():
        from_attributes = True