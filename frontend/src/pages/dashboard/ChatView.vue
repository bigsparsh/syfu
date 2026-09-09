<template>
  <div class="h-full w-full flex flex-col">
    <!-- mock thread header -->
    <div class="h-11 flex items-center gap-2 px-4 border-b border-white/15 shrink-0">
      <Icon name="chat" :size="15" class="text-white" />
      <h2 class="text-[11px] font-bold tracking-[0.22em] text-white uppercase sora">Assistant</h2>
      <span class="ml-auto flex items-center gap-1.5 text-[9px] uppercase tracking-wider text-zinc-500">
        <span class="w-1.5 h-1.5 bg-white inline-block"></span> online
      </span>
    </div>

    <!-- thread -->
    <div class="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3 min-h-0">
      <div
        v-for="(m, i) in messages"
        :key="i"
        v-motion
        class="max-w-[70%] px-3.5 py-2 text-[13px] leading-relaxed"
        :class="m.from === 'me'
          ? 'bg-white text-black self-end'
          : 'bg-neutral-900 border border-white/15 text-zinc-200 self-start'"
        :initial="{ opacity: 0, y: 10 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.35, delay: 0.08 * i }"
      >
        {{ m.text }}
      </div>
    </div>

    <!-- composer -->
    <div class="flex items-center gap-2 px-3 py-3 border-t border-white/15 shrink-0">
      <input
        disabled
        placeholder="Ask SYFU to plan your day…"
        class="flex-1 h-9 px-3 bg-transparent border border-white/15 text-white placeholder:text-zinc-500 outline-none"
      />
      <button class="h-9 px-4 text-[11px] font-bold uppercase tracking-wider bg-white text-black">
        Send
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import Icon from '../../components/Icon.vue'

const messages = [
  { from: 'ai', text: 'You have a light afternoon. Want me to prototype the task API endpoint?' },
  { from: 'me', text: 'Yes — start with GET /api/tasks and the create flow.' },
  { from: 'ai', text: 'Done. I built the full tasks router and wired it to the tools. It’s live under /api/tasks.' },
  { from: 'me', text: 'Nice. Can we block a focus hour for shipping it tomorrow?' },
] as const
</script>