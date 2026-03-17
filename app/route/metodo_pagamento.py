from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.metodo_pagamento import MetodoPagamentoModels
from app.schema.metodo_pagamento import MetodoPagamentoSchema

metodo_pagamento = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo método de pagamento

@metodo_pagamento.post("/")
async def criar_metodo_pagamento(metodo_pagamento: MetodoPagamentoSchema, db: Session = Depends(get_db)):
    novo_metodo_pagamento = MetodoPagamentoModels(**metodo_pagamento.model_dump())
    db.add(novo_metodo_pagamento)
    db.commit()
    db.refresh(novo_metodo_pagamento)
    return novo_metodo_pagamento

##----------------------------------------------------------------------------##

# Listar todos os métodos de pagamento

@metodo_pagamento.get("/listar")
async def listar_metodos_pagamento(db: Session = Depends(get_db)):
    return db.query(MetodoPagamentoModels).all()

##----------------------------------------------------------------------------##

# Deletar um método de pagamento por ID

@metodo_pagamento.delete("/deletar/{id}")
async def deletar_metodo_pagamento(id: int, db: Session = Depends(get_db)):
    metodo_pagamento = db.query(MetodoPagamentoModels).filter(MetodoPagamentoModels.id_metodo_pagamento == id).first()

    if not metodo_pagamento:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O método de pagamento com ID {id} não foi encontrado")
    
    db.delete(metodo_pagamento)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um método de pagamento por ID

@metodo_pagamento.put("/atualizar/{id}")
async def atualizar_metodo_pagamento(id: int, metodo_pagamento: MetodoPagamentoSchema, db: Session = Depends(get_db)):
    metodo_pagamento_atualizar = db.query(MetodoPagamentoModels).filter(MetodoPagamentoModels.id_metodo_pagamento == id).first()

    if not metodo_pagamento_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O método de pagamento com ID {id} não foi encontrado")
    
    for key, value in metodo_pagamento.model_dump().items():
        setattr(metodo_pagamento_atualizar, key, value)
        db.commit()
        db.refresh(metodo_pagamento_atualizar)
    return metodo_pagamento_atualizar


