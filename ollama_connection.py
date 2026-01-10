from langchain_ollama import ChatOllama

def chat(ask, model_name):
    #Configurar el modelo
    llm = ChatOllama(
        model=model_name,
        temperature=0
    )

    response= llm.invoke(ask)
    return response.content