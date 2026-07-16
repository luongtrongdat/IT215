from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from model import DocumentCreate
from services import get_documents,create_document,delete_document

app = FastAPI(
    title="🐾✨ FÁT ÂY PI AI CỦA ĐẠT NHÓ 💓🐾"
)

@app.get("/documents")
def get_document(db: Session = Depends(get_db)):
    get_documents


@app.post("/documents")
def create_documents(document: DocumentCreate,db: Session = Depends(get_db)):
    create_document


@app.delete("/documents/{document_id}")
def delete_documents(document_id: int,db: Session = Depends(get_db)):
    delete_document