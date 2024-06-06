<template>
    <a-layout class="layout">
        <a-layout-header class="layout-nav" style="background: #FF3C37;">
            <a href="https://github.com/Gouryella/ChatTTS-webui" style="color: inherit; text-decoration: none;">
                <div class="logo">
                    <img class="ico" src="/favicon.ico" alt="icon" />
                    <p class="nav-text">ChatTTS WebUI</p>
                </div>
            </a>
            <a-button type="default" @click="toggleLanguage" style="color: black; border: none;">
                {{ language === 'en' ? '切换到中文' : 'Switch to English' }}
            </a-button>
        </a-layout-header>
        <a-layout-content>
            <div class="content" >
                <a-textarea class="textarea" v-model:value="text" :rows="6" :placeholder="language === 'en' ? 'Input text...' : '输入文字...'" ref="textareaRef"/>
                <div class="setting">
                    <div class="button-group">
                        <div class="function-button">
                            <a-button style="margin-right: 10px;width: 100px;" type="primary" @click="addLaugh">{{ language === 'en' ? 'Add Laugh' : '加笑声' }}</a-button>
                            <a-button style="width: 100px;" type="primary" @click="addBreak">{{ language === 'en' ? 'Add Break' : '加停顿' }}</a-button>
                        </div>
                        <a-radio-group class="voice_adj-button" v-model:value="voice" >
                            <a-radio-button :value="voice_adj === 2222 ? 'man' : null" value="man" style="width: 120px; text-align: center;" @click="setVoiceAdj(2222)">{{ language === 'en' ? 'Male Voice' : '男声' }}</a-radio-button>
                            <a-radio-button :value="voice_adj === 6615 ? 'woman' : null" value="woman" style="width: 120px; text-align: center;" @click="setVoiceAdj(6615)">{{ language === 'en' ? 'Female Voice' : '女声' }}</a-radio-button>
                        </a-radio-group>
                    </div>
                    <div class="slider-group">
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="margin-right: 10px;">{{language === 'en' ? 'Voice Adjustment' : '声音调节' }}</span>
                            <a-slider v-model:value="voice_adj" :min="0" :max="10000" :step="1" style="flex: 1;" />
                            <a-input-number v-model:value="voice_adj" :min="0" :max="10000" :step="1" style="margin-left: 16px" />
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="margin-right: 10px;">Temperature</span>
                            <a-slider v-model:value="temperature" :min="0.1" :max="1" :step="0.1" style="flex: 1;" />
                            <a-input-number v-model:value="temperature" :min="0.1" :max="1" :step="0.1" style="margin-left: 16px" />
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="margin-right: 10px;">Top P</span>
                            <a-slider v-model:value="top_p" :min="0.1" :max="1" :step="0.1" style="flex: 1;" />
                            <a-input-number v-model:value="top_p" :min="0.1" :max="1" :step="0.1" style="margin-left: 16px" />
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="margin-right: 10px;">Top K</span>
                            <a-slider v-model:value="top_k" :min="1" :max="100" :step="1" style="flex: 1;" />
                            <a-input-number v-model:value="top_k" :min="1" :max="100" :step="1" style="margin-left: 16px" />
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: space-between;">
                            <span>{{language === 'en' ? 'Speed' : '语速' }}</span>
                            <a-input-number class="setting-input" v-model:value="speed" :min="0" :max="9" :step="1" />
                            <span>{{language === 'en' ? 'Oral' : '口语' }}</span>
                            <a-input-number class="setting-input" v-model:value="oral" :min="0" :max="9" :step="1" />
                            <span>{{language === 'en' ? 'Laugh' : '笑声' }}</span>
                            <a-input-number class="setting-input" v-model:value="laugh" :min="0" :max="2" :step="1" />
                            <span>{{language === 'en' ? 'Break' : '停顿' }}</span>
                            <a-input-number class="setting-input" v-model:value="break_value" :min="0" :max="7" :step="1" />
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: flex; justify-content: center; margin-top: 20px;">
                <a-button class="generate-button" type="primary" @click="generate">{{ language === 'en' ? 'Generate' : '生成' }}</a-button>
            </div>
            <br/>
            <br/>
            <div v-if="loading" style="text-align: center;">
                <a-spin :indicator="indicator" />
                <p>{{ language === 'en' ? 'Please wait...' : '请稍后...' }}</p>
            </div>
            <div v-if="audioUrl" style="text-align: center;">
                <p>{{ language === 'en' ? 'Generated Audio' : '生成的音频' }}</p>
                <div class="waveform-container">
                    <div id="waveform"></div>
                </div>
                <br/>
                <a :href="audioUrl" download="generated_audio_by_201lab.wav">
                    <a-button class="download-button" type="primary">{{ language === 'en' ? 'Download Audio' : '下载音频' }}</a-button>
                </a>
            </div>
        </a-layout-content>
        <a-layout-footer style="text-align: center;">
            Developed based on <a href="https://github.com/2noise/ChatTTS/">ChatTTS</a> by <a href="https://2noise.com/">@2noise</a>, web developed by <a href="https://github.com/Gouryella">@Gouryella</a>
        </a-layout-footer>
    </a-layout>
