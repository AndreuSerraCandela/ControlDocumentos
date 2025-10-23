from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import json
import logging
from datetime import datetime

# Configurar logging
import os
log_file = os.path.join(os.getcwd(), 'document_logs.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Document Check API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Debug print
    print("=" * 80)
    print("🔍 DEBUG BACKEND: Documento recibido")
    print("=" * 80)
    print(f"📋 DNI: {doc_dict.get('dni', 'N/A')}")
    print(f"🆔 Transaction ID: {doc_dict.get('transactionId', 'N/A')}")
    print(f"📱 Device Info: {doc_dict.get('deviceInfo', {})}")
    print(f"🔑 Client Data: {doc_dict.get('clientData', {})}")
    
    # Debug del resultJSON
    result_json = doc_dict.get('resultJSON', {})
    print(f"📄 ResultJSON keys: {list(result_json.keys()) if result_json else 'None'}")
    
    if 'DocumentData' in result_json:
        doc_data = result_json['DocumentData']
        print(f"📄 DocumentData keys: {list(doc_data.keys()) if doc_data else 'None'}")
        
        if 'serviceDocument' in doc_data:
            service_doc = doc_data['serviceDocument']
            print(f"📄 ServiceDocument keys: {list(service_doc.keys()) if service_doc else 'None'}")
            
            if 'FRONTSIDE' in service_doc:
                frontside = service_doc['FRONTSIDE']
                print(f"📄 FRONTSIDE keys: {list(frontside.keys()) if frontside else 'None'}")
                
                if 'FIELD_DATA' in frontside:
                    field_data = frontside['FIELD_DATA']
                    print(f"📄 FIELD_DATA keys: {list(field_data.keys()) if field_data else 'None'}")
                    print(f"📄 PERSONAL_NUMBER: {field_data.get('PERSONAL_NUMBER', 'N/A')}")
                    print(f"📄 GIVEN_NAMES: {field_data.get('GIVEN_NAMES', 'N/A')}")
                    print(f"📄 SURNAME: {field_data.get('SURNAME', 'N/A')}")
    
    print("=" * 80)

    # Log document capture details
    logger.info("=" * 80)
    logger.info("📄 NUEVO DOCUMENTO CAPTURADO")
    logger.info("=" * 80)
    logger.info(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🆔 Transaction ID: {doc_dict.get('transactionId', 'N/A')}")
    logger.info(f"📋 DNI: {doc_dict.get('dni', 'N/A')}")
    
    # Extract and log personal information
    try:
        frontside = doc_dict.get("resultJSON", {}).get("DocumentData", {}).get("serviceDocument", {}).get("FRONTSIDE", {}).get("FIELD_DATA", {})
        backside = doc_dict.get("resultJSON", {}).get("DocumentData", {}).get("serviceDocument", {}).get("BACKSIDE", {}).get("MRZ_DATA", {})
        
        logger.info("👤 INFORMACIÓN PERSONAL:")
        logger.info(f"   Nombre: {frontside.get('GIVEN_NAMES', backside.get('NAME', 'N/A'))}")
        logger.info(f"   Apellidos: {frontside.get('SURNAME', [backside.get('SURNAME', 'N/A')])}")
        logger.info(f"   Nacionalidad: {frontside.get('NATIONALITY_CODE', backside.get('NATIONALITY', 'N/A'))}")
        logger.info(f"   Sexo: {frontside.get('SEX', backside.get('SEX', 'N/A'))}")
        logger.info(f"   Fecha de nacimiento: {frontside.get('DATE_OF_BIRTH', backside.get('BIRTH_DATE', 'N/A'))}")
        logger.info(f"   Fecha de expiración: {frontside.get('DATE_OF_EXPIRY', backside.get('EXPIRATION_DATE', 'N/A'))}")
        logger.info(f"   Número de documento: {frontside.get('DOCUMENT_NUMBER', backside.get('IDENTITY_NUMBER', 'N/A'))}")
        
        # Log address if available
        address = backside.get('ADDRESS', [])
        if address:
            logger.info(f"   Dirección: {', '.join(address)}")
            
    except Exception as e:
        logger.error(f"❌ Error extrayendo información personal: {e}")
    
    # Log validation checks
    try:
        checks = doc_dict.get("resultJSON", {}).get("DocumentData", {}).get("serviceDocument", {}).get("CHECKS", {})
        if checks:
            logger.info("✅ VALIDACIONES DEL DOCUMENTO:")
            valid_checks = sum(1 for v in checks.values() if v)
            total_checks = len(checks)
            logger.info(f"   Validaciones pasadas: {valid_checks}/{total_checks}")
            
            # Log specific important checks
            important_checks = [
                "PERSONAL_NUMBER_SIDE_MATCH",
                "SEX_SIDE_MATCH", 
                "FRONTSIDE_EXPIRATION_DATE_VALID",
                "FULLNAME_SIDE_MATCH",
                "NATIONALITY_CODE_SIDE_MATCH"
            ]
            
            for check in important_checks:
                if check in checks:
                    status = "✅" if checks[check] else "❌"
                    logger.info(f"   {status} {check}: {checks[check]}")
                    
    except Exception as e:
        logger.error(f"❌ Error procesando validaciones: {e}")
    
    # Log device information
    try:
        device_info = doc_dict.get("deviceInfo", {})
        logger.info("📱 INFORMACIÓN DEL DISPOSITIVO:")
        logger.info(f"   OS: {device_info.get('osName', 'N/A')} {device_info.get('osVersion', 'N/A')}")
        logger.info(f"   Navegador: {device_info.get('browser', 'N/A')}")
        logger.info(f"   Modelo: {device_info.get('model', 'N/A')}")
        logger.info(f"   Marca: {device_info.get('brand', 'N/A')}")
    except Exception as e:
        logger.error(f"❌ Error procesando información del dispositivo: {e}")
    
    # Check if the document already exists
    logger.info("🔍 VERIFICANDO DUPLICADOS...")
    for existing_doc in documents:
        if existing_doc["dni"] == doc_dict["dni"]:
            logger.warning(f"⚠️  DOCUMENTO DUPLICADO DETECTADO - DNI: {doc_dict['dni']}")
            logger.info("=" * 80)
            return {"exists": True, "message": "Document already exists in the list"}
    
    # If not found, add it to the list
    documents.append(doc_dict)
    logger.info(f"✅ DOCUMENTO AGREGADO EXITOSAMENTE - Total documentos: {len(documents)}")
    logger.info("=" * 80)
    
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
    uvicorn.run(app, host="127.0.0.1", port=8001)
