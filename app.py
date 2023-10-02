from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, PromptHelper, ServiceContext, StorageContext, set_global_service_context, load_index_from_storage
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def initLogging():
    sys.stdout = sys.stderr

def initOpenAI(max_tokens):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=max_tokens)
    set_global_service_context(ServiceContext.from_defaults(llm=llm))

def readDocumentsFromDisk(docs_dir):
    return SimpleDirectoryReader(input_dir=docs_dir, recursive=True).load_data()

def indexDocuments(documents):
    return GPTVectorStoreIndex.from_documents(documents, show_progress=True)

def saveIndexToDisk(index, index_dir):
    index.storage_context.persist(index_dir)

def readIndexFromDisk(index_dir):
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    return load_index_from_storage(storage_context)

def indexDocumentsAndSave(index_dir):
    documents = readDocumentsFromDisk()
    index = indexDocuments(documents)
    saveIndexToDisk(index, index_dir)
    return index

def createChatEngine(index):
    return index.as_chat_engine(chat_mode="best")

sys.stdout = sys.stderr

print("Starting bootstrap")

DOCS_DIR = '/docs'
INDEX_DIR = '/index'
MAX_TOKENS = 512

initLogging()
initOpenAI(MAX_TOKENS)

numDocs = len(os.listdir(INDEX_DIR))
index = readIndexFromDisk(INDEX_DIR) if numDocs > 0 else indexDocumentsAndSave(INDEX_DIR)

chat_engine = createChatEngine(index)

def chatbot(input_text):
    return chat_engine.chat(input_text).response

# gr.ChatInterface(chatbot, title="Maia's Custom-trained AI Chatbot").launch(share=True)

iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Maia's Custom-trained AI Chatbot")

iface.launch(server_port=7860, share=True)
