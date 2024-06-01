export default defineNuxtConfig({
  modules: [
    '@ant-design-vue/nuxt'
  ],
  app: {
    head: {
        title: "ChatTTS-WebUI",
        meta: [
            { name: "description", content: "Powered by @ Gouryella" },
            { name: "keyword", content: "ChatTTS" }
        ],
        link: [
            { rel: "icon", type: "image/x-icon", href: "/favicon.ico" }
        ]
    }
},
})
