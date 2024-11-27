import os
import pdfplumber
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.schema import Document

VECTORSTORE_PATH = "vectorstore"
PDF_DIRECTORY = "pdfs"

class VectorDatabaseManager:
    def __init__(self):
        self.vectorstore = None
        self.embeddings = HuggingFaceEmbeddings()

    def load_vectorstore(self):
        """Carrega o vetorstore do disco, se disponível."""
        if os.path.exists(VECTORSTORE_PATH):
            self.vectorstore = FAISS.load_local(VECTORSTORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
            print("Vetorstore carregado do disco.")
        else:
            print("Nenhum vetorstore salvo encontrado. Um novo será criado.")

    def save_vectorstore(self):
        """Salva o vetorstore no disco."""
        if self.vectorstore:
            self.vectorstore.save_local(VECTORSTORE_PATH)
            print("Vetorstore salvo no disco.")

    def process_pdf(self, pdf_path):
        """Processa um PDF e retorna uma lista de documentos."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text

            if not text.strip():
                print(f"Arquivo {os.path.basename(pdf_path)} não contém texto extraível. Pulando...")
                return []

            splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
            chunks = splitter.split_text(text)
            return [Document(page_content=chunk) for chunk in chunks]
        except Exception as e:
            print(f"Erro ao processar o arquivo {pdf_path}: {str(e)}")
            return []

    def process_all_pdfs(self):
        """Processa todos os PDFs da pasta e cria/atualiza o índice."""
        all_documents = []
        for filename in os.listdir(PDF_DIRECTORY):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(PDF_DIRECTORY, filename)
                print(f"Processando o arquivo: {filename}")
                documents = self.process_pdf(pdf_path)
                all_documents.extend(documents)

        if all_documents:
            if self.vectorstore:
                self.vectorstore.add_documents(all_documents)
            else:
                self.vectorstore = FAISS.from_documents(all_documents, self.embeddings)
            print("Todos os PDFs foram processados e o índice foi atualizado.")
        else:
            print("Nenhum documento válido encontrado nos PDFs.")

    def add_new_pdf(self, pdf_path):
        """Adiciona um único PDF ao vetorstore."""
        documents = self.process_pdf(pdf_path)
        if documents:
            if self.vectorstore:
                self.vectorstore.add_documents(documents)
            else:
                self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            print(f"Novo arquivo {os.path.basename(pdf_path)} adicionado com sucesso.")
        else:
            print(f"Arquivo {os.path.basename(pdf_path)} não contém dados úteis.")

if __name__ == "__main__":
    manager = VectorDatabaseManager()
    manager.load_vectorstore()
    manager.process_all_pdfs()
    manager.save_vectorstore()