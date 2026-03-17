from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.passageiro import PassageiroModels
from app.schema.passageiro import PassageiroSchema

passageiro = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo passageiro

@passageiro.post("/")
async def criar_passageiro(passageiro: PassageiroSchema, db: Session = Depends(get_db)):
    novo_passageiro = PassageiroModels(**passageiro.model_dump())
    db.add(novo_passageiro)
    db.commit()
    db.refresh(novo_passageiro)
    return novo_passageiro

##----------------------------------------------------------------------------##

# Listar todos os passageiros

@passageiro.get("/listar")
async def listar_passageiros(db: Session = Depends(get_db)):
    return db.query(PassageiroModels).all() 

##----------------------------------------------------------------------------##

# Deletar um passageiro por ID

@passageiro.delete("/deletar/{id}")
async def deletar_passageiro(id: int, db: Session = Depends(get_db)):
    passageiro = db.query(PassageiroModels).filter(PassageiroModels.id_passageiro == id).first()

    if not passageiro:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O passageiro com ID {id} não foi encontrado")
    
    db.delete(passageiro)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um passageiro por ID

@passageiro.put("/atualizar/{id}")
async def atualizar_passageiro(id: int, passageiro: PassageiroSchema, db: Session = Depends(get_db)):
    passageiro_atualizar = db.query(PassageiroModels).filter(PassageiroModels.id_passageiro == id).first()

    if not passageiro_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O passageiro com ID {id} não foi encontrado")
    
    for key, value in passageiro.model_dump().items():
        setattr(passageiro_atualizar, key, value)
        db.commit()
        db.refresh(passageiro_atualizar)
    return passageiro_atualizar
