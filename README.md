# ChatTTS-Nuxt3 Webui

Developed based on [ChatTTS](https://github.com/2noise/ChatTTS/) by [@2noise](https://2noise.com/), web developed by [@Gouryella](https://github.com/Gouryella)

## Step 1
```bash
git clone https://github.com/Gouryella/ChatTTS-webui.git
cd ChatTTS-webui
npm install
```
## Step 2
```bash
yes | conda install pytorch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 pytorch-cuda=12.1 -c pytorch -c nvidia
pip install -r requirements.txt
```

## Step 3
```bash
cd api
git clone https://github.com/2noise/ChatTTS.git
git clone https://huggingface.co/2Noise/ChatTTS.git models
cd ..
```

## Step 4
```bash
npm run dev
python api/server.py
```


## Use Docker
```bash
wget https://raw.githubusercontent.com/Gouryella/ChatTTS-webui/main/docker/Dockerfile
docker build -t chattts_webui .
docker run -itd --name chattts_webui --gpus all -p 3000:3000  chattts_webui
```