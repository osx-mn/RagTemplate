import os
from tinydb import TinyDB, Query

# Configuración de DB y Carpeta
db = TinyDB("documents_process.json")
Document = Query()

def inicializar_sistema(documents_folder):
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        print(f"Carpeta '{documents_folder}' creada.")

def detectar_cambios_en_archivos(documents_folder):
    #===== Obtener lista de archivos reales en la carpeta =====#
    archivos_en_disco = os.listdir(documents_folder)
    
    queue = []

    #===== determinar si un archivo ha sido eliminado =====#
    archivos_en_db = db.all()
    archivos_en_db = [archivo['nombre']+archivo['tipo'] for archivo in archivos_en_db]

    for archivo in archivos_en_db:
        ruta_archivo= os.path.join(documents_folder, archivo)
        if not os.path.isfile(ruta_archivo):
            nombre, extension= archivo.split(".")
            queue.append({
                "nombre": nombre,
                "tipo": "."+extension,
                "estado": "delete"
            })
            
            db.remove(Document.nombre == nombre)
            print(f"Archivo eliminado de la base de datos: {archivo}")

    #===== determinar si un nuevo archivo ha sido agregado =====#
    for nombre_archivo in archivos_en_disco:

        nombre, extension = os.path.splitext(nombre_archivo)
        
        if not db.contains((Document.nombre == nombre) & (Document.tipo == extension)):
            queue.append({
                "nombre": nombre,
                "tipo": extension,
                "estado": "insert"
            })
            
            db.insert({"nombre": nombre, "tipo": extension})
            print(f"Nuevo archivo detectado y registrado: {nombre_archivo}")
    
    #===== imprimir cambios detectados =====#
    if queue:
        print("\nCambios detectados:")
        for cambio in queue:
            print(f"Estado: {cambio['estado']}, Archivo: {cambio['nombre'] + cambio['tipo']}")
    else:
        print("No se detectaron cambios en los archivos.")
    
    return queue