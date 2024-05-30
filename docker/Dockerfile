FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-devel

WORKDIR /app
RUN apt-get update && \
    apt-get install -y curl git git-lfs && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -  && \
    apt-get install -y nodejs && \
    git-lfs install
RUN git clone https://github.com/Gouryella/ChatTTS-webui.git

WORKDIR /app/ChatTTS-webui
RUN npm install -g yarn && yarn install

WORKDIR /app/ChatTTS-webui/api
RUN git clone https://github.com/2noise/ChatTTS.git && \
    git clone https://huggingface.co/2Noise/ChatTTS.git models

WORKDIR /app/ChatTTS-webui/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3000
COPY docker/start.sh .
RUN chmod +x /app/ChatTTS-webui/start.sh
CMD ["/app/ChatTTS-webui/start.sh"]



