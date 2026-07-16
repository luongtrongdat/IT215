from fastapi import  HTTPException
from model import DocumentCreate,DocumentModel

def get_documents(db):
    documents = db.query(DocumentModel).all()

    return {
        "message": "Get documents successfully",
        "data": documents
    }


def create_document(document: DocumentCreate,db):
    new_document = DocumentModel(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Document created successfully",
        "data": new_document
    }


def delete_document(document_id: int,db):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }