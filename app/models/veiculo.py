from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class VeiculoModels(Base):
    __tablename__ = "veiculo"

    id_veiculo = Column(Integer, primary_key=True)
    id_modelo_veiculo = Column(Integer, ForeignKey("modelo_veiculo.id_modelo_veiculo"))
    id_classe_veiculo = Column(Integer, ForeignKey("classe_veiculo.id_classe_veiculo"))

    placa = Column(String(7))
    tem_seguro = Column(String(3))