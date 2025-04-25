from PIL import Image
import os

def convert_png_to_webp(input_folder, output_folder):
    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Obtener lista de archivos PNG
    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    total_files = len(png_files)
    
    print(f"Encontrados {total_files} archivos PNG para convertir")
    
    # Contador de archivos procesados
    converted = 0
    
    # Procesar cada archivo
    for filename in png_files:
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + '.webp'
        output_path = os.path.join(output_folder, output_filename)
        
        # Abrir y convertir la imagen
        img = Image.open(input_path)
        img.save(output_path, 'WEBP', lossless=True, quality=90)
        
        # Actualizar contador y mostrar progreso
        converted += 1
        progress = (converted / total_files) * 100
        print(f'[{converted}/{total_files}] ({progress:.1f}%) Convertido: {filename} -> {output_filename}')
    
    print(f"\nConversión completada: {converted} de {total_files} archivos convertidos a WebP")

# Ejemplo de uso
convert_png_to_webp('./avatars', './avatars_webp')