import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplate import css, bot_template, user_template
from langchain.llms import CTransformers


def extract_txt(pdfs):
    text = ""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()

    return text


def split_txt(text):
    splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = splitter.split_text(text)
    return chunks


def generate_vectorStore(data):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    vector_store = FAISS.from_texts(texts=data, embedding=embeddings)
    return vector_store


def load_llama():
    llm = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens=512,
        temprature=0.5,
    )
    return llm


def generate_convo(vector_store):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # llm = HuggingFaceHub(
    #     # repo_id="google/flan-t5-xxl",
    #     # repo_id="meta-llama/Llama-2-7b-chat-hf",
    #     repo_id="TheBloke/Llama-2-7B-Chat-GGML",
    #     model_kwargs={"temperature": 0.5, "max_length": 1000},
    # )
    llm = load_llama()
    convo_chain = ConversationalRetrievalChain.from_llm(
        retriever=vector_store.as_retriever(), memory=memory, llm=llm
    )
    return convo_chain


def handle_input(user_question):
    response = st.session_state.convo({"question": user_question})
    st.write(response)
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with your PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "convo" not in st.session_state:
        st.session_state.convo = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with your PDFs :books:")
    input = st.text_input("Ask questions from your PDFs")
    if input:
        handle_input(input)

    with st.sidebar:
        st.header("Your documents")
        pdfs = st.file_uploader("Upload your PDFs", accept_multiple_files=True)
        if st.button("Process"):
            if not pdfs:
                st.write("Atleast upload one PDF")
            else:
                with st.spinner("Processing"):
                    text = extract_txt(pdfs)

                    chunks = split_txt(text)

                    vector_store = generate_vectorStore(chunks)

                    st.session_state.convo = generate_convo(vector_store)
                st.write("Processed")


if __name__ == "__main__":
    main()
