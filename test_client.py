import requests
import json

# URL del endpoint
url = "http://127.0.0.1:8003/check-document"

# Datos de prueba con formato incorrecto (falta información requerida)
data_invalid = {
    "body": {
        # Falta "transactionId"
        "dni": "12345678A",
        # Faltan campos en clientData
        "clientData": {
        },
        # Faltan campos en deviceInfo
        "deviceInfo": {
            "browser": "Chrome"
        },
        # Estructura incorrecta en resultJSON
        "resultJSON": {
            # Falta estructura correcta
        }
    }
}

# Datos de prueba con formato correcto
data_valid = {
    "body": {
        "transactionId": "test123",
        "dni": "12345678A",
        "clientData": {
            "customerId": "customer001"
        },
        "deviceInfo": {
            "osVersion": "Windows 10",
            "model": "PC",
            "brand": "Generic",
            "browser": "Chrome",
            "osName": "Windows"
        },
        "resultJSON": {
            "DocumentData": {
                "serviceTransactionId": "trans001",
                "serviceDocument": {
                    "CHECKS": {
                        "checkPassed": True
                    },
                    "FRONTSIDE": {
                        "FIELD_DATA": {
                            "GIVEN_NAMES": "Juan",
                            "SURNAME": ["Pérez", "García"],
                            "NATIONALITY_CODE": "ESP"
                        }
                    }
                }
            }
        }
    }
}

# Probar con datos inválidos para reproducir el error 422
print("===== PRUEBA CON DATOS INVÁLIDOS =====")
print("Enviando solicitud a:", url)
print("Datos:", json.dumps(data_invalid, indent=2))

try:
    response = requests.post(url, json=data_invalid)
    
    # Imprimir respuesta
    print("\nEstado de respuesta:", response.status_code)
    print("Encabezados:", response.headers)
    
    if response.status_code == 422:
        print("\nError de validación (422):")
        print(json.dumps(response.json(), indent=2))
    else:
        print("\nRespuesta:")
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error al hacer la solicitud:", str(e))

# Probar con datos válidos
print("\n\n===== PRUEBA CON DATOS VÁLIDOS =====")
print("Enviando solicitud a:", url)
print("Datos:", json.dumps(data_valid, indent=2))

try:
    response = requests.post(url, json=data_valid)
    
    # Imprimir respuesta
    print("\nEstado de respuesta:", response.status_code)
    print("Encabezados:", response.headers)
    
    if response.status_code == 422:
        print("\nError de validación (422):")
        print(json.dumps(response.json(), indent=2))
    else:
        print("\nRespuesta:")
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error al hacer la solicitud:", str(e)) 