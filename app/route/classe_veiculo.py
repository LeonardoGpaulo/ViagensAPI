from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.classe_veiculo import ClasseVeiculoModels
from app.schema.classe_veiculo import ClasseVeiculoSchema

classe_veiculo = APIRouter()


##----------------------------------------------------------------------------##

## Criar uma nova classe

@classe_veiculo.post("/")
async def criar_classe_veiculo(dados: ClasseVeiculoSchema, db: Session = Depends(get_db)):
    novaClasse = ClasseVeiculoModels(**dados.model_dump())
    db.add(novaClasse)
    db.commit()
    db.refresh(novaClasse)
    return novaClasse

##----------------------------------------------------------------------------##

## Listar todas as classes

@classe_veiculo.get("/listar")
async def listar_classe_veiculo(db: Session = Depends(get_db)):
    return db.query(ClasseVeiculoModels).all()

##----------------------------------------------------------------------------##

## Deletar uma classe por ID

@classe_veiculo.delete("/deletar/{id}")
async def deletar_classe_veiculo(id:int, db: Session = Depends(get_db)):
    id = db.query(ClasseVeiculoModels).filter(ClasseVeiculoModels.id_classe_veiculo == id).first()

    if not id:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A classe com ID {id} não foi encontrada")
    
    db.delete(id)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

## Atualizar uma classe por ID

@classe_veiculo.put("/atualizar/{id}")
async def atualizar_classe_veiculo(id: int, dados: ClasseVeiculoSchema, db: Session = Depends(get_db)):
    classe_atualizar =db.query(ClasseVeiculoModels).filter(ClasseVeiculoModels.id_classe_veiculo == id).first()

    ## Verificar se a classe existe
    if not classe_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A classe com ID {id} não foi encontrada")
    
    for key, value in dados.model_dump().items():
        setattr(classe_atualizar, key, value)

    db.commit()
    db.refresh(classe_atualizar)
    return classe_atualizar