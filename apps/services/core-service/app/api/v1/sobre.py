import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.tutorial import (
    ProfessorBaseSchema,
    ProfessorCreateSchema,
    SobreResponseSchema,
)
from app.services.tutorial_service import TutorialService

router = APIRouter()


@router.get("/sobre", response_model=SobreResponseSchema)
def get_sobre(db: Session = Depends(get_db)):
    service = TutorialService(db)
    return service.get_sobre_data()


@router.get("/sobre/professores/{professor_id}", response_model=ProfessorBaseSchema)
def get_professor_por_id(professor_id: uuid.UUID, db: Session = Depends(get_db)):
    service = TutorialService(db)
    prof = service.get_professor_by_id(professor_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor nao encontrado")
    return prof


@router.post("/sobre/professores", response_model=ProfessorBaseSchema, status_code=201)
def criar_professor(
    payload: ProfessorCreateSchema,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Nao autorizado: Token ausente")

    if authorization != "Bearer token-admin-master":
        raise HTTPException(
            status_code=403, detail="Acesso proibido: Permissao insuficiente"
        )

    service = TutorialService(db)
    return service.create_professor(payload)


@router.get("/debug/error")
def trigger_error():
    raise RuntimeError("Erro imprevisto de conexao com gateway ou hardware.")
