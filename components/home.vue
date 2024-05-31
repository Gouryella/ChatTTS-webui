<template>
    <a-layout class="layout">
        <a-layout-header style="background: #FF3C37; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center;">
                <img src="/public/favicon.ico" alt="icon" style="width: 3em; height: 3em; margin-right: 10px;" />
                <p style="color: white; font-size: 2em; margin: 0;">ChatTTS WebUI</p>
            </div>
            <a-button type="default" @click="toggleLanguage" style="color: black; border: none;">
                {{ language === 'en' ? '切换到中文' : 'Switch to English' }}
            </a-button>
        </a-layout-header>
        <a-layout-content style="padding: 20px 50px;">
            <div style="display: flex; align-items: center; width: 100%; justify-content: center;">
                <a-textarea v-model:value="text" :rows="5" :placeholder="language === 'en' ? 'Input text...' : '输入文字...'" style="width: 30%; min-width: 300px;border-radius: 7px; font-size: 27px" />
                <div style="display: flex; flex-direction: column; margin-left: 10px;">
                    <div style="display: flex; margin-bottom: 10px;">
                        <a-button type="primary" style="margin-right: 10px;width: 100px;" @click="addLaugh">{{ language === 'en' ? 'Add Laugh' : '加笑声' }}</a-button>
                        <a-button type="primary" style="width: 100px;" @click="addBreak">{{ language === 'en' ? 'Add Break' : '加停顿' }}</a-button>
                        <a-radio-group v-model:value="voice" style="display: flex; margin-left: 10px;">
                            <a-radio-button :value="voice_adj === 2222 ? 'man' : null" value="man" style="width: 120px; text-align: center;" @click="setVoiceAdj(2222)">{{ language === 'en' ? 'Male Voice' : '男声' }}</a-radio-button>
                            <a-radio-button :value="voice_adj === 6615 ? 'woman' : null" value="woman" style="width: 120px; text-align: center;" @click="setVoiceAdj(6615)">{{ language === 'en' ? 'Female Voice' : '女声' }}</a-radio-button>
                        </a-radio-group>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="margin-right: 10px;">{{ language === 'en' ? 'Voice Adjustment' : '声音调节' }}</span>
                        <a-slider v-model:value="voice_adj" :min="0" :max="10000" :step="1" style="flex: 1;" />
                        <a-input-number v-model:value="voice_adj" :min="0" :max="10000" :step="1" style="margin-left: 16px" />
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="margin-right: 10px;">Temperature</span>
                        <a-slider v-model:value="temperature" :min="0" :max="1" :step="0.1" style="flex: 1;" />
                        <a-input-number v-model:value="temperature" :min="0" :max="1" :step="0.1" style="margin-left: 16px" />
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="margin-right: 10px;">Top P</span>
                        <a-slider v-model:value="top_p" :min="0" :max="1" :step="0.1" style="flex: 1;" />
                        <a-input-number v-model:value="top_p" :min="0" :max="1" :step="0.1" style="margin-left: 16px" />
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="margin-right: 10px;">Top K</span>
                        <a-slider v-model:value="top_k" :min="1" :max="100" :step="1" style="flex: 1;" />
                        <a-input-number v-model:value="top_k" :min="1" :max="100" :step="1" style="margin-left: 16px" />
                    </div>
                </div>
            </div>
            <div style="display: flex; justify-content: center; margin-top: 20px;">
                <a-button type="primary" style="width: 30%;" @click="generate">{{ language === 'en' ? 'Generate' : '生成' }}</a-button>
            </div>
            <br/>
            <br/>
            <div v-if="loading" style="text-align: center;">
                <a-spin :indicator="indicator" />
                <p>{{ language === 'en' ? 'Please wait...' : '请稍后...' }}</p>
            </div>
            <div v-if="audioUrl" style="text-align: center;">
                <p>{{ language === 'en' ? 'Generated Audio' : '生成的音频' }}</p>
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
const temperature = ref(0.4)
const top_p = ref(0.7)
const top_k = ref(20)
const voice_adj = ref(2222)

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
const setVoiceAdj = (value) => {
    voice_adj.value = value;
};
const generate = async () => {
    loading.value = true;
    audioUrl.value = false;
    try {
        const response = await axios.post(
            'http://127.0.0.1:8000/generate',
            {
                text: text.value,
                voice_adj: voice_adj.value,
                temperature: temperature.value,
                top_p: top_p.value,
                top_k: top_k.value
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
