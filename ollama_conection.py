from langchain_ollama import ChatOllama

def chat(ask):
    #Configurar el modelo
    llm = ChatOllama(
        model="gemma3:4b",
        temperature=0
    )

    response= llm.invoke(ask)
    return response.content