from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import soundfile as sf
import datetime
import sys
import os
import asyncio
import torch
from io import BytesIO

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
    voice_adj: int
    temperature: float
    top_p: float
    top_k: int 

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
    torch.manual_seed(request.voice_adj)
    params_infer_code = {
        'spk_emb': chat.sample_random_speaker(),
        'temperature': request.temperature,
        'top_P': request.top_p,
        'top_K': request.top_k,
        }

    wavs = await asyncio.to_thread(chat.infer, text, use_decoder=True, params_infer_code=params_infer_code)
    audio_data = np.array(wavs[0])
    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=0)
    
    audio_buffer = BytesIO()
    sf.write(audio_buffer, audio_data.T, 24000, format='WAV')
    audio_buffer.seek(0)
    
    return StreamingResponse(audio_buffer, media_type='audio/wav')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
