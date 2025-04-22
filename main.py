from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union
import json

app = FastAPI(title="Document Check API")

# In-memory storage for documents (in a real application, this would be a database)
documents = []

class DeviceInfo(BaseModel):
    osVersion: str
    model: str
    brand: str
    browser: str
    osName: str

class ClientData(BaseModel):
    customerId: str

class DocumentData(BaseModel):
    serviceTransactionId: str
    serviceDocument: dict

class ResultJSON(BaseModel):
    DocumentData: DocumentData

class DocumentRequest(BaseModel):
    transactionId: str
    dni: str
    clientData: ClientData
    deviceInfo: DeviceInfo
    resultJSON: ResultJSON

class LoadDocumentsRequest(BaseModel):
    documents: Union[DocumentRequest, List[DocumentRequest]]

def extract_name_from_document(doc: dict) -> dict:
    """Extract name and surname from document data"""
    try:
        frontside = doc["resultJSON"]["DocumentData"]["serviceDocument"]["FRONTSIDE"]["FIELD_DATA"]
        name = frontside.get("GIVEN_NAMES", "")
        surname = " ".join(frontside.get("SURNAME", []))
        nationality = frontside.get("NATIONALITY_CODE", "")
        return {
            "name": name,
            "surname": surname,
            "nationality": nationality
        }
    except:
        return {
            "name": "",
            "surname": "",
            "nationality": ""
        }

def extract_face_from_document(doc: dict) -> str:
    """Extract face image from document data"""
    try:
        return doc["resultJSON"]["DocumentData"]["serviceDocument"]["DECOMPOSED"]["FACE"]
    except:
        return ""

@app.post("/check-document")
async def check_document(document: DocumentRequest):
    """
    Check if a document exists in the list and add it if it doesn't.
    Returns True if the document was added, False if it already existed.
    """
    # Convert the document to a dictionary for comparison
    doc_dict = document.dict()
    
    # Check if the document already exists
    for existing_doc in documents:
        if existing_doc["dni"] == doc_dict["dni"]:
            return {"exists": True, "message": "Document already exists in the list"}
    
    # If not found, add it to the list
    documents.append(doc_dict)
    return {"exists": False, "message": "Document added to the list"}

@app.get("/documents")
async def get_documents():
    """
    Get all documents in the list
    """
    return {"documents": documents}

@app.get("/documents/search")
async def search_documents(nationality: Optional[str] = None, dni: Optional[str] = None):
    """
    Search documents by nationality and/or DNI
    Returns a list of documents with name and surname
    """
    filtered_docs = documents
    
    if nationality:
        filtered_docs = [doc for doc in filtered_docs 
                        if doc["resultJSON"]["DocumentData"]["serviceDocument"]["FRONTSIDE"]["FIELD_DATA"].get("NATIONALITY_CODE") == nationality]
    
    if dni:
        filtered_docs = [doc for doc in filtered_docs if doc["dni"] == dni]
    
    result = []
    for doc in filtered_docs:
        name_info = extract_name_from_document(doc)
        result.append({
            "dni": doc["dni"],
            "name": name_info["name"],
            "surname": name_info["surname"],
            "nationality": name_info["nationality"]
        })
    
    return {"documents": result}

@app.get("/documents/with-face")
async def get_documents_with_face(nationality: Optional[str] = None, dni: Optional[str] = None):
    """
    Search documents by nationality and/or DNI including face image
    """
    filtered_docs = documents
    
    if nationality:
        filtered_docs = [doc for doc in filtered_docs 
                        if doc["resultJSON"]["DocumentData"]["serviceDocument"]["FRONTSIDE"]["FIELD_DATA"].get("NATIONALITY_CODE") == nationality]
    
    if dni:
        filtered_docs = [doc for doc in filtered_docs if doc["dni"] == dni]
    
    result = []
    for doc in filtered_docs:
        name_info = extract_name_from_document(doc)
        face = extract_face_from_document(doc)
        result.append({
            "dni": doc["dni"],
            "name": name_info["name"],
            "surname": name_info["surname"],
            "nationality": name_info["nationality"],
            "face": face
        })
    
    return {"documents": result}

@app.post("/documents/load")
async def load_documents(request: LoadDocumentsRequest):
    """
    Load documents directly from JSON
    """
    try:
        if isinstance(request.documents, list):
            documents.extend([doc.dict() for doc in request.documents])
        else:
            documents.append(request.documents.dict())
        return {"message": "Successfully loaded documents", "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 