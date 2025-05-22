import requests
import json

# URL del endpoint
url = "http://127.0.0.1:8003/check-document"

# Datos extremadamente mínimos (sólo lo básico)
data_minimal = {
    "body": {
        "dni": "12345678Z"
    }
}

# Enviar la solicitud POST con los datos mínimos
print("===== PRUEBA CON DATOS MÍNIMOS =====")
print("Enviando solicitud a:", url)
print("Datos:", json.dumps(data_minimal, indent=2))

try:
    response = requests.post(url, json=data_minimal)
    
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