from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, RootModel, field_validator, model_validator
from typing import List, Optional, Union, Dict, Any, ForwardRef
import json
import pandas as pd
from io import BytesIO
import os
import asyncio
from collections import deque
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("api")

app = FastAPI(title="Document Check API")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
# Montar frontend simple (servirá index.html en /simple)
app.mount("/simple", StaticFiles(directory="frontend_simple", html=True), name="simple")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for documents (in a real application, this would be a database)
documents = []
# Lista de personas no permitidas
blocked_persons = []
# Cola para los resultados de verificación
verification_results = deque()

# Archivo para almacenar la lista de personas bloqueadas
BLOCKED_PERSONS_FILE = "blocked_persons.json"

def load_blocked_persons():
    """Carga la lista de personas bloqueadas desde el archivo JSON"""
    global blocked_persons
    try:
        if os.path.exists(BLOCKED_PERSONS_FILE):
            with open(BLOCKED_PERSONS_FILE, 'r', encoding='utf-8') as f:
                blocked_persons = json.load(f)
    except Exception as e:
        print(f"Error al cargar la lista de personas bloqueadas: {e}")
        blocked_persons = []

def save_blocked_persons():
    """Guarda la lista de personas bloqueadas en el archivo JSON"""
    try:
        with open(BLOCKED_PERSONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(blocked_persons, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar la lista de personas bloqueadas: {e}")

# Cargar la lista de personas bloqueadas al iniciar la aplicación
load_blocked_persons()

class DeviceInfo(BaseModel):
    osVersion: Optional[str] = ""
    model: Optional[str] = ""
    brand: Optional[str] = ""
    browser: Optional[str] = ""
    osName: Optional[str] = ""
    
    model_config = {
        "extra": "allow"  # Permite campos adicionales
    }

class ClientData(BaseModel):
    customerId: Optional[str] = ""
    
    model_config = {
        "extra": "allow"  # Permite campos adicionales
    }

class ServiceDocument(BaseModel):
    CHECKS: Optional[Dict[str, Any]] = {}
    BACKSIDE: Optional[Dict[str, Any]] = None
    FRONTSIDE: Optional[Dict[str, Any]] = {}
    
    model_config = {
        "extra": "allow"  # Permite cualquier campo adicional
    }

class DocumentData(BaseModel):
    serviceTransactionId: Optional[str] = ""
    serviceDocument: Optional[ServiceDocument] = None
    
    @field_validator('serviceDocument', mode="before")
    @classmethod
    def default_service_document(cls, v):
        if v is None:
            return ServiceDocument()
        return v
    
    model_config = {
        "extra": "allow"  # Permite cualquier campo adicional
    }

class ResultJSON(BaseModel):
    DocumentData: Optional["DocumentData"] = None
    
    @field_validator('DocumentData', mode="before")
    @classmethod
    def default_document_data(cls, v):
        if v is None:
            return DocumentData()
        return v
    
    model_config = {
        "extra": "allow"  # Permite cualquier campo adicional
    }

class DocumentRequest(BaseModel):
    transactionId: Optional[str] = ""
    dni: Optional[str] = ""
    clientData: Optional[ClientData] = None
    deviceInfo: Optional[DeviceInfo] = None
    resultJSON: Optional[ResultJSON] = None
    
    @field_validator('clientData', mode="before")
    @classmethod
    def default_client_data(cls, v):
        if v is None:
            return ClientData()
        return v
    
    @field_validator('deviceInfo', mode="before")
    @classmethod
    def default_device_info(cls, v):
        if v is None:
            return DeviceInfo()
        return v
    
    @field_validator('resultJSON', mode="before")
    @classmethod
    def default_result_json(cls, v):
        if v is None:
            return ResultJSON()
        return v
    
    model_config = {
        "extra": "allow"  # Permite cualquier campo adicional
    }

class DocumentRequestWrapper(BaseModel):
    body: Optional[DocumentRequest] = None
    
    @model_validator(mode="before")
    @classmethod
    def validate_and_fill_body(cls, data):
        if isinstance(data, dict):
            if "body" not in data or data["body"] is None:
                data["body"] = {}
        return data
    
    @field_validator('body', mode="before")
    @classmethod
    def default_body(cls, v):
        if v is None:
            return DocumentRequest()
        return v
    
    model_config = {
        "extra": "allow"  # Permite cualquier campo adicional
    }

class BlockedPerson(BaseModel):
    dni: str
    name: str
    nationality: str

class BlockedPersonsList(RootModel):
    root: List[BlockedPerson]

@app.get("/")
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/full")
async def read_full(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/facephi")
async def facephi_system(request: Request):
    """Sistema Facephi completo con frontend y backend integrados"""
    return templates.TemplateResponse("facephi.html", {"request": request})

@app.post("/upload-blocked-list")
async def upload_blocked_list(
    request: Request,
    file: Optional[UploadFile] = File(None)
):
    """
    Carga la lista de personas no permitidas desde un archivo Excel o JSON
    """
    try:
        logger.debug(f"Recibida solicitud de carga de lista bloqueada")
        
        # Ya no borramos la lista existente, solo añadimos registros
        # Cargar la lista actual para asegurarnos de tener la última versión
        load_blocked_persons()
        
        new_records = 0
        updated_records = 0
        existing_dnis = {person['dni']: i for i, person in enumerate(blocked_persons)}
        
        if file:
            logger.debug(f"Archivo recibido: {file.filename}, content_type: {file.content_type}")
            # Procesar archivo Excel
            try:
                contents = await file.read()
                logger.debug(f"Tamaño del archivo: {len(contents)} bytes")
                df = pd.read_excel(BytesIO(contents))
                logger.debug(f"DataFrame creado. Columnas encontradas: {df.columns.tolist()}")
                logger.debug(f"Número de filas: {len(df)}")
                
                # Normalizar nombres de columnas (convertir a minúscula y eliminar espacios)
                df.columns = df.columns.str.lower().str.strip()
                logger.debug(f"Columnas normalizadas: {df.columns.tolist()}")
                
                # Mapeo de posibles nombres de columnas
                column_mapping = {
                    'dni': ['dni', 'id','DNI','Dni','NIF','Nif', 'documento', 'doc', 'documento nacional de identidad', 'identificacion'],
                    'name': ['name', 'nombre', 'nombres', 'nombrecompleto', 'nombre completo', 'apellido y nombre'],
                    'nationality': ['nationality', 'nacionalidad', 'pais', 'nacion']
                }
                
                # Verificar si existen columnas compatibles
                dni_column = None
                name_column = None
                nationality_column = None
                
                for col in df.columns:
                    col_lower = col.lower().strip()
                    if col_lower in column_mapping['dni']:
                        dni_column = col
                    if col_lower in column_mapping['name']:
                        name_column = col
                    if col_lower in column_mapping['nationality']:
                        nationality_column = col
                
                if not dni_column or not name_column:
                    logger.error(f"Columnas requeridas no encontradas. Buscando: dni/DNI y name/Nombre")
                    raise HTTPException(
                        status_code=400,
                        detail=f"El archivo Excel debe contener columnas para DNI/dni y Nombre/name. Columnas encontradas: {df.columns.tolist()}"
                    )
                
                logger.debug(f"Columnas mapeadas: DNI={dni_column}, Nombre={name_column}, Nacionalidad={nationality_column}")
                
                for index, row in df.iterrows():
                    try:
                        dni_value = str(row[dni_column]).strip()
                        
                        # Crear objeto persona
                        person = {
                            "dni": dni_value,
                            "name": str(row[name_column]).strip(),
                            "nationality": str(row[nationality_column]).strip() if nationality_column else ""
                        }
                        
                        # Verificar si el DNI ya existe
                        if dni_value in existing_dnis:
                            # Actualizar registro existente
                            blocked_persons[existing_dnis[dni_value]] = person
                            updated_records += 1
                            logger.debug(f"Actualizada persona bloqueada: {person}")
                        else:
                            # Añadir nuevo registro
                            blocked_persons.append(person)
                            existing_dnis[dni_value] = len(blocked_persons) - 1
                            new_records += 1
                            logger.debug(f"Añadida nueva persona bloqueada: {person}")
                            
                    except Exception as row_error:
                        logger.error(f"Error al procesar la fila {index}: {str(row_error)}")
                        # Continuamos procesando el resto de filas
                        
                # Guardar la lista actualizada
                logger.debug(f"Guardando lista actualizada con {len(blocked_persons)} personas")
                save_blocked_persons()
                
                return {
                    "message": f"Lista actualizada correctamente. Registros nuevos: {new_records}, Actualizados: {updated_records}",
                    "total_records": len(blocked_persons),
                    "new_records": new_records,
                    "updated_records": updated_records
                }
                
            except Exception as excel_error:
                logger.error(f"Error al procesar el archivo Excel: {str(excel_error)}", exc_info=True)
                raise HTTPException(
                    status_code=400,
                    detail=f"Error al procesar el archivo Excel: {str(excel_error)}"
                )
        else:
            logger.warning("No se recibió ningún archivo")
            # Intentar procesar JSON del cuerpo de la solicitud
            try:
                body = await request.json()
                if not isinstance(body, list):
                    logger.error(f"El cuerpo no es una lista: {type(body)}")
                    raise HTTPException(
                        status_code=400,
                        detail="El JSON debe ser una lista de personas"
                    )
                
                for person in body:
                    if not all(key in person for key in ['dni', 'name', 'nationality']):
                        logger.error(f"Persona con campos faltantes: {person}")
                        raise HTTPException(
                            status_code=400,
                            detail="Cada persona en el JSON debe tener los campos dni, name y nationality"
                        )
                    blocked_persons.append({
                        "dni": str(person['dni']),
                        "name": str(person['name']),
                        "nationality": str(person['nationality'])
                    })
                    logger.debug(f"Añadida persona bloqueada desde JSON: {person}")
            except json.JSONDecodeError:
                logger.error("Error al decodificar JSON del cuerpo")
                raise HTTPException(
                    status_code=400,
                    detail="El cuerpo de la solicitud debe ser un JSON válido"
                )
        
        # Guardar la lista actualizada
        logger.debug(f"Guardando lista actualizada con {len(blocked_persons)} personas")
        save_blocked_persons()
            
        return {"message": f"Successfully loaded {len(blocked_persons)} blocked persons"}
    except HTTPException as he:
        logger.error(f"HTTPException: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar los datos: {str(e)}"
        )

@app.post("/check-document")
async def check_document(request: DocumentRequestWrapper):
    """
    Verifica si un documento está en la lista de personas no permitidas
    """
    try:
        logger.debug(f"Received document check request")
        # Convertir a diccionario para poder acceder a los campos
        doc_dict = request.model_dump()
        
        # Añadir logs para depuración
        logger.debug(f"Estructura de request.body: {request.body}")
        
        # Extraer DNI del documento o usar valor por defecto
        dni = ""
        
        # Intentar obtener el DNI de la propiedad principal
        if hasattr(request.body, "dni") and request.body.dni:
            dni = request.body.dni
            logger.debug(f"DNI extraído de la propiedad principal: {dni}")
        
        # Intentar extraer del transactionId si existe (algunas implementaciones lo usan)
        if not dni and hasattr(request.body, "transactionId") and request.body.transactionId:
            logger.debug(f"transactionId encontrado: {request.body.transactionId}")
            
        # Si el DNI está vacío, intentar extraerlo de resultJSON
        try:
            # Imprimir la estructura para depuración
            result_json_dict = {}
            if hasattr(request.body, "resultJSON") and request.body.resultJSON:
                result_json_dict = request.body.resultJSON.model_dump()
                logger.debug(f"Contenido de resultJSON: {result_json_dict}")
                
                # Primero intentar acceder a través de los atributos
                if hasattr(request.body.resultJSON, "DocumentData") and request.body.resultJSON.DocumentData:
                    if hasattr(request.body.resultJSON.DocumentData, "serviceDocument") and request.body.resultJSON.DocumentData.serviceDocument:
                        service_doc = request.body.resultJSON.DocumentData.serviceDocument
                        
                        # Verificar FRONTSIDE.MRZ_DATA.PERSONAL_NUMBER
                        if hasattr(service_doc, "FRONTSIDE"):
                            frontside = service_doc.FRONTSIDE
                            if isinstance(frontside, dict) and "MRZ_DATA" in frontside:
                                mrz_data = frontside["MRZ_DATA"]
                                if isinstance(mrz_data, dict) and "PERSONAL_NUMBER" in mrz_data:
                                    dni = mrz_data["PERSONAL_NUMBER"]
                                    logger.debug(f"DNI extraído de FRONTSIDE.MRZ_DATA.PERSONAL_NUMBER: {dni}")
            
            # Si no se encontró por el método anterior, intentar acceder directamente a través del diccionario
            if not dni and "resultJSON" in doc_dict and doc_dict["resultJSON"]:
                logger.debug("Intentando extraer DNI accediendo al diccionario doc_dict")
                result_json = doc_dict["resultJSON"]
                
                if "DocumentData" in result_json and result_json["DocumentData"]:
                    doc_data = result_json["DocumentData"]
                    
                    if "serviceDocument" in doc_data and doc_data["serviceDocument"]:
                        service_doc = doc_data["serviceDocument"]
                        
                        if "FRONTSIDE" in service_doc and service_doc["FRONTSIDE"]:
                            frontside = service_doc["FRONTSIDE"]
                            
                            if "MRZ_DATA" in frontside and frontside["MRZ_DATA"]:
                                mrz_data = frontside["MRZ_DATA"]
                                
                                if "PERSONAL_NUMBER" in mrz_data:
                                    dni = mrz_data["PERSONAL_NUMBER"]
                                    logger.debug(f"DNI extraído del diccionario doc_dict: {dni}")
        except Exception as e:
            logger.error(f"Error al extraer DNI de resultJSON: {str(e)}", exc_info=True)
        
        # Si el DNI sigue vacío, revisar los datos de depuración
        if not dni:
            # Intentar extraer de la cadena de solicitud en bruto para propósitos de depuración
            try:
                logger.debug("Buscando DNI en la representación de cadena de la solicitud")
                request_str = str(doc_dict)
                import re
                # Buscar patrones de DNI español (8 dígitos seguidos de una letra)
                dni_matches = re.findall(r'PERSONAL_NUMBER[\'"]?\s*:\s*[\'"]([0-9]{8}[A-Za-z])[\'"]', request_str)
                if dni_matches:
                    dni = dni_matches[0]
                    logger.debug(f"DNI extraído mediante expresión regular: {dni}")
            except Exception as e:
                logger.error(f"Error en extracción con regex: {str(e)}")
        
        # Si el DNI sigue vacío, devolver error
        if not dni:
            logger.warning("No se pudo obtener el DNI del documento")
            result = {
                "blocked": False,
                "message": "No se pudo obtener el DNI del documento",
                "documentData": doc_dict
            }
            verification_results.append(result)
            return result
            
        # Actualizar el DNI en el doc_dict
        if "dni" not in doc_dict or not doc_dict["dni"]:
            doc_dict["dni"] = dni
        
        # Normalizar DNI a minúsculas para comparación
        dni_normalizado = dni.lower()
        logger.debug(f"DNI normalizado para comparación: {dni_normalizado}")
        
        # Verificar si la persona está en la lista de no permitidos
        for blocked_person in blocked_persons:
            # Normalizar DNI de la persona bloqueada también
            blocked_dni = blocked_person["dni"].lower()
            logger.debug(f"Comparando con persona bloqueada: {blocked_person['name']}, DNI: {blocked_dni}")
            if blocked_dni == dni_normalizado:
                result = {
                    "blocked": True,
                    "message": "Persona no permitida",
                    "details": blocked_person,
                    "documentData": doc_dict
                }
                verification_results.append(result)
                return result
        
        # Si no está en la lista de no permitidos, se añade a la lista de documentos
        documents.append(doc_dict)
        result = {
            "blocked": False,
            "message": "Documento verificado y añadido a la lista",
            "documentData": doc_dict
        }
        verification_results.append(result)
        return result
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el documento: {str(e)}"
        )

@app.get("/check-document/stream")
async def stream_verification_results():
    """
    Stream de resultados de verificación usando Server-Sent Events
    """
    async def event_generator():
        while True:
            if verification_results:
                result = verification_results.popleft()
                yield f"data: {json.dumps(result)}\n\n"
                break
            await asyncio.sleep(0.1)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="debug") 