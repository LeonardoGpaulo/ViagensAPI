from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pagamento import PagamentoModels
from app.schema.pagamento import PagamentoSchema

pagamento = APIRouter() 

##----------------------------------------------------------------------------##

# Criar um novo pagamento

@pagamento.post("/")
def criar_pagamento(pagamento: PagamentoSchema, db: Session = Depends(get_db)):
    novo_pagamento = PagamentoModels(**pagamento.model_dump())
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)
    return novo_pagamento

##----------------------------------------------------------------------------##

# Listar todos os pagamentos

@pagamento.get("/listar")
def listar_pagamentos(db: Session = Depends(get_db)):
    return db.query(PagamentoModels).all()

##----------------------------------------------------------------------------##

# Deletar um pagamento por ID

@pagamento.delete("/deletar/{id}")
def deletar_pagamento(id: int, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoModels).filter(PagamentoModels.id_pagamentos == id).first()

    if not pagamento:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O pagamento com ID {id} não foi encontrado")
    
    db.delete(pagamento)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um pagamento por ID

@pagamento.put("/atualizar/{id}")
def atualizar_pagamento(id: int, dados: PagamentoSchema, db: Session = Depends(get_db)):
    pagamento_atualizar = db.query(PagamentoModels).filter(PagamentoModels.id_pagamentos == id).first()

    # Verificar se o pagamento existe
    if not pagamento_atualizar:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O pagamento com ID {id} não foi encontrado")

    for key, value in dados.model_dump().items():
        setattr(pagamento_atualizar, key, value)

    db.commit()
    db.refresh(pagamento_atualizar)
    return pagamento_atualizar
