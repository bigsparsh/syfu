<template>
  <div class="flex flex-col gap-2 overflow-y-auto">
    <div
      v-for="(item, i) in suggestions"
      :key="item.id"
      v-motion
      class="flex items-start gap-3 px-4 py-3 bg-neutral-950 border border-white/15"
      :initial="{ opacity: 0, y: 14 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ duration: 0.5, ease: [0.16, 1, 0.3, 1], delay: 0.1 * (i + 1) }"
    >
      <span class="w-8 h-8 shrink-0 flex items-center justify-center border border-white/20 text-white">
        <Icon :name="item.icon" :size="15" />
      </span>
      <div class="min-w-0 flex-1">
        <h3 class="text-[12px] font-semibold text-white leading-tight">{{ item.title }}</h3>
        <p class="text-[10.5px] text-zinc-400 mt-1.5 leading-snug line-clamp-3">{{ item.body }}</p>
      </div>
      <button
        class="shrink-0 h-7 px-2.5 text-[10px] font-bold uppercase tracking-wider bg-white text-black"
      >
        {{ item.cta }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import Icon from '../../components/Icon.vue'
import { suggestions } from './mock'
</script>