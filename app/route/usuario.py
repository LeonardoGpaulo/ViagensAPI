from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import UsuarioModels
from app.schema.usuario import UsuarioSchema

usuario = APIRouter()

##----------------------------------------------------------------------------##

# Criar um novo usuário

@usuario.post("/")
async def criar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    novo_usuario = UsuarioModels(**usuario.model_dump())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

##----------------------------------------------------------------------------##

# Listar todos os usuários

@usuario.get("/listar")
async def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModels).all()

##----------------------------------------------------------------------------##

# Deletar um usuário por ID

@usuario.delete("/deletar/{id}")
async def deletar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModels).filter(UsuarioModels.id_usuario == id).first()

    if not usuario:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O usuário com ID {id} não foi encontrado")
    
    db.delete(usuario)
    db.commit()
    return("deletado")

##----------------------------------------------------------------------------##

# Atualizar um usuário por ID

@usuario.put("/atualizar/{id}")
async def atualizar_usuario(id: int, usuario: UsuarioSchema, db: Session = Depends(get_db)):
    atualizar_usuario = db.query(UsuarioModels).filter(UsuarioModels.id_usuario == id).first()
    if not atualizar_usuario:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"O usuário com ID {id} não foi encontrado")
    
    for key, value in usuario.model_dump().items():
        setattr(atualizar_usuario, key, value)
        db.commit()
        db.refresh(atualizar_usuario)
        return atualizar_usuario

