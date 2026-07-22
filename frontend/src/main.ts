import { createApp } from 'vue'
import './style.css'
import Landing from './Landing.vue';
import { createMemoryHistory, createRouter } from 'vue-router';
import Dashboard from './pages/Dashboard.vue';
import "@fontsource/sora";
import "@fontsource/space-grotesk";

const routes =  [
    {path: "/", component: Landing},
    {path: "/dashboard", component: Dashboard}
]

export const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

const app = createApp(Landing);

app.use(router)
app.mount('#app')