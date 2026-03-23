from pydantic import BaseModel
from typing import Optional

class VeiculoSchema(BaseModel):
    id_modelo_veiculo: Optional[int] = None
    id_classe_veiculo: Optional[int] = None
    placa: Optional[str] = None
    tem_seguro: Optional[str] = None

    class config():
        from_atributes = True