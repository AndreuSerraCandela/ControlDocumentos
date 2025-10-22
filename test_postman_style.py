#!/usr/bin/env python3
"""
Script que simula exactamente las llamadas de Postman a Facephi API
"""

import requests
import os
from datetime import datetime

def test_facephi_postman_style():
    """Probar Facephi API exactamente como Postman"""
    
    print("🔍 PROBANDO FACEPHI API - ESTILO POSTMAN")
    print("=" * 60)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuración
    base_url = "https://api.identity-platform.io"
    endpoint = "/services/extractDocumentDataWeb"
    api_key = "kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU"
    client_id = "52f5e18b-e599-4de3-91e1-f4b0e80ff657"
    secret_id = "82880bda-d8c4-448c-baf1-ecc650a3bc58"
    
    # Verificar que existe la imagen de prueba
    image_path = "test_document.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Error: No se encuentra la imagen {image_path}")
        print("   Ejecuta primero: python create_test_image.py")
        return
    
    print(f"📁 Imagen de prueba: {image_path}")
    print(f"📏 Tamaño: {os.path.getsize(image_path)} bytes")
    print()
    
    # Probar diferentes configuraciones
    test_configs = [
        {
            "name": "1. Solo API Key en Header",
            "headers": {"X-API-Key": api_key},
            "data": {},
            "files": {"image": open(image_path, "rb")}
        },
        {
            "name": "2. API Key en Header + Body",
            "headers": {"X-API-Key": api_key},
            "data": {"apiKey": api_key},
            "files": {"image": open(image_path, "rb")}
        },
        {
            "name": "3. Todas las credenciales",
            "headers": {"X-API-Key": api_key},
            "data": {
                "apiKey": api_key,
                "clientId": client_id,
                "secretId": secret_id
            },
            "files": {"image": open(image_path, "rb")}
        },
        {
            "name": "4. Sin Header, solo Body",
            "headers": {},
            "data": {
                "apiKey": api_key,
                "clientId": client_id,
                "secretId": secret_id
            },
            "files": {"image": open(image_path, "rb")}
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"🔄 {config['name']}")
        print("-" * 40)
        
        try:
            # Mostrar configuración
            print(f"   Headers: {config['headers']}")
            print(f"   Data: {config['data']}")
            print(f"   Files: image")
            
            # Realizar petición
            response = requests.post(
                f"{base_url}{endpoint}",
                headers=config['headers'],
                data=config['data'],
                files=config['files'],
                timeout=30
            )
            
            # Mostrar resultado
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("   ✅ ¡ÉXITO!")
                try:
                    result = response.json()
                    print(f"   Response: {result}")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print()
        
        # Cerrar el archivo si está abierto
        if 'files' in config and 'image' in config['files']:
            config['files']['image'].close()
    
    print("=" * 60)
    print("🔍 PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_facephi_postman_style()
