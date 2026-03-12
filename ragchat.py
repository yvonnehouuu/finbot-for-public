import os
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from tqdm import tqdm
from langchain.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import gradio as gr
import os
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Function to initialize conversation chain with GROQ language model
groq_api_key = os.environ['GROQ_API_KEY']


def load_documents(directory):
    documents = []
    supported_formats = ['.txt', '.pdf', '.docx']  # Add more supported file formats
    for filename in tqdm(os.listdir(directory), desc="Loading documents"):
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension in supported_formats:
            try:
                filepath = os.path.join(directory, filename)
                if file_extension == '.txt':
                    with open(filepath, 'r', encoding='utf-8') as file:
                        text = file.read()
                elif file_extension == '.pdf':
                    # Use PyPDF2 or another PDF library to read PDF files
                    # text = read_pdf(filepath)
                    pass
                elif file_extension == '.docx':
                    # Use python-docx to read DOCX files
                    # text = read_docx(filepath)
                    pass
                filename = os.path.splitext(filename)[0]
                documents.append(Document(page_content=text, metadata={"source": filename}))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Increase chunk size to include more context
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", " ", "", "    "]  # Custom separators
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vectorstore(chunks):
    print("cuda")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("hugging face")
    # Use a more advanced embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/msmarco-bert-base-dot-v5",  # A more accurate model
        model_kwargs={'device': device}
    )

    print("vec")
    # Add indexing parameters to improve retrieval efficiency
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        collection_metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    print("finish")
    return vectorstore


print("loading doc...")
documents = load_documents('./data')
print("spliting doc...")
chunks = split_documents(documents)
print("creating vec...")
vectorstore = create_vectorstore(chunks)


def main():
    print("main")


def mai():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    
    model = 'llama3-8b-8192'
    # Initialize Groq LangChain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )

    # Set up memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 20})  # 5,10

    # Modify the prompt template
    template = """你是一個在幫助使用者回答有關金融知識問題的智能助手。根據提供的檢索到的資料來回答問題。如果信息不足以回答問題，直接忽略檢索直接使用原問題回答，並且所有回答皆須以繁體中文回答，並且是基於台灣的金融市場做回答。

檢索資料信息：
{context}

聊天歷史：
{chat_history}

原始提問：{question}

請根據上述信息回答問題。請注意：

1.優先使用檢索資料信息中的內容，但也可以參考聊天歷史。
2.如果檢索資訊為無或是相關度極低，直接忽略檢索資料回答。
3.回答要簡潔明瞭，並以繁體中文表達。
4.回答時須以列點式回答，並且在答案的最開始隨機使用兩中表情符號。
回答："""

    prompt = ChatPromptTemplate.from_template(template)

    # Create ConversationalRetrievalChain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=groq_chat,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
    '''conversation = LLMChain(
        llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
        prompt=prompt,  # The constructed prompt template.
        verbose=False,  # TRUE Enables verbose output, which can be useful for debugging.
        memory=memory,  # The conversational memory object that stores and manages the conversation history.
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    response = conversation.predict(human_input=user_question)
    '''

    # Use this inside the main loop
    while True:
        user_question = input("請問您的問題：")
        if user_question:
            try:
                # Execute retrieval
                results = retriever.invoke(user_question)
                
                print('results:', results)
                
                # Retrieve and answer based on the given question
                response = qa_chain({"question": user_question})
                
                # Get the answer and related documents
                answer = response['answer']

                # Print the answer
                print("Groq Agent:", answer)
                  
                print("-" * 50)
                
            except Exception as e:
                print(f"發生錯誤: {e}")
                print("很抱歉，我無法處理您的問題。請再試一次或換個問題。")


if __name__ == "__main__":
    main()