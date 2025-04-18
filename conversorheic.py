from pillow_heif import register_heif_opener
from PIL import Image
import os
import sys
import time
import subprocess
from tqdm import tqdm

# Configura el registro de logs
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("conversion_heic.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Función para verificar que ExifTool está instalado
def check_exiftool():
    try:
        result = subprocess.run(['exiftool', '-ver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        version = result.stdout.strip()
        logger.info(f"ExifTool encontrado: versión {version}")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.error("ExifTool no está instalado o no está en el PATH. Instálalo para preservar metadatos.")
        return False

# Función para copiar metadatos específicos (solo fechas) de HEIC a JPEG
def copy_date_metadata(input_file, output_file):
    try:
        # Copiar solo las etiquetas de fecha del archivo original al convertido
        # El parámetro -TagsFromFile indica el archivo fuente
        # Los siguientes parámetros indican qué etiquetas copiar
        cmd = ['exiftool', 
              '-TagsFromFile', input_file, 
              '-CreateDate', '-ModifyDate', '-DateTimeOriginal',
              '-overwrite_original',  # No crear archivos de backup
              output_file]
        
        # Ejecutar ExifTool
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Verificar si se ejecutó correctamente
        if process.returncode == 0:
            return True
        else:
            logger.error(f"Error al copiar metadatos: {process.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error al ejecutar ExifTool: {str(e)}")
        return False

# Registra el soporte para .heic
logger.info("Iniciando el proceso de conversion HEIC a JPEG")
try:
    register_heif_opener()
    logger.info("Soporte HEIC registrado correctamente")
except Exception as e:
    logger.error(f"Error al registrar soporte HEIC: {e}")
    sys.exit(1)

# Verificar que ExifTool está disponible
has_exiftool = check_exiftool()
if not has_exiftool:
    logger.warning("La preservación de metadatos estará desactivada")

# Carpeta con los archivos HEIC
input_folder = "Diciembre"
output_folder = "122024Diciembre"
quality = 90
max_errors = 3  # Número máximo de errores consecutivos

# Verificar que la carpeta de entrada existe
if not os.path.exists(input_folder):
    logger.error(f"La carpeta de entrada '{input_folder}' no existe")
    sys.exit(1)

# Crear carpeta de salida si no existe
try:
    os.makedirs(output_folder, exist_ok=True)
    logger.info(f"Carpeta de salida '{output_folder}' preparada")
except Exception as e:
    logger.error(f"Error al crear la carpeta de salida '{output_folder}': {e}")
    sys.exit(1)

# Obtener la lista de archivos HEIC
heic_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.heic', '.HEIC'))]
total_files = len(heic_files)

if total_files == 0:
    logger.warning(f"No se encontraron archivos HEIC en '{input_folder}'")
    sys.exit(0)

logger.info(f"Se encontraron {total_files} archivos HEIC para convertir")

# Contadores para seguimiento
converted = 0
errors = 0
consecutive_errors = 0
metadata_preserved = 0

# Procesar archivos con barra de progreso
for filename in tqdm(heic_files, desc="Convirtiendo archivos", unit="imagen"):
    input_path = os.path.join(input_folder, filename)
    # Manejo seguro de nombres de archivo
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_folder, base_name + ".jpg")
    
    logger.info(f"Procesando: {filename}")
    
    try:
        # Intentar abrir y convertir la imagen
        start_time = time.time()
        with Image.open(input_path) as img:
            img.save(output_path, "JPEG", quality=quality)
        
        # Verificar si el archivo se creó correctamente
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            conversion_time = time.time() - start_time
            converted += 1
            
            # Aplicar metadatos de fecha si ExifTool está disponible
            if has_exiftool:
                if copy_date_metadata(input_path, output_path):
                    metadata_preserved += 1
                    logger.info(f"Metadatos de fecha preservados para: {filename}")
                else:
                    logger.warning(f"No se pudieron preservar metadatos para: {filename}")
            
            consecutive_errors = 0  # Resetear contador de errores consecutivos
            logger.info(f"OK: Convertido: {filename} -> {os.path.basename(output_path)} ({conversion_time:.2f}s)")
        else:
            errors += 1
            consecutive_errors += 1
            logger.error(f"ERROR: El archivo {output_path} no se creo correctamente")
            
    except Exception as e:
        errors += 1
        consecutive_errors += 1
        logger.error(f"ERROR al convertir {filename}: {str(e)}")
        
        # Mostrar información detallada sobre el archivo que causó el error
        try:
            file_size = os.path.getsize(input_path)
            logger.error(f"Detalles del archivo problematico: Tamaño={file_size} bytes")
        except Exception as file_error:
            logger.error(f"No se pudo obtener información del archivo: {str(file_error)}")
    
    # Verificar si hay demasiados errores consecutivos
    if consecutive_errors >= max_errors:
        logger.critical(f"Se detiene la ejecucion despues de {consecutive_errors} errores consecutivos")
        break

# Resumen final
success_rate = (converted / total_files) * 100 if total_files > 0 else 0
metadata_rate = (metadata_preserved / converted) * 100 if converted > 0 else 0

logger.info(f"Proceso finalizado. Estadisticas:")
logger.info(f"  - Total de archivos: {total_files}")
logger.info(f"  - Convertidos con exito: {converted} ({success_rate:.1f}%)")
logger.info(f"  - Con metadatos preservados: {metadata_preserved} ({metadata_rate:.1f}%)")
logger.info(f"  - Errores: {errors}")

if errors > 0:
    sys.exit(1)
else:
    logger.info("Conversion completada exitosamente")
    sys.exit(0)