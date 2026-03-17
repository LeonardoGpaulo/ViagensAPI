from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.avaliacao import AvaliacaoModels
from app.schema.avaliacao import AvaliacaoSchema

avaliacao = APIRouter() 

#-------------------------------------------------------------------------------

## Criar uma nova avaliação

@avaliacao.post("/")
async def criar_avaliacao(dados: AvaliacaoSchema, db: Session = Depends(get_db)):
    nova_avaliacao = AvaliacaoModels(**dados.model_dump())
    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)
    return nova_avaliacao

#--------------------------------------------------------------------------------

## Listar todas as avaliações

@avaliacao.get("/listar")
async def listar_avaliacoes(db: Session = Depends(get_db)):
    return db.query(AvaliacaoModels).all()


#--------------------------------------------------------------------------------

## Deletar uma avaliação por ID

@avaliacao.delete("/deletar/{id}")
async def deletar_series(id:int, db: Session = Depends(get_db)):
    id = db.query(AvaliacaoModels).filter(AvaliacaoModels.id_avaliacao == id).first()

    if not id:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A avaliação com ID {id} não foi encontrada")
    
    db.delete(id)
    db.commit()
    return("deletado")

#--------------------------------------------------------------------------------

## Atualizar uma avaliação por ID

@avaliacao.put("/atualizar/{id}")
async def atualizar_avaliacao(id: int, dados: AvaliacaoSchema, db: Session = Depends(get_db)):
    avaliacao_atualizar = db.query(AvaliacaoModels).filter(AvaliacaoModels.id_avaliacao == id).first()

    ## Verificar se a avaliação existe
    if not avaliacao_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A avaliação com ID {id} não foi encontrada")
    
    #atualizar pro banco de dados
    for key, value in dados.model_dump().items():
        setattr(avaliacao_atualizar, key, value)

    #lançar a atualização no banco de dados
    db.commit()
    db.refresh(avaliacao_atualizar)
    return avaliacao_atualizar

#--------------------------------------------------------------------------------