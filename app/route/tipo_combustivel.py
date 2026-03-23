from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tipo_combustivel import TipoCombustivelModels
from app.schema.tipo_combustivel import TipoCombustivelSchema

tipo_combustivel = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo serviço

@tipo_combustivel.post("/")
async def criar_tipo_combustivel(tipo_combustivel: TipoCombustivelSchema, db: Session = Depends(get_db)):
    novo_tipo_combustivel = TipoCombustivelModels(**tipo_combustivel.model_dump())
    db.add(novo_tipo_combustivel)
    db.commit()
    db.refresh(novo_tipo_combustivel)
    return  novo_tipo_combustivel

##----------------------------------------------------------------------------##

# Listar todos os serviços

@tipo_combustivel.get("/listar")
async def listar_tipo_combustivel(db: Session = Depends(get_db)):
    return db.query(TipoCombustivelModels).all()

##----------------------------------------------------------------------------##

# Deletar um serviço por ID

@tipo_combustivel.delete("/deletar/{id}")
async def deletar_tipo_combustivel(id: int, db: Session = Depends(get_db)):
    tipo_combustivel = db.query(TipoCombustivelModels).filter(TipoCombustivelModels.id_tipo_combustivel == id).first()

    if not tipo_combustivel:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O serviço com ID {id} não foi encontrado")
    
    db.delete(tipo_combustivel)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um serviço por ID

@tipo_combustivel.put("/atualizar/{id}")
async def atualizar_tipo_combustivel(id: int, tipo_combustivel: TipoCombustivelSchema, db: Session = Depends(get_db)):
    tipo_combustivel_atualizar = db.query(TipoCombustivelModels).filter(TipoCombustivelModels.id_tipo_combustivel == id).first()

    if not tipo_combustivel_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O tipo combustivel com ID {id} não foi encontrado")
    
    for key, value in tipo_combustivel.model_dump().items():
        setattr(tipo_combustivel_atualizar, key, value)
        db.commit()
        db.refresh(tipo_combustivel_atualizar)
        return tipo_combustivel_atualizar
