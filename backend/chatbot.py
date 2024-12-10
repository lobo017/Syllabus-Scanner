import os
# import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# from typing import List, Dict


class TextChatbot:
    def __init__(self, model_path: str = "meta-llama/Llama-2-7b-chat-hf"):
        """
        Initialize the chatbot with a Llama model and text file processing capabilities.
        
        :param model_path: Path to the Llama model
        """

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir="./model_cache")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            cache_dir="./model_cache",
            device_map='cpu'
        )
        
        # Embedding and vector store components
        self.embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )
        self.vectorstore = None
        
    def load_txt_files_from_directory(self, directory_path: str, file_extension: str = '.txt') -> None:
        """
        Load and process text files from a specified directory.
        
        :param directory_path: Path to the directory containing text files
        :param file_extension: File extension to filter (default is '.txt')
        """
        all_documents = []
        
        # Load and split text files
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        
        # Validate directory path
        if not os.path.isdir(directory_path):
            print(f"Error: {directory_path} is not a valid directory.")
            return
        
        # Collect all text files in the directory
        txt_paths = [
            os.path.join(directory_path, f) 
            for f in os.listdir(directory_path) 
            if f.endswith(file_extension)
        ]
        
        # Print number of files found
        print(f"Found {len(txt_paths)} text files in {directory_path}")
        
        for txt_path in txt_paths:
            try:
                # Load text file
                loader = TextLoader(txt_path, encoding='utf-8')
                documents = loader.load()
                
                # Split documents into chunks
                splits = text_splitter.split_documents(documents)
                all_documents.extend(splits)
            except Exception as e:
                print(f"Error loading {txt_path}: {e}")
        
        # Create vector store from document chunks
        if all_documents:
            self.vectorstore = FAISS.from_documents(
                all_documents, 
                self.embeddings
            )
            print(f"Successfully loaded and processed {len(all_documents)} document chunks.")
        else:
            print("No documents were loaded. Please check your directory and file types.")
        
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """
        Retrieve relevant context from loaded documents.
        
        :param query: User's query
        :param top_k: Number of top relevant documents to retrieve
        :return: Retrieved context as a string
        """
        if not self.vectorstore:
            return "No documents have been loaded."
        
        # Retrieve top k most similar document chunks
        results = self.vectorstore.similarity_search(query, k=top_k)
        context = "\n".join([doc.page_content for doc in results])
        
        return context
    
    def generate_response(self, query: str) -> str:
        """
        Generate a response based on the query and retrieved context.
        
        :param query: User's query
        :return: AI-generated response
        """
        # Retrieve context
        context = self.retrieve_context(query)
        
        # Prepare prompt with context
        prompt = f"""Context: {context}
        
Question: {query}
Answer the question based on the given context. If the context does not provide 
sufficient information, indicate that you cannot find a definitive answer."""
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # Generate response
        outputs = self.model.generate(
            inputs.input_ids, 
            max_length=500,
            num_return_sequences=1,
            temperature=0.7
        )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return response
    
    def chat(self) -> None:
        """
        Interactive chat interface for the text file-trained chatbot.
        """
        print("Text File Chatbot: Hello! I'm ready to answer questions about the documents you've loaded.")
        print("Type 'quit' to exit.")
        
        while True:
            query = input("You: ")
            
            if query.lower() == 'quit':
                break
            
            response = self.generate_response(query)
            print("Chatbot:", response)


def main():
    # Example usage
    chatbot = TextChatbot()

    # Load text files from a directory
    directory_path = '../textfiles'
    chatbot.load_txt_files_from_directory(directory_path)
    
    # Start interactive chat
    chatbot.chat()


if __name__ == "__main__":
    main()
