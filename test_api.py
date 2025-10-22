import requests
import json

def test_api():
    base_url = "http://localhost:8001"
    
    print("🧪 Probando la API del sistema de documentos...")
    print("=" * 50)
    
    # Test 1: Obtener todos los documentos
    print("1. Probando GET /documents...")
    try:
        response = requests.get(f"{base_url}/documents")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Buscar documentos
    print("2. Probando GET /documents/search...")
    try:
        response = requests.get(f"{base_url}/documents/search")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Probar con un documento de ejemplo
    print("3. Probando POST /check-document...")
    test_document = {
        "transactionId": "test-123-456-789",
        "dni": "12345678A",
        "clientData": {
            "customerId": "customer-123"
        },
        "deviceInfo": {
            "osVersion": "Windows 10",
            "model": "PC",
            "brand": "Chrome",
            "browser": "Chrome",
            "osName": "Windows"
        },
        "resultJSON": {
            "DocumentData": {
                "serviceTransactionId": "test-123-456-789",
                "serviceDocument": {
                    "CHECKS": {
                        "PERSONAL_NUMBER_SIDE_MATCH": True,
                        "SEX_SIDE_MATCH": True,
                        "BACKSIDE_AGE_IS_ADULT": True,
                        "BACKSIDE_EXPIRATION_DATE_VALID": True,
                        "BACKSIDE_PERSONAL_NUMBER_CHECK_DIGIT_VALID": True,
                        "DATE_OF_BIRTH_SIDE_MATCH": True,
                        "DATE_OF_EXPIRY_SIDE_MATCH": True,
                        "FRONTSIDE_AGE_IS_ADULT": True,
                        "FRONTSIDE_EXPIRATION_DATE_VALID": True,
                        "FRONTSIDE_PERSONAL_NUMBER_CHECK_DIGIT_VALID": True,
                        "FULLNAME_SIDE_MATCH": True,
                        "MRZ_CHECK_DIGIT_DOB": "1",
                        "MRZ_CHECK_DIGIT_DOB_IS_VALID": True,
                        "MRZ_CHECK_DIGIT_DOCUMENT_NUMBER": "4",
                        "MRZ_CHECK_DIGIT_DOCUMENT_NUMBER_IS_VALID": True,
                        "MRZ_CHECK_DIGIT_EXPIRY": "5",
                        "MRZ_CHECK_DIGIT_EXPIRY_IS_VALID": True,
                        "MRZ_CHECK_DIGIT_FINALCHECK": "1",
                        "MRZ_CHECK_DIGIT_FINALCHECK_IS_VALID": True,
                        "NATIONALITY_CODE_SIDE_MATCH": True
                    },
                    "FRONTSIDE": {
                        "FIELD_DATA": {
                            "PERSONAL_NUMBER": "12345678A",
                            "SEX": "M",
                            "SURNAME": ["GARCIA", "LOPEZ"],
                            "CARD_ACCESS_NUMBER": "123456",
                            "DATE_OF_BIRTH": "01/01/1990",
                            "DATE_OF_EXPIRY": "01/01/2030",
                            "DOCUMENT_NUMBER": "ABC123456",
                            "FIRST_SURNAME": "GARCIA",
                            "GIVEN_NAMES": "JUAN",
                            "NATIONALITY_CODE": "ESP",
                            "SECOND_SURNAME": "LOPEZ"
                        }
                    },
                    "BACKSIDE": {
                        "FIELD_DATA": {
                            "ADDRESS": ["C. PRUEBA 123", "MADRID", "MADRID"],
                            "AUTHORITY_CODE": "12345L6D2",
                            "E_ID_PLACE_OF_BIRTH_CITY": ["MADRID", "MADRID"],
                            "PARENTS_GIVEN_NAMES": "PADRE MADRE"
                        },
                        "MRZ_DATA": {
                            "BIRTH_DATE": "01/01/1990",
                            "EXPIRATION_DATE": "01/01/2030",
                            "IDENTITY_NUMBER": "ABC123456",
                            "ISSUING_COUNTRY": "ESP",
                            "NAME": "JUAN",
                            "NATIONALITY": "ESP",
                            "PERSONAL_NUMBER": "12345678A",
                            "SEX": "M",
                            "SURNAME": "GARCIA LOPEZ"
                        }
                    },
                    "DECOMPOSED": {
                        "FACE": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA6QDpAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAFdARoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDtIg8d3JCVCh/mXI6VHFHv822nYMVyV+hqW9KNDFdbixQ5OPTvSzJsuIbiNQEb5WJ9DXi+0Z7nsolaKHzrF1WP95HkZPt0qSXznsY51YLsOSB7dasCMw32HkGyUdvWnW0MW+a2JJU/MPx60/aMPZRIboSLJBdrLlTww9jUhE1vqSEsGjmXHPYii2gjktpbVmOUJA5/Km3D/wDEsEhYl4j+ORT52Hs0OgLxX91rMhKSLv"
                    }
                }
            }
        }
    }
    
    try:
        response = requests.post(f"{base_url}/check-document", json=test_document)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    print("✅ Pruebas completadas!")

if __name__ == "__main__":
    test_api()
