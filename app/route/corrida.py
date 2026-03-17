from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.corrida import CorridaModels
from app.schema.corrida import CorridaSchema

corrida = APIRouter()

##----------------------------------------------------------------------------##

# Criar uma nova corrida

@corrida.post("/")
async def criar_corrida(dados: CorridaSchema, db: Session = Depends(get_db)):
    nova_corrida = CorridaModels(**dados.model_dump())
    db.add(nova_corrida)
    db.commit()
    db.refresh(nova_corrida)
    return nova_corrida

##----------------------------------------------------------------------------##

# Listar todas as corridas

@corrida.get("/listar")
async def listar_corrida(db: Session = Depends(get_db)):
    return db.query(CorridaModels).all()

##----------------------------------------------------------------------------##

# Deletar uma corrida por ID

@corrida.delete("/deletar/{id}")
async def deletar_corrida(id:int, db: Session = Depends(get_db)):
    id = db.query(CorridaModels).filter(CorridaModels.id_corrida == id).first()

    if not id:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A corrida com ID {id} não foi encontrada")
    
    db.delete(id)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar uma corrida por ID

@corrida.put("/atualizar/{id}")
async def atualizar_corrida(id: int, dados: CorridaSchema, db: Session = Depends(get_db)):
    corrida_atualizar =db.query(CorridaModels).filter(CorridaModels.id_corrida == id).first()

    ## Verificar se a corrida existe
    if not corrida_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A corrida com ID {id} não foi encontrada")
    
    for key, value in dados.model_dump().items():
        setattr(corrida_atualizar, key, value)
        db.commit()
        db.refresh(corrida_atualizar)
    return corrida_atualizar