from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

#===== DEFINIR MODELO DE EMBEDING =====#
def definir_modelo_embeding(embedding_model_name):
    print(f"Definiendo modelo de embeding: {embedding_model_name}")
    return HuggingFaceEmbeddings(model_name=embedding_model_name)

#===== INICIALIZAR DB VECTORIAL =====#
def inicializar_db_vectorial(embedding, qdrant_client_path, collection_name):
    client = QdrantClient(path=qdrant_client_path)

    if not client.collection_exists(collection_name):
        vector_size= len(embedding.embed_query("aaaaaaa"))
        
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
        print("Base de datos vectorial creada.")
    else:
        print("Base de datos vectorial cargada.")

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding
    )

    return client, vectorstore

#===== INSERTAR DOCUMENTOS =====#
def insertar_documentos_qdrant(vectorstore, document):
    vectorstore.add_documents(document)
    print("Documentos insertados en la base de datos vectorial.")

#===== ELIMINAR DOCUMENTOS =====#
def eliminar_documentos_qdrant(client, file_name, collection_name):
    client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source",
                        match=models.MatchValue(value=file_name)
                    )
                ]
            )
        )
    )
    print("Documentos eliminados de la base de datos vectorial.")
