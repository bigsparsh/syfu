<template>
  <div class="min-h-screen w-screen flex overflow-x-hidden bg-black lg:h-screen lg:overflow-hidden">
    <!-- Retractable sidebar (drawer on mobile) -->
    <Sidebar
      class="h-full"
      :collapsed="collapsed"
      :active="active"
      :mobile-open="mobileOpen"
      @toggle="collapsed = !collapsed"
      @select="onSelect"
      @close="mobileOpen = false"
    />

    <!-- Mobile backdrop -->
    <transition name="fade">
      <div
        v-if="mobileOpen"
        class="fixed inset-0 z-30 bg-black/70 lg:hidden"
        @click="mobileOpen = false"
      ></div>
    </transition>

    <!-- Main area -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top bar -->
      <div class="h-12 flex items-center gap-3 px-5 border-b border-white/10 bg-black shrink-0">
        <button
          class="lg:hidden w-7 h-7 shrink-0 flex items-center justify-center border border-white/20 text-white"
          @click="mobileOpen = true"
        >
          <Icon name="menu" :size="16" />
        </button>
        <h1
          v-motion
          class="text-base lg:text-lg font-black tracking-[0.25em] text-white uppercase sora truncate"
          :key="active"
          :initial="{ opacity: 0, y: -8 }"
          :animate="{ opacity: 1, y: 0 }"
          :transition="{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }"
        >
          {{ headerFor(active) }}
        </h1>
        <span class="ml-auto text-[11px] text-zinc-400 tabular-nums">{{ today }}</span>
      </div>

      <!-- Active view -->
      <div class="flex-1 p-5 min-h-0 overflow-y-auto">
        <HomeView v-if="active === 'home'" class="lg:h-full" />
        <TasksView v-else-if="active === 'tasks'" class="lg:h-full" />
        <PlaceholderView
          v-else-if="active === 'projects'"
          icon="projects"
          title="Projects"
          description="Every project, its milestones and the tasks that keep it moving — one sharp board, no clutter."
          :chips="['Active', 'Archived', 'Milestones']"
          class="lg:h-full"
        />
        <PlaceholderView
          v-else-if="active === 'timetable'"
          icon="timetable"
          title="Timetable"
          description="A full week view of your schedule. Drag blocks, resolve overlaps, and protect your deep-work hours."
          :chips="['Week', 'Month', 'Gantt']"
          class="lg:h-full"
        />
        <PlaceholderView
          v-else-if="active === 'suggestions'"
          icon="suggestions"
          title="Suggestions"
          description="Intelligent nudges computed from your calendar, habits and energy — everything that helps you reclaim your day."
          :chips="['Smart', 'Focus', 'Rest']"
          class="lg:h-full"
        />
        <ChatView v-else-if="active === 'chat'" class="lg:h-full" />
        <PlaceholderView
          v-else-if="active === 'analytics'"
          icon="analytics"
          title="Analytics"
          description="Your time, spent and saved. Break it down by week, project and focus to see where the hours actually go."
          :chips="['Focus', 'Projects', 'Trends']"
          class="lg:h-full"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import Sidebar from './dashboard/Sidebar.vue'
import HomeView from './dashboard/HomeView.vue'
import ChatView from './dashboard/ChatView.vue'
import TasksView from './dashboard/TasksView.vue'
import PlaceholderView from './dashboard/PlaceholderView.vue'
import Icon from '../components/Icon.vue'

const collapsed = ref(false)
const mobileOpen = ref(false)

const active = ref('home')
const onSelect = (id: string) => {
  active.value = id
  mobileOpen.value = false
}

const titles: Record<string, string> = {
  home: 'Home',
  tasks: 'Tasks',
  projects: 'Projects',
  timetable: 'Timetable',
  suggestions: 'Suggestions',
  chat: 'Chat',
  analytics: 'Analytics',
}

const headerFor = (id: string) => titles[id] ?? 'Home'

const today = computed(() =>
  new Date().toLocaleDateString(undefined, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  }),
)
</script>