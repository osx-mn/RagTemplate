from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def _procesar_pdf(documents_folder, file_name):
    loader = PyPDFLoader(f"{documents_folder}/{file_name}")
    document = loader.load()
    return document

def procesar_pdf(documents_folder, file_name, strict_type=None):
    print("Procesando PDF: ", file_name, " de tipo ", strict_type)
    if strict_type:
        exact_type= file_name.split(".")[-1]
        print("Tipo exacto: ", exact_type)
        if exact_type != strict_type:
            return
        return _procesar_pdf(documents_folder, file_name)
    else:
        return _procesar_pdf(documents_folder, file_name)

def divir_documento_en_chunks(document, file_name):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=True,
    )   
    
    chunks = text_splitter.split_documents(document)
    #agregar metadata a cada chunk
    for i, chunk in enumerate(chunks):
        chunk.metadata['chunk_number'] = i + 1
        chunk.metadata['source'] = file_name

    return chunks
