def buscar_documentos(prompt, vectorstore):
    retriever= vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    retrieve_documents= retriever.invoke(prompt)
    return retrieve_documents
