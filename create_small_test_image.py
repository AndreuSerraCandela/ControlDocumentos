#!/usr/bin/env python3
"""
Script para crear una imagen de prueba más pequeña para Facephi
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_small_test_document_image():
    """Crear una imagen de documento de prueba más pequeña"""
    
    # Crear imagen más pequeña
    width, height = 400, 250
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Intentar usar una fuente del sistema
    try:
        # Windows
        font_large = ImageFont.truetype("arial.ttf", 16)
        font_medium = ImageFont.truetype("arial.ttf", 12)
        font_small = ImageFont.truetype("arial.ttf", 10)
    except:
        try:
            # Linux/Mac
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            # Fuente por defecto
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Dibujar borde
    draw.rectangle([5, 5, width-5, height-5], outline='black', width=2)
    
    # Título
    draw.text((20, 20), "DNI TEST", fill='black', font=font_large)
    
    # Línea separadora
    draw.line([(20, 45), (width-20, 45)], fill='black', width=1)
    
    # Información del documento (más compacta)
    y_pos = 60
    line_height = 20
    
    info_lines = [
        "NOMBRE: JUAN CARLOS",
        "APELLIDOS: GARCIA LOPEZ", 
        "DNI: 12345678A",
        "NACIONALIDAD: ESPAÑA",
        "FECHA NAC: 15/03/1985",
        "FECHA EXP: 15/03/2030",
        "SEXO: M"
    ]
    
    for line in info_lines:
        draw.text((20, y_pos), line, fill='black', font=font_medium)
        y_pos += line_height
    
    # Línea separadora
    draw.line([(20, y_pos + 5), (width-20, y_pos + 5)], fill='black', width=1)
    
    # Texto adicional
    draw.text((20, y_pos + 15), "Documento de prueba Facephi", fill='gray', font=font_small)
    
    # Guardar imagen
    output_path = "test_document_small.jpg"
    image.save(output_path, "JPEG", quality=85, optimize=True)
    
    print(f"✅ Imagen pequeña creada: {output_path}")
    print(f"📏 Dimensiones: {width}x{height} píxeles")
    print(f"📁 Ruta completa: {os.path.abspath(output_path)}")
    print(f"📊 Tamaño del archivo: {os.path.getsize(output_path)} bytes")
    
    return output_path

if __name__ == "__main__":
    create_small_test_document_image()
