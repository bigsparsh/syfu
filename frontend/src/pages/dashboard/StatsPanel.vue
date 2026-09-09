<template>
  <div class="grid grid-cols-2 gap-px bg-white/15 border border-white/15">
    <div
      v-for="(stat, i) in stats"
      :key="stat.label"
      v-motion
      class="h-full min-h-[70px] px-4 py-3 flex items-center gap-3 bg-neutral-950"
      :initial="{ opacity: 0, y: 12 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ duration: 0.45, ease: [0.16, 1, 0.3, 1], delay: 0.12 * (i + 1) }"
    >
      <span
        class="w-9 h-9 shrink-0 flex items-center justify-center border border-white/20 text-white"
      >
        <Icon :name="stat.icon" :size="16" />
      </span>
      <div class="min-w-0 leading-none">
        <p class="text-[20px] font-bold text-white sora tabular-nums">{{ stat.value }}</p>
        <p class="text-[10px] text-zinc-400 mt-1 truncate">{{ stat.sub }}</p>
        <p class="text-[9px] uppercase tracking-[0.18em] text-zinc-500 mt-0.5">{{ stat.label }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Icon from '../../components/Icon.vue'
import { stats } from './mock'
</script>