from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import soundfile as sf
import datetime
import sys
import os
import asyncio
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ChatTTS')))
import ChatTTS

chat = ChatTTS.Chat()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Text2Speech(BaseModel):
    text: str
    voice: str

model_path = os.path.join(os.path.dirname(__file__), 'models')
model_files = [
    os.path.join(model_path, 'asset/Decoder.pt'),
    os.path.join(model_path, 'asset/DVAE.pt'),
    os.path.join(model_path, 'asset/GPT.pt'),
    os.path.join(model_path, 'asset/spk_stat.pt'),
    os.path.join(model_path, 'asset/tokenizer.pt'),
    os.path.join(model_path, 'asset/Vocos.pt'),
    os.path.join(model_path, 'config/decoder.yaml'),
    os.path.join(model_path, 'config/dvae.yaml'),
    os.path.join(model_path, 'config/gpt.yaml'),
    os.path.join(model_path, 'config/path.yaml'),
    os.path.join(model_path, 'config/vocos.yaml')
]

all_files_exist = all(os.path.exists(file_path) for file_path in model_files)
assert all_files_exist, "Model files do not exist, please download the models."
print('Load models from local path.')
chat.load_models(source='local', local_path=model_path)

@app.post("/generate")
async def generate_text(request: Text2Speech):
    text = request.text
    voice = request.voice
    if voice == 'man':
        torch.manual_seed(2222)
    else:
       torch.manual_seed(6615)
    params_infer_code = {
        'spk_emb': chat.sample_random_speaker(),
        'temperature': 0.1,
        'top_P': 0.7,
        'top_K': 20,
        }

    wavs = await asyncio.to_thread(chat.infer, text, use_decoder=True, params_infer_code=params_infer_code)
    audio_data = np.array(wavs[0])
    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=0)
    
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    output_file = f'outputs/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.wav'
    sf.write(output_file, audio_data.T, 24000)
    return FileResponse(output_file, media_type='audio/wav', filename='generated_audio.wav')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
