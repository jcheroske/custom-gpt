from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, PromptHelper, ServiceContext, StorageContext, set_global_service_context, load_index_from_storage
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os

print("Starting bootstrap")

docs_directory = '/docs'
index_dir = '/index'

max_input_size = 4096
num_outputs = 512
max_chunk_overlap = .5 # Unknown what this does
chunk_size_limit = 600

prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs)
service_context = ServiceContext.from_defaults(llm=llm, prompt_helper=prompt_helper)
set_global_service_context(service_context)

index = None
if len(os.listdir(index_dir)) > 0:
    print('Loading index file from disk')
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    index = load_index_from_storage(storage_context)

else:
    print('No index file found')

    documents = SimpleDirectoryReader(docs_directory, recursive=True).load_data()
    print(f"Loaded {len(documents)} docs")

    index = GPTVectorStoreIndex.from_documents(documents)

    index.storage_context.persist(index_dir)

    print('Index file saved to disk')


def chatbot(input_text):
    print(f"Chatbot called")
    response = index.query(input_text, response_mode="compact")
    return response.response

iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

iface.launch(server_port=7860, share=True)
