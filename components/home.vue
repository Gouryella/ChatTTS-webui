<template>
    <a-layout class="layout">
        <a-layout-header style="background: #FF3C37; display: flex; align-items: center; justify-content: space-between;">
            <p style="color: white; font-size: 2em; margin: 0; " >ChatTTS WebUI</p>
            <a-button type="default" @click="toggleLanguage" style="color: black; border: none;">
                {{ language === 'en' ? '切换到中文' : 'Switch to English' }}
            </a-button>
        </a-layout-header>
        <a-layout-content style="padding: 20px 50px;">
            <div style="display: flex; align-items: center; width: 100%; justify-content: center;">
                <a-textarea v-model:value="text" :rows="4" :placeholder="language === 'en' ? 'Input text...' : '输入文字...'" style="width: 30%; min-width: 300px;border-radius: 7px;" />
                <div style="display: flex; flex-direction: column; margin-left: 10px;">
                    <div style="display: flex; margin-bottom: 10px;">
                        <a-button type="primary" style="margin-right: 10px;" @click="addLaugh">{{ language === 'en' ? 'Add Laugh' : '加笑声' }}</a-button>
                        <a-button type="primary" @click="addBreak">{{ language === 'en' ? 'Add Break' : '加停顿' }}</a-button>
                        <a-radio-group v-model:value="voice" style="display: flex; margin-left: 10px;">
                            <a-radio-button value="man">{{ language === 'en' ? 'Male Voice' : '男声' }}</a-radio-button>
                            <a-radio-button value="woman">{{ language === 'en' ? 'Female Voice' : '女声' }}</a-radio-button>
                        </a-radio-group>
                    </div>
                    <a-button type="primary" style="width: 100%;" @click="generate">{{ language === 'en' ? 'Generate' : '生成' }}</a-button>
                </div>
            </div>
            <br/>
            <br/>
            <div v-if="loading" style="text-align: center;">
                <a-spin :indicator="indicator" />
            </div>
            <div v-if="audioUrl" style="text-align: center;">
                <p>{{ language === 'en' ? 'Generated Audio:' : '生成的音频:' }}</p>
                <audio :src="audioUrl" controls></audio>
                <br/>
                <a :href="audioUrl" download="generated_audio.wav">
                    <a-button type="primary" style="margin-top: 10px;">{{ language === 'en' ? 'Download Audio' : '下载音频' }}</a-button>
                </a>
            </div>
        </a-layout-content>
        <a-layout-footer style="text-align: center;">
            Developed based on <a href="https://github.com/2noise/ChatTTS/">ChatTTS</a> by <a href="https://2noise.com/">@2noise</a>, web developed by <a href="https://github.com/Gouryella">@Gouryella</a>
        </a-layout-footer>
    </a-layout>
</template>

<script setup>
import { ref, h } from 'vue';
import { LoadingOutlined } from '@ant-design/icons-vue';
import axios from 'axios';

const text = ref('');
const voice = ref('man');
const audioUrl = ref('');
const loading = ref('');
const language = ref('en');
const indicator = h(LoadingOutlined, { style: { fontSize: '50px' } });

const toggleLanguage = () => {
    language.value = language.value === 'en' ? 'zh' : 'en';
};

const addLaugh = () => {
    text.value += '[laugh]';
};

const addBreak = () => {
    text.value += '[uv_break]';
};

const generate = async () => {
    loading.value = true;
    audioUrl.value = false;
    console.log(voice.value);
    try {
        const response = await axios.post(
            'http://192.168.1.69:8000/generate',
            {
                text: text.value,
                voice: voice.value
            },
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                responseType: 'blob',
            }
        );
        const url = URL.createObjectURL(new Blob([response.data], { type: 'audio/wav' }));
        audioUrl.value = url;
        console.log(audioUrl.value);
        console.log(text.value);
    } catch (error) {
        console.error('生成音频时出错:', error);
    } finally {
        loading.value = false;
    }
};
</script>

<style>
.layout {
    min-height: 100vh;
    width: 100%;
}

.layout-header {
    width: 100%;
    background-color: #001529;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-title {
    color: white;
    font-size: 1.8em;
    margin: 0;
    font-weight: bold;
}

.layout-content {
    padding: 20px 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f0f2f5;
}

.content-wrapper {
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: center;
}

.textarea {
    width: 40%;
    min-width: 300px;
    border-radius: 5px;
}

.controls {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}

.buttons {
    display: flex;
    margin-bottom: 20px;
}

.control-button {
    margin-right: 10px;
}

.radio-group {
    display: flex;
    margin-left: 20px;
}

.generate-button {
    width: 100%;
}

.loading {
    text-align: center;
}

.audio-result {
    text-align: center;
}

.audio-player {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

.download-button {
    margin-top: 10px;
}

.layout-footer {
    text-align: center;
    padding: 24px 50px;
    background: #001529;
    color: white;
}
</style>
