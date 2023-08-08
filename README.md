# Chat with your PDFs using Llama2 LLm

Welcome to the **Chat with your PDFs** GitHub repository! This project aims to revolutionize the way you interact with your PDF documents. By utilizing the power of Llama2 LLm, this project allows you to have natural and dynamic conversations with the text extracted from your PDF files. Say goodbye to manual searching and scrolling through lengthy documents – now you can simply chat with your PDFs!

## Features

- **PDF Text Extraction:** The project automatically extracts text from multiple PDF documents, making it accessible for conversational interactions.

- **Llama2 LLm Integration:** Llama2 LLm, a state-of-the-art language model, is used to facilitate engaging and informative conversations with the content of your PDFs.

- **Conversation History:** The project maintains a conversation history, enabling it to get the whole context of the conversation, by passing the past convo along with every new input.

- **Vector Store Generation:** A vector store is generated for the extracted PDF text, allowing for efficient retrieval and enhanced search capabilities.

- **User-Friendly Interface:** The project provides a simple and intuitive interface for users to interact with their PDFs through conversational inputs.

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/JatinSingh28/Chat-with-your-PDFs-Llama2.git
   cd Chat-with-your-PDFs-Llama2

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt


3. **Download Llama2 Model:**
Download the Llama2 LLm model from [here](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML).

5. **Run the Project:**
    ```bash
    streamlit run app.py
