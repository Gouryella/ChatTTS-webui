#!/bin/bash
cd /app/ChatTTS-webui/
nohup npm run dev > /dev/null 2>&1 &
python api/server.py