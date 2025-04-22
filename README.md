# Document Check API

This is a simple FastAPI application that allows you to check if a document exists in a list and add it if it doesn't.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

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