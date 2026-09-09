<template>
  <div class="h-full w-full flex items-center justify-center px-8">
    <div
      v-motion
      class="max-w-md text-center flex flex-col items-center gap-5"
      :initial="{ opacity: 0, y: 16, scale: 0.96 }"
      :animate="{ opacity: 1, y: 0, scale: 1 }"
      :transition="{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }"
    >
      <span class="w-14 h-14 flex items-center justify-center border border-white/25 text-white">
        <Icon :name="icon" :size="26" />
      </span>
      <h2 class="text-2xl font-black tracking-[0.2em] text-white uppercase sora">{{ title }}</h2>
      <p class="text-sm text-zinc-400 max-w-sm text-center leading-relaxed">{{ description }}</p>
      <div class="flex flex-wrap gap-2 justify-center">
        <span
          v-for="chip in chips"
          :key="chip"
          class="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider bg-white text-black"
        >
          {{ chip }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Icon from '../../components/Icon.vue'

withDefaults(
  defineProps<{ icon: string; title: string; description: string; chips?: string[] }>(),
  { chips: () => [] },
)
</script>