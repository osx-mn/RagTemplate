import tomllib
import gestionar_archivos
import procesar_documentos
import db_vectorial
import ollama_connection
import buscar_documentos

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

#===== CONFIGURACIONES =====#

EMBEDDING_MODEL_NAME = config["models"]["embedding_model"]
DOCUMENTS_FOLDER = config["paths"]["documents_folder"]
QDRANT_CLIENT_PATH = config["paths"]["qdrant_client_path"]
QDRANT_COLLECTION_NAME = config["paths"]["qdrant_collection_name"]
PROMPT_INSTRUCTIONS= config["struct_prompts"]["cordial"]
LLM_MODEL_NAME= config["models"]["llm_model"]

client, vectorstore = None, None

#===== INICIO =====#
gestionar_archivos.inicializar_sistema(DOCUMENTS_FOLDER)
archivos= gestionar_archivos.detectar_cambios_en_archivos(DOCUMENTS_FOLDER)
print("QUEUE:",archivos)

if archivos:
    for archivo in archivos:
        if archivo["estado"] == "insert":
            file_name = archivo["nombre"]+archivo["tipo"]
            pages = procesar_documentos.procesar_pdf(
                documents_folder=DOCUMENTS_FOLDER,
                file_name=file_name,
                strict_type="pdf"
                )
            
            chunk = procesar_documentos.divir_documento_en_chunks(pages, file_name)
            
            embedding = db_vectorial.definir_modelo_embeding(EMBEDDING_MODEL_NAME)
            
            [client, vectorstore] = db_vectorial.inicializar_db_vectorial(
                embedding,
                QDRANT_CLIENT_PATH,
                QDRANT_COLLECTION_NAME
            )

            db_vectorial.insertar_documentos_qdrant(vectorstore, chunk)

        
        if archivo["estado"] == "delete" and client:    
            file_name = archivo["nombre"]+archivo["tipo"]
            db_vectorial.eliminar_documentos_qdrant(client, file_name, QDRANT_COLLECTION_NAME)   

#===== PROCESO TEMPORAL DE VALIDACIÓN RAG =====#

prompt= input("Ingrese su pregunta: ")

embedding = db_vectorial.definir_modelo_embeding(EMBEDDING_MODEL_NAME)

client, vectorstore = db_vectorial.inicializar_db_vectorial(
    embedding,
    QDRANT_CLIENT_PATH,
    QDRANT_COLLECTION_NAME
)

documents= buscar_documentos.buscar_documentos(prompt, vectorstore)

response= ollama_connection.chat(PROMPT_INSTRUCTIONS+" "+prompt+" - ".join(str(doc) for doc in documents), LLM_MODEL_NAME)
print(response)

if client:
    client.close()