</template>

<script setup>
import { ref, h, watch, nextTick } from 'vue';
import { LoadingOutlined } from '@ant-design/icons-vue';
import axios from 'axios';
import WaveSurfer from 'wavesurfer.js';
import { message } from 'ant-design-vue';

const text = ref('');
const voice = ref('man');
const audioUrl = ref('');
const loading = ref('');
const language = ref('en');
const temperature = ref(0.4)
const top_p = ref(0.7)
const top_k = ref(20)
const speed = ref(3)
const oral = ref(2)
const laugh = ref(0)
const break_value = ref(4)
const voice_adj = ref(2222)
const textareaRef = ref(null);

let wavesurfer;

const indicator = h(LoadingOutlined, { style: { fontSize: '50px' } });

const toggleLanguage = () => {
    language.value = language.value === 'en' ? 'zh' : 'en';
};



const insertText = (insertedText) => {
    const dom = textareaRef.value?.resizableTextArea?.textarea || textareaRef.value?.resizableTextArea?.textArea;
    if (!dom) return;
    const index = dom.selectionStart;
    const content = text.value;

    text.value = content.substring(0, index) + insertedText + content.substring(index, content.length);


    nextTick(() => {
        dom.focus();
        dom.setSelectionRange(index + insertedText.length, index + insertedText.length);
    });
};


const addLaugh = () => {
  insertText('[laugh]');
};

const addBreak = () => {
  insertText('[uv_break]');
};


const setVoiceAdj = (value) => {
    voice_adj.value = value;
};
const generate = async () => {
    if (!text.value || text.value === '0') {
        if (language.value === 'zh') {
            message.error('输入文本不能为空');
        } else {
            message.error('Input text cannot be empty');
        }
        return;
    }
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
                top_k: top_k.value,
                speed: speed.value,
                oral: oral.value,
                laugh: laugh.value,
                break_value: break_value.value,
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
        console.error(error);
    } finally {
        loading.value = false;
    }
};
const initWaveSurfer = (url) => {
    nextTick(() => {
        if (wavesurfer) {
            wavesurfer.destroy();
        }
        wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: 'rgb(200, 0, 200)',
            progressColor: 'rgb(100, 0, 100)',
            barWidth: 3,
            barGap: 1,
            barRadius: 2,
            minPxPerSec: 2,
            height: 100,
            mediaControls: true,
        });
        wavesurfer.load(url);

        wavesurfer.on('interaction', () => {
        wavesurfer.play()
        })
    });
};

watch(audioUrl, (newUrl) => {
    if (newUrl) {
        initWaveSurfer(newUrl);
        
    }
});
</script>

<style>
.layout {
    min-height: 100vh;
    width: 100%;
}

.ant-layout .ant-layout-content{
    padding: 20px 50px;
}

.layout-nav{
    display: flex; 
    align-items: center; 
    justify-content: space-between; 
}

#waveform {
    width: 500px;
}

.logo{
    display: flex; 
    align-items: center;
}

.ico{
    width: 3em; 
    height: 3em; 
    margin-right: 10px;
}

.nav-text{
    color: white; 
    font-size: 2em; 
    margin: 0;
}

.nav-ad{
    color: white; 
    font-size: large; 
    position: absolute; 
    left: 50%; 
    transform: translateX(-50%); 
    margin: 0;
}

.content{
    display: flex; 
    align-items: center; 
    width: 100%; 
    justify-content: center;
}

.voice_adj-button{
    display: flex; 
    margin-left: 10px;
}

.button-group{
    display: flex; 
    margin-bottom: 10px;
}


.setting{
    display: flex; 
    flex-direction: column; 
    margin-left: 10px;
}

.textarea{
    width: 30%; 
    min-width: 300px;
    border-radius: 7px; 
    font-size: 27px;
}

.slider-group {
    width: auto;
}

.generate-button{
    width: 500px;
    margin-top: 10px;
}

.waveform-container{
    height: 100px; 
    margin-top: 20px;
    display: flex; 
    justify-content: center; 
}

.download-button{
    margin-top: 80px;
}



@media (max-width: 600px) {
.ant-layout .ant-layout-header{
    padding-inline:10px;
}

.ant-layout .ant-layout-content{
    padding: 0;
}
.nav-text{
    font-size: 1.5em; 
    white-space: normal;
}
.nav-ad {
    display: none;
}
.button-group{
    flex-direction: column;
}

.function-button{
    display: flex;
    margin-top: 20px;
    justify-content:center;
}

.voice_adj-button {
    margin: 10px auto 0 auto;
}

.content{
    flex-direction: column;
    margin-top: 25px;
    }

.slider-group {
    width: 95vw;
}

.generate-button{
    width: 300px;
    margin-top: 0;
}
#waveform {
    width: 100vw;
}
}
</style>
