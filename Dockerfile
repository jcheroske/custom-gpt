FROM ubuntu:jammy

RUN apt-get update && apt-get install -y python3-pip curl

RUN pip install openai && \
    pip install llama_index && \
    pip install langchain && \
    pip install pypdf && \
    pip install PyCryptodome && \
    pip install gradio && \
    # pip install gevent==22.10.2 && \
    pip install nltk

RUN python3 -m nltk.downloader punkt

RUN curl -o /usr/local/lib/python3.10/dist-packages/gradio/frpc_linux_aarch64_v0.2 https://cdn-media.huggingface.co/frpc-gradio-0.2/frpc_linux_aarch64
    # chmod +x /usr/local/lib/python3.10/dist-packages/gradio/frpc_linux_aarch64_v0.2

COPY app.py .

RUN mkdir /docs && mkdir /index

CMD [ "python3", "app.py" ]
