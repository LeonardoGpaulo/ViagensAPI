from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.modelo_veiculo import ModeloVeiculoModels
from app.schema.modelo_veiculo import ModeloVeiculoSchema

modelo_veiculo = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo modelo de veículo

@modelo_veiculo.post("/")
async def criar_modelo_veiculo(modelo_veiculo: ModeloVeiculoSchema, db: Session = Depends(get_db)):
    novo_modelo_veiculo = ModeloVeiculoModels(**modelo_veiculo.model_dump())
    db.add(novo_modelo_veiculo)
    db.commit()
    db.refresh(novo_modelo_veiculo)
    return novo_modelo_veiculo

##----------------------------------------------------------------------------##

# Listar todos os modelos de veículo

@modelo_veiculo.get("/listar")
async def listar_modelos_veiculo(db: Session = Depends(get_db)):
    return db.query(ModeloVeiculoModels).all()

##----------------------------------------------------------------------------##

# Deletar um modelo de veículo por ID

@modelo_veiculo.delete("/deletar/{id}")
async def deletar_modelo_veiculo(id: int, db: Session = Depends(get_db)):
    modelo_veiculo = db.query(ModeloVeiculoModels).filter(ModeloVeiculoModels.id_modelo_veiculo == id).first()

    if not modelo_veiculo:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O modelo de veículo com ID {id} não foi encontrado")
    
    db.delete(modelo_veiculo)
    db.commit()
    return("deletado")

#-----------------------------------------------------------------------------##

# Atualizar um modelo de veículo por ID

@modelo_veiculo.put("/atualizar/{id}")
async def atualizar_modelo_veiculo(id: int, modelo_veiculo: ModeloVeiculoSchema, db: Session = Depends(get_db)):
    modelo_veiculo_atualizar = db.query(ModeloVeiculoModels).filter(ModeloVeiculoModels.id_modelo_veiculo == id).first()

    if not modelo_veiculo_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O modelo de veículo com ID {id} não foi encontrado")
    
    for key, value in modelo_veiculo.model_dump().items():
        setattr(modelo_veiculo_atualizar, key, value)

    db.commit()
    db.refresh(modelo_veiculo_atualizar)
    return modelo_veiculo_atualizar
