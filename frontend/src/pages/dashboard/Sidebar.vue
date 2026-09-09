<template>
  <aside
    v-motion
    class="h-full flex flex-col bg-black border-r border-white/10 overflow-hidden fixed top-0 bottom-0 left-0 z-40 w-full lg:static lg:h-full"
    :initial="{ width: EXPANDED_W + 'px', x: '-100%' }"
    :animate="sidebarAnimate"
    :transition="{ duration: 0.28, ease: [0.32, 0.72, 0, 1] }"
  >
    <!-- Brand -->
    <div class="flex items-center h-12 px-3 gap-3 border-b border-white/10 shrink-0">
      <span
        class="w-8 h-8 shrink-0 flex items-center justify-center border border-white/30 text-white"
      >
        <Icon name="home" :size="16" />
      </span>
      <span
        v-motion
        class="font-black text-lg tracking-[0.3em] text-white sora whitespace-nowrap"
        :animate="{ opacity: collapsed || isMobile ? 0 : 1 }"
      >
        SYFU
      </span>
      <button
        class="ml-auto lg:hidden w-7 h-7 flex items-center justify-center border border-white/20 text-white"
        @click.prevent="$emit('close')"
      >
        <Icon name="x" :size="14" />
      </button>
    </div>

    <!-- Nav -->
    <nav class="flex-1 overflow-y-auto px-2 py-3 flex flex-col gap-px bg-white/10">
      <button
        v-for="item in items"
        :key="item.id"
        class="h-11 flex items-center px-3 gap-3 w-full select-none cursor-pointer"
        :class="item.id === active ? 'bg-white text-black' : 'bg-neutral-900 text-white hover:bg-neutral-800'"
        @click.prevent="onSelect(item.id)"
      >
        <span class="w-5 h-5 shrink-0 flex items-center justify-center" :class="item.id === active ? 'text-black' : 'text-white'">
          <Icon :name="item.icon" :size="18" />
        </span>
        <span
          v-motion
          class="flex-1 min-w-0 text-left text-[13px] font-medium truncate whitespace-nowrap"
          :animate="{ opacity: collapsed || isMobile ? 0 : 1, x: collapsed ? -6 : 0 }"
          :transition="{ duration: 0.18 }"
        >
          {{ item.label }}
        </span>
      </button>
    </nav>

    <!-- Collapse toggle (desktop only; mobile uses the close drawer) -->
    <div class="hidden lg:flex items-center px-3 h-11 shrink-0">
      <button
        class="h-8 w-full flex items-center px-3 gap-3 border border-white/15 text-white hover:bg-neutral-800"
        @click.prevent="$emit('toggle')"
      >
        <span class="w-5 h-5 shrink-0 flex items-center justify-center">
          <Icon :name="collapsed ? 'expand' : 'collapse'" :size="18" />
        </span>
        <span
          v-motion
          class="flex-1 text-left text-[12px] truncate whitespace-nowrap"
          :animate="{ opacity: collapsed ? 0 : 1 }"
          :transition="{ duration: 0.18 }"
        >
          Collapse
        </span>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'
import Icon from '../../components/Icon.vue'

const EXPANDED_W = 248
const COLLAPSED_W = 72

interface NavItem {
  id: string
  label: string
  icon: string
}

const items: NavItem[] = [
  { id: 'home', label: 'Home', icon: 'home' },
  { id: 'tasks', label: 'Tasks', icon: 'tasks' },
  { id: 'projects', label: 'Projects', icon: 'projects' },
  { id: 'timetable', label: 'Timetable', icon: 'timetable' },
  { id: 'suggestions', label: 'Suggestions', icon: 'suggestions' },
  { id: 'chat', label: 'Chat', icon: 'chat' },
  { id: 'analytics', label: 'Analytics', icon: 'analytics' },
]

const props = withDefaults(
  defineProps<{ collapsed?: boolean; active?: string; mobileOpen?: boolean }>(),
  { collapsed: false, active: 'home', mobileOpen: false },
)

const emit = defineEmits<{ toggle: []; select: [id: string]; close: [] }>()
const onSelect = (id: string) => emit('select', id)

// `isMobile` = below the `lg` breakpoint even, drives the off-canvas drawer.
const isMobile = ref(typeof window !== 'undefined' ? window.innerWidth < 1024 : false)
const onResize = () => {
  isMobile.value = window.innerWidth < 1024
}
window.addEventListener('resize', onResize)
onUnmounted(() => window.removeEventListener('resize', onResize))

// Desktop: width animates between expanded/collapsed, x stays 0.
// Mobile: fixed 248px drawer that slides in/out via x.
const sidebarAnimate = computed(() => ({
  width: (isMobile.value || !props.collapsed ? EXPANDED_W : COLLAPSED_W) + 'px',
  x: isMobile.value ? (props.mobileOpen ? '0px' : '-100%') : '0px',
}))
</script>