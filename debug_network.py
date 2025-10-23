#!/usr/bin/env python3
"""
Script para debuggear las peticiones de red del sistema
"""

import requests
import json
import time
from datetime import datetime

def debug_facephi_api():
    """Debug de la API de Facephi"""
    print("🔍 DEBUG: Probando API de Facephi...")
    
    # Configuración
    facephi_config = {
        'apiKey': '4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS',
        'baseUrl': 'https://api.identity-platform.io',
        'clientId': '52f5e18b-e599-4de3-91e1-f4b0e80ff657',
        'secretId': '82880bda-d8c4-448c-baf1-ecc650a3bc58'
    }
    
    # Crear imagen de prueba
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    image_data = test_image_base64.encode('utf-8')
    
    # Probar diferentes formatos de autenticación
    auth_methods = [
        {
            'name': 'API Key en Header',
            'headers': {'X-API-Key': facephi_config['apiKey']},
            'data': {'clientId': facephi_config['clientId'], 'secretId': facephi_config['secretId']}
        },
        {
            'name': 'API Key en Body',
            'headers': {},
            'data': {
                'apiKey': facephi_config['apiKey'],
                'clientId': facephi_config['clientId'],
                'secretId': facephi_config['secretId']
            }
        },
        {
            'name': 'Authorization Bearer',
            'headers': {'Authorization': f'Bearer {facephi_config["apiKey"]}'},
            'data': {'clientId': facephi_config['clientId'], 'secretId': facephi_config['secretId']}
        }
    ]
    
    for method in auth_methods:
        print(f"\n🔄 Probando: {method['name']}")
        
        try:
            files = {'image': ('test.png', image_data, 'image/png')}
            
            response = requests.post(
                f"{facephi_config['baseUrl']}/services/extractDocumentDataWeb",
                files=files,
                data=method['data'],
                headers=method['headers'],
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("   ✅ ¡Éxito!")
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def debug_backend_api():
    """Debug de la API del backend"""
    print("\n🔍 DEBUG: Probando API del backend...")
    
    base_url = "http://localhost:8001"
    
    # Probar endpoints
    endpoints = [
        ("GET", "/documents", "Listar documentos"),
        ("GET", "/documents/search", "Buscar documentos"),
        ("GET", "/docs", "Documentación API")
    ]
    
    for method, endpoint, description in endpoints:
        try:
            print(f"\n🔄 {description}: {method} {endpoint}")
            
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=5)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ ¡Éxito!")
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def debug_mock_document():
    """Debug con documento simulado"""
    print("\n🔍 DEBUG: Probando con documento simulado...")
    
    base_url = "http://localhost:8001"
    
    # Crear documento simulado
    mock_document = {
        "transactionId": "debug-test-123",
        "dni": "DEBUG123456",
        "clientData": {
            "customerId": "debug-customer-123"
        },
        "deviceInfo": {
            "osVersion": "Debug Test",
            "model": "Debug Browser",
            "brand": "Debug",
            "browser": "Debug Browser",
            "osName": "Debug OS"
        },
        "resultJSON": {
            "DocumentData": {
                "serviceTransactionId": "debug-transaction-123",
                "serviceDocument": {
                    "FRONTSIDE": {
                        "FIELD_DATA": {
                            "PERSONAL_NUMBER": "DEBUG123456",
                            "GIVEN_NAMES": "DEBUG",
                            "SURNAME": "TEST",
                            "NATIONALITY_CODE": "ESP",
                            "SEX": "M",
                            "DATE_OF_BIRTH": "01/01/1990",
                            "DATE_OF_EXPIRY": "01/01/2030",
                            "DOCUMENT_NUMBER": "DEBUG123456"
                        }
                    },
                    "CHECKS": {
                        "PERSONAL_NUMBER_SIDE_MATCH": True,
                        "SEX_SIDE_MATCH": True,
                        "FRONTSIDE_EXPIRATION_DATE_VALID": True,
                        "FULLNAME_SIDE_MATCH": True,
                        "NATIONALITY_CODE_SIDE_MATCH": True
                    }
                }
            }
        }
    }
    
    try:
        print("🔄 Enviando documento simulado...")
        response = requests.post(
            f"{base_url}/check-document",
            json=mock_document,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ ¡Éxito!")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    print("🔍 SISTEMA DE DEBUG COMPLETO")
    print("=" * 50)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Debug de Facephi
    debug_facephi_api()
    
    # Debug del backend
    debug_backend_api()
    
    # Debug con documento simulado
    debug_mock_document()
    
    print("\n" + "=" * 50)
    print("🔍 DEBUG COMPLETADO")
