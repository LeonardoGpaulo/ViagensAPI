from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.motorista_veiculo import MotoristaVeiculoModels
from app.schema.motorista_veiculo import MotoristaVeiculoSchema

motorista_veiculo = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo motorista_veiculo

@motorista_veiculo.post("/{id_motorista}/{id_veiculo}")
async def criar_motorista_veiculo(id_motorista: int, id_veiculo: int, db: Session = Depends(get_db)):
    novo_motorista_veiculo = MotoristaVeiculoModels(id_motorista=id_motorista, id_veiculo=id_veiculo)
    db.add(novo_motorista_veiculo)
    db.commit()
    db.refresh(novo_motorista_veiculo)
    return novo_motorista_veiculo 

##----------------------------------------------------------------------------##

# Listar todos os motorista_veiculo

@motorista_veiculo.get("/listar")
async def listar_motorista_veiculo(db: Session = Depends(get_db)):
    return db.query(MotoristaVeiculoModels).all()

##----------------------------------------------------------------------------##

# Deletar um motorista_veiculo por ID

@motorista_veiculo.delete("/deletar/{id_motorista}/{id_veiculo}")
async def deletar_motorista_veiculo(id_motorista: int, id_veiculo: int, db: Session = Depends(get_db)):
    motorista_veiculo = db.query(MotoristaVeiculoModels).filter(MotoristaVeiculoModels.id_motorista == id_motorista, MotoristaVeiculoModels.id_veiculo == id_veiculo).first()

    if not motorista_veiculo:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O motorista_veiculo com ID {id_motorista} e ID {id_veiculo} não foi encontrado")
    
    db.delete(motorista_veiculo)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um motorista_veiculo por ID

@motorista_veiculo.put("/atualizar/{id_motorista}/{id_veiculo}")
async def atualizar_motorista_veiculo(id_motorista: int, id_veiculo: int, motorista_veiculo: MotoristaVeiculoSchema, db: Session = Depends(get_db)):
    motorista_veiculo_atualizar = db.query(MotoristaVeiculoModels).filter(MotoristaVeiculoModels.id_motorista == id_motorista, MotoristaVeiculoModels.id_veiculo == id_veiculo).first()

    if not motorista_veiculo_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O motorista_veiculo com ID {id_motorista} e ID {id_veiculo} não foi encontrado")
    
    for key, value in motorista_veiculo.model_dump().items():
        setattr(motorista_veiculo_atualizar, key, value)
    db.commit()
    db.refresh(motorista_veiculo_atualizar)
    return motorista_veiculo_atualizar



