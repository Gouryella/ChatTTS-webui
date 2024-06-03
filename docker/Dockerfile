FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-devel

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl git git-lfs && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    git-lfs install && \
    git clone https://github.com/Gouryella/ChatTTS-webui.git

WORKDIR /app/ChatTTS-webui

RUN npm install -g yarn && yarn install && \
    git clone https://github.com/2noise/ChatTTS.git api/ChatTTS && \
    cd api/ChatTTS && git checkout a0a1a9f && cd ../.. && \
    git clone https://huggingface.co/2Noise/ChatTTS.git api/models && \
    pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/ChatTTS-webui/docker/start.sh

EXPOSE 3000

CMD ["/app/ChatTTS-webui/docker/start.sh"]
