import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import 'primeicons/primeicons.css'
import Nora from '@primeuix/themes/nora'
import Toast from 'primevue/toast'

const app = createApp(App)
app.use(PrimeVue, {
    theme: {
        preset: Nora
    }
})
app.use(router)
app.use(ToastService)


app.component('Toast', Toast)
app.mount('#app')