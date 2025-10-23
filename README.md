# Document Check System

Sistema completo para escanear y gestionar documentos utilizando tecnología Facephi. Incluye una API backend en Python (FastAPI) y un frontend React con integración del SDK de Facephi.

## Arquitectura del Sistema

### Backend API (Python/FastAPI)
- API REST para gestión de documentos
- Validación y almacenamiento de datos
- Integración con Facephi SDK
- Endpoints para búsqueda y filtrado

### Frontend (React)
- Interfaz web moderna y responsive
- Escaneo de documentos con cámara
- Visualización de resultados
- Integración completa con Facephi SDK

## Setup Rápido

### Opción 1: Script Automático
```bash
# Windows
start-dev.bat

# Linux/Mac
./start-dev.sh
```

### Opción 2: Manual

#### Backend
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar API:
```bash
python main.py
```

#### Frontend
1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Ejecutar aplicación:
```bash
npm start
```

### URLs de Acceso
- **API Backend**: http://localhost:8000
- **Frontend React**: http://localhost:3000
- **Documentación API**: http://localhost:8000/docs

## API Endpoints

### Check Document
- **URL**: `/check-document`
- **Method**: POST
- **Description**: Checks if a document exists in the list and adds it if it doesn't
- **Request Body**: JSON document with the specified format
- **Response**: 
  ```json
  {
    "exists": true/false,
    "message": "Document already exists in the list" or "Document added to the list"
  }
  ```

### Get Documents
- **URL**: `/documents`
- **Method**: GET
- **Description**: Returns all documents in the list
- **Response**: List of all documents

### Search Documents
- **URL**: `/documents/search`
- **Method**: GET
- **Description**: Search documents by nationality and/or DNI
- **Query Parameters**:
  - `nationality`: (optional) Filter by nationality code (e.g., "ESP")
  - `dni`: (optional) Filter by DNI
- **Response**: 
  ```json
  {
    "documents": [
      {
        "dni": "10873694F",
        "name": "INES",
        "surname": "ALVAREZ ALVAREZ",
        "nationality": "ESP"
      }
    ]
  }
  ```

### Get Documents with Face
- **URL**: `/documents/with-face`
- **Method**: GET
- **Description**: Search documents by nationality and/or DNI including face image
- **Query Parameters**:
  - `nationality`: (optional) Filter by nationality code (e.g., "ESP")
  - `dni`: (optional) Filter by DNI
- **Response**: 
  ```json
  {
    "documents": [
      {
        "dni": "10873694F",
        "name": "INES",
        "surname": "ALVAREZ ALVAREZ",
        "nationality": "ESP",
        "face": "base64_encoded_face_image"
      }
    ]
  }
  ```

### Load Documents
- **URL**: `/documents/load`
- **Method**: POST
- **Description**: Load documents directly from JSON
- **Request Body**:
  ```json
  {
    "documents": {
      "transactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
      "dni": "10873694F",
      "clientData": {
        "customerId": "ec39c357-b56d-41aa-8524-73ac270f0ed3"
      },
      "deviceInfo": {
        "osVersion": "18.3.1",
        "model": "18.3.1",
        "brand": "Mobile Safari",
        "browser": "Mobile Safari",
        "osName": "iOS"
      },
      "resultJSON": {
        "DocumentData": {
          "serviceTransactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
          "serviceDocument": {
            // ... document data ...
          }
        }
      }
    }
  }
  ```
  O para cargar múltiples documentos:
  ```json
  {
    "documents": [
      {
        "transactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
        "dni": "10873694F",
        // ... resto del documento ...
      },
      {
        "transactionId": "otro-id",
        "dni": "otro-dni",
        // ... otro documento ...
      }
    ]
  }
  ```
- **Response**: 
  ```json
  {
    "message": "Successfully loaded documents",
    "count": 2
  }
  ```

## Example Usage

