#!/usr/bin/env python3
"""
Script para crear una imagen de prueba para Postman
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_document_image():
    """Crear una imagen de documento de prueba"""
    
    # Crear imagen blanca
    width, height = 800, 500
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Intentar usar una fuente del sistema
    try:
        # Windows
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        try:
            # Linux/Mac
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            # Fuente por defecto
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Dibujar borde
    draw.rectangle([10, 10, width-10, height-10], outline='black', width=3)
    
    # Título
    draw.text((50, 50), "DOCUMENTO DE PRUEBA", fill='black', font=font_large)
    
    # Línea separadora
    draw.line([(50, 90), (width-50, 90)], fill='black', width=2)
    
    # Información del documento
    y_pos = 120
    line_height = 35
    
    info_lines = [
        "NOMBRE: JUAN CARLOS",
        "APELLIDOS: GARCIA LOPEZ", 
        "DNI: 12345678A",
        "NACIONALIDAD: ESPAÑA",
        "FECHA NACIMIENTO: 15/03/1985",
        "FECHA EXPIRACION: 15/03/2030",
        "SEXO: M",
        "NUMERO DOCUMENTO: 12345678A"
    ]
    
    for line in info_lines:
        draw.text((50, y_pos), line, fill='black', font=font_medium)
        y_pos += line_height
    
    # Línea separadora
    draw.line([(50, y_pos + 10), (width-50, y_pos + 10)], fill='black', width=2)
    
    # Texto adicional
    draw.text((50, y_pos + 30), "Este es un documento de prueba para testing", fill='gray', font=font_small)
    draw.text((50, y_pos + 50), "de la API de Facephi", fill='gray', font=font_small)
    
    # Guardar imagen
    output_path = "test_document.jpg"
    image.save(output_path, "JPEG", quality=95)
    
    print(f"✅ Imagen de prueba creada: {output_path}")
    print(f"📏 Dimensiones: {width}x{height} píxeles")
    print(f"📁 Ruta completa: {os.path.abspath(output_path)}")
    
    return output_path

if __name__ == "__main__":
    create_test_document_image()
