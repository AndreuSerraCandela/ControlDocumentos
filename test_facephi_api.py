#!/usr/bin/env python3
"""
Script para probar la API de Facephi directamente
"""

import requests
import base64
import json

def test_facephi_api():
    """Prueba la API de Facephi con una imagen de prueba"""
    
    # Configuración de Facephi
    facephi_config = {
        'apiKey': 'kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU',
        'baseUrl': 'https://api.identity-platform.io',
        'clientId': '52f5e18b-e599-4de3-91e1-f4b0e80ff657',
        'secretId': '82880bda-d8c4-448c-baf1-ecc650a3bc58'
    }
    
    # Crear una imagen de prueba (1x1 pixel PNG en base64)
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    try:
        print("🔄 Probando API de Facephi...")
        print(f"URL: {facephi_config['baseUrl']}/services/extractDocumentDataWeb")
        print(f"API Key: {facephi_config['apiKey'][:10]}...")
        
        # Convertir base64 a bytes
        image_data = base64.b64decode(test_image_base64)
        
        # Preparar headers de autenticación (solo API Key)
        headers = {
            'X-API-Key': facephi_config['apiKey']
        }
        
        # Preparar datos para la petición (solo API Key)
        files = {
            'image': ('test.png', image_data, 'image/png')
        }
        
        data = {
            'apiKey': facephi_config['apiKey']
        }
        
        # Probar diferentes endpoints
        endpoints = [
            "/services/extractDocumentDataWeb",
            "/verify/documentValidation/v2/start",
            "/verify/documentValidation/v2/data"
        ]
        
        for endpoint in endpoints:
            print(f"\n🔄 Probando endpoint: {endpoint}")
            
            # Realizar petición
            response = requests.post(
                f"{facephi_config['baseUrl']}{endpoint}",
                files=files,
                data=data,
                headers=headers,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Endpoint funcionando!")
                try:
                    result = response.json()
                    print("📄 Respuesta JSON:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print(f"Contenido: {response.text[:500]}...")
                break
            else:
                print(f"❌ Error: {response.status_code} - {response.text[:200]}")
        
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_facephi_api()