To check a document:
```bash
curl -X POST "http://localhost:8000/check-document" \
     -H "Content-Type: application/json" \
     -d '{
           "transactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
           "dni": "10873694F",
           "clientData": {
             "customerId": "ec39c357-b56d-41aa-8524-73ac270f0ed3"
           },
           "deviceInfo": {
             "osVersion": "18.3.1",
             "model": "18.3.1",
             "brand": "Mobile Safari",
             "browser": "Mobile Safari",
             "osName": "iOS"
           },
           "resultJSON": {
             "DocumentData": {
               "serviceTransactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
               "serviceDocument": {
                 // ... document data ...
               }
             }
           }
         }'
```

To search documents by nationality:
```bash
curl "http://localhost:8000/documents/search?nationality=ESP"
```

To search documents by DNI:
```bash
curl "http://localhost:8000/documents/search?dni=10873694F"
```

To get documents with face images:
```bash
curl "http://localhost:8000/documents/with-face?nationality=ESP"
```

To load documents:
```bash
curl -X POST "http://localhost:8000/documents/load" \
     -H "Content-Type: application/json" \
     -d '{
           "documents": {
             "transactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
             "dni": "10873694F",
             "clientData": {
               "customerId": "ec39c357-b56d-41aa-8524-73ac270f0ed3"
             },
             "deviceInfo": {
               "osVersion": "18.3.1",
               "model": "18.3.1",
               "brand": "Mobile Safari",
               "browser": "Mobile Safari",
               "osName": "iOS"
             },
             "resultJSON": {
               "DocumentData": {
                 "serviceTransactionId": "52550355-27ef-4562-a9e2-072706d2baf3",
                 "serviceDocument": {
                   // ... document data ...
                 }
               }
             }
           }
         }'
```

## Frontend React

### Características del Frontend

- **📱 Escaneo de Documentos**: Utiliza la cámara del dispositivo para capturar documentos
- **🔍 Búsqueda Avanzada**: Filtra documentos por nacionalidad y DNI
- **👤 Visualización Facial**: Muestra imágenes faciales extraídas de los documentos
- **📊 Dashboard**: Estadísticas y gestión de documentos escaneados
- **🎨 UI Moderna**: Interfaz responsive con Styled Components

### Tecnologías Frontend

- **React 18**: Framework principal
- **Styled Components**: Estilos CSS-in-JS
- **Axios**: Cliente HTTP para API
- **Facephi SDK**: Integración con servicios de identidad
- **HTML5 Camera API**: Acceso a la cámara del dispositivo

### Configuración Facephi

El frontend está configurado con las siguientes credenciales de Facephi:

- **API Key**: `4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS`
- **Client ID**: `52f5e18b-e599-4de3-91e1-f4b0e80ff657`
- **Secret ID**: `82880bda-d8c4-448c-baf1-ecc650a3bc58`
- **Base URL**: `https://api.identity-platform.io`

### Endpoints Facephi Utilizados

- `extractDocumentDataWeb`: Extracción de datos del documento
- `documentValidation/v2/start`: Inicio del proceso de validación
- `documentValidation/v2/data`: Datos de validación del documento
- `documentValidation/v2/status`: Estado del proceso de validación
- `finishTracking`: Finalización del seguimiento

### Uso del Frontend

1. **Escanear Documento**:
   - Haz clic en "Iniciar Escaneo"
   - Permite el acceso a la cámara
   - Coloca el documento frente a la cámara
   - Captura el documento

2. **Gestionar Documentos**:
   - Ve a "Documentos Escaneados"
   - Usa los filtros de búsqueda
   - Visualiza información detallada
   - Activa/desactiva la visualización de caras

### Estructura del Proyecto Frontend

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── DocumentScanner.js    # Componente de escaneo
│   │   └── DocumentResults.js    # Componente de resultados
│   ├── services/
│   │   └── api.js               # Servicios de API
│   ├── config/
│   │   └── facephi.js           # Configuración Facephi
│   ├── App.js                   # Componente principal
│   └── index.js                 # Punto de entrada
├── package.json
└── README.md
```

Para más detalles sobre el frontend, consulta [frontend/README.md](frontend/README.md). 