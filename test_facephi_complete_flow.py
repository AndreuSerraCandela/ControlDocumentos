#!/usr/bin/env python3
"""
Script para probar el flujo completo de Facephi:
1. documentValidation/v2/start (subir imágenes)
2. extractDocumentDataWeb (procesar con tokens)
"""

import requests
import json
import base64
import os
from datetime import datetime

def test_facephi_complete_flow():
    """Probar el flujo completo de Facephi"""
    
    print("🔍 PROBANDO FLUJO COMPLETO DE FACEPHI")
    print("=" * 60)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuración
    base_url = "https://api.identity-platform.io"
    api_key = "kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU"
    
    # Headers comunes
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Verificar que existe la imagen de prueba
    image_path = "test_document.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Error: No se encuentra la imagen {image_path}")
        print("   Ejecuta primero: python create_test_image.py")
        return
    
    print(f"📁 Imagen de prueba: {image_path}")
    print(f"📏 Tamaño: {os.path.getsize(image_path)} bytes")
    print()
    
    try:
        # PASO 1: Leer y codificar la imagen en base64
        print("🔄 PASO 1: Codificando imagen en base64...")
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        print(f"   ✅ Imagen codificada: {len(image_base64)} caracteres")
        print()
        
        # PASO 2: Llamar a documentValidation/v2/start
        print("🔄 PASO 2: Llamando a documentValidation/v2/start...")
        
        start_data = {
            "country": "ESP",
            "idType": "DNI",
            "documentRawImageMimeType": "image/jpeg",
            "documentFrontRawImage": image_base64,
            "documentBackRawImage": image_base64,  # Usar la misma imagen para ambas caras
            "merchantIdScanReference": f"scan_ref_{int(datetime.now().timestamp())}"
        }
        
        print(f"   📋 Datos de start:")
        print(f"      Country: {start_data['country']}")
        print(f"      ID Type: {start_data['idType']}")
        print(f"      MIME Type: {start_data['documentRawImageMimeType']}")
        print(f"      Scan Reference: {start_data['merchantIdScanReference']}")
        print(f"      Image size: {len(image_base64)} chars")
        print()
        
        start_response = requests.post(
            f"{base_url}/verify/documentValidation/v2/start",
            headers=headers,
            json=start_data,
            timeout=30
        )
        
        print(f"   📊 Respuesta de start:")
        print(f"      Status: {start_response.status_code}")
        print(f"      Headers: {dict(start_response.headers)}")
        
        if start_response.status_code == 200:
            start_result = start_response.json()
            print(f"   ✅ ¡ÉXITO en start!")
            print(f"   📄 Respuesta JSON:")
            print(json.dumps(start_result, indent=2, ensure_ascii=False))
            
            # Extraer tokens de la respuesta
            if 'serviceDocument' in start_result:
                service_doc = start_result['serviceDocument']
                token_front = service_doc.get('FRONTSIDE', {}).get('TOKEN')
                token_back = service_doc.get('BACKSIDE', {}).get('TOKEN')
                
                print(f"   🔑 Tokens extraídos:")
                print(f"      Front Token: {token_front}")
                print(f"      Back Token: {token_back}")
                print()
                
                # PASO 3: Llamar a extractDocumentDataWeb con los tokens
                if token_front and token_back:
                    print("🔄 PASO 3: Llamando a extractDocumentDataWeb...")
                    
                    extract_data = {
                        "tokenFrontDocument": token_front,
                        "tokenBackDocument": token_back,
                        "countryCode": "ESP",
                        "decompose": False,
                        "tracking": {
                            "extraData": "complete_flow_test",
                            "operationId": f"op_{int(datetime.now().timestamp())}"
                        }
                    }
                    
                    print(f"   📋 Datos de extract:")
                    print(f"      Front Token: {token_front[:20]}...")
                    print(f"      Back Token: {token_back[:20]}...")
                    print(f"      Country Code: {extract_data['countryCode']}")
                    print()
                    
                    extract_response = requests.post(
                        f"{base_url}/services/extractDocumentDataWeb",
                        headers=headers,
                        json=extract_data,
                        timeout=30
                    )
                    
                    print(f"   📊 Respuesta de extract:")
                    print(f"      Status: {extract_response.status_code}")
                    
                    if extract_response.status_code == 200:
                        extract_result = extract_response.json()
                        print(f"   ✅ ¡ÉXITO en extract!")
                        print(f"   📄 Respuesta JSON:")
                        print(json.dumps(extract_result, indent=2, ensure_ascii=False))
                    else:
                        print(f"   ❌ Error en extract: {extract_response.status_code}")
                        print(f"   📄 Mensaje: {extract_response.text}")
                else:
                    print("   ❌ No se pudieron extraer los tokens de la respuesta")
            else:
                print("   ❌ No se encontró 'serviceDocument' en la respuesta")
        else:
            print(f"   ❌ Error en start: {start_response.status_code}")
            print(f"   📄 Mensaje: {start_response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()
    print("=" * 60)
    print("🔍 PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_facephi_complete_flow()
