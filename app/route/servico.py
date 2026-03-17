from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.servico import ServicoModels
from app.schema.servico import ServicoSchema

servico = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo serviço

@servico.post("/")
async def criar_servico(servico: ServicoSchema, db: Session = Depends(get_db)):
    novo_servico = ServicoModels(**servico.model_dump())
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return novo_servico

##----------------------------------------------------------------------------##

# Listar todos os serviços

@servico.get("/listar")
async def listar_servicos(db: Session = Depends(get_db)):
    return db.query(ServicoModels).all()

##----------------------------------------------------------------------------##

# Deletar um serviço por ID

@servico.delete("/deletar/{id}")
async def deletar_servico(id: int, db: Session = Depends(get_db)):
    servico = db.query(ServicoModels).filter(ServicoModels.id_servico == id).first()

    if not servico:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O serviço com ID {id} não foi encontrado")
    
    db.delete(servico)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um serviço por ID

@servico.put("/atualizar/{id}")
async def atualizar_servico(id: int, servico: ServicoSchema, db: Session = Depends(get_db)):
    servico_atualizar = db.query(ServicoModels).filter(ServicoModels.id_servico == id).first()

    if not servico_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O serviço com ID {id} não foi encontrado")
    
    for key, value in servico.model_dump().items():
        setattr(servico_atualizar, key, value)
        db.commit()
        db.refresh(servico_atualizar)



