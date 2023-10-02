FROM ubuntu:jammy
 
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN mkdir /docs && mkdir /index

RUN apt-get update && apt-get install -y python3-pip curl

RUN pip install openai && \
    pip install llama_index && \
    pip install langchain && \
    pip install gradio

RUN pip install pypdf && \
    pip install PyCryptodome && \
    pip install nltk && \ 
    pip install watchdog

RUN python3 -m nltk.downloader punkt

COPY app.py .

CMD [ "python3", "app.py" ]
