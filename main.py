import os
from flask import Flask, request, jsonify, render_template
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

VECTORSTORE_PATH = "vectorstore"

# Configuração do modelo OpenAI
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Configuração do Prompt
QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""Baseado no contexto abaixo, responda à pergunta a seguir de forma clara e objetiva em português.
    Se a resposta não estiver no contexto, diga coisas como "Não tenho detalhes sobre essa informação. Para saber mais, acesse nosso site www.fametro.edu.br. Você também pode buscar o atendimento presencial de segunda a sexta-feira, das 8h às 21h e sábado das 8h às 11 horas.".
    
    Contexto:
    {context}
    
    Pergunta: {question}
    Resposta:
    """
)

# Inicializar Flask
app = Flask(__name__)

# Carregar o vectorstore
def load_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        return FAISS.load_local(VECTORSTORE_PATH, HuggingFaceEmbeddings(), allow_dangerous_deserialization=True)
    else:
        raise ValueError("Vectorstore não encontrado. Execute o script 'vector_database_manager.py' para criá-lo.")

vectorstore = load_vectorstore()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    if vectorstore is None:
        return jsonify({"error": "Vectorstore não carregado."}), 500

    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Pergunta não fornecida"}), 400

    try:
        # Busca no vetorstore com scores
        results = vectorstore.similarity_search_with_score(question, k=5)

        # Filtrar resultados com score acima de 0.2
        confidence_threshold = 0.2
        docs = [doc for doc, score in results if score > confidence_threshold]

        if not docs:
            return jsonify({"answer": "Não encontrei essa informação na base de dados."})

        # Combina os chunks recuperados
        context = "\n\n".join([doc.page_content for doc in docs])

        # Gerar resposta usando o LLM
        chain = LLMChain(llm=llm, prompt=QA_PROMPT)
        response = chain.run({"context": context, "question": question})
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": f"Erro ao processar pergunta: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
