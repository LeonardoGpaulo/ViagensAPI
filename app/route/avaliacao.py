from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import avaliacao
from app.models.avaliacao import AvaliacaoModels
from app.schema.avaliacao import AvaliacaoSchema

Avaliacao = APIRouter()


