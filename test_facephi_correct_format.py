#!/usr/bin/env python3
"""
Script para probar la API de Facephi con el formato correcto (tokens)
"""

import requests
import json
from datetime import datetime

def test_facephi_correct_format():
    """Probar Facephi API con el formato correcto usando tokens"""
    
    print("🔍 PROBANDO FACEPHI API - FORMATO CORRECTO")
    print("=" * 60)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuración
    base_url = "https://api.identity-platform.io"
    endpoint = "/services/extractDocumentDataWeb"
    api_key = "kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU"
    
    # Headers correctos
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Datos de prueba con formato correcto
    test_data = {
        "tokenFrontDocument": "test_token_front_123",
        "tokenBackDocument": "test_token_back_123", 
        "countryCode": "ESP",
        "decompose": False,
        "tracking": {
            "extraData": "test_extra_data",
            "operationId": "test_operation_123"
        }
    }
    
    print(f"🔧 Configuración:")
    print(f"   URL: {base_url}{endpoint}")
    print(f"   API Key: {api_key[:10]}...")
    print(f"   Headers: {headers}")
    print()
    
    print(f"📋 Datos de prueba:")
    print(json.dumps(test_data, indent=2))
    print()
    
    try:
        print("🔄 Enviando petición...")
        
        response = requests.post(
            f"{base_url}{endpoint}",
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        print(f"📊 Resultado:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            print("✅ ¡ÉXITO!")
            try:
                result = response.json()
                print("📄 Respuesta JSON:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except:
                print(f"📄 Respuesta (texto): {response.text}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Mensaje: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()
    print("=" * 60)
    print("🔍 PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_facephi_correct_format()
