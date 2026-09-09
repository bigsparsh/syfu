<template>
  <div class="gantt flex flex-col h-full min-h-0 bg-neutral-950 border border-white/15">
    <!-- Header -->
    <div class="flex items-center justify-between px-4 h-11 border-b border-white/15 shrink-0">
      <div class="flex items-center gap-2">
        <Icon name="timetable" :size="15" class="text-white" />
        <h2 class="text-[11px] font-bold tracking-[0.22em] text-white uppercase sora">Timetable</h2>
      </div>
      <span class="text-[10px] text-zinc-400">today · aug 27</span>
    </div>

    <!-- Body -->
    <div class="relative flex-1 min-h-0 overflow-auto" @mouseleave="hideTooltip">
      <div class="flex items-stretch">
        <!-- left gutter: task labels (sticky while timeline scrolls) -->
        <div class="sticky left-0 z-20 self-stretch w-[120px] shrink-0 bg-neutral-950 border-r border-white/15">
          <div class="h-7 border-b border-white/15"></div>
          <div
            v-for="task in tasks"
            :key="task.id"
            class="flex flex-col justify-center pr-3 pl-4"
            :style="{ height: rowHeight + 'px' }"
          >
            <span class="text-[11px] text-white truncate font-medium">{{ task.title }}</span>
            <span class="text-[9px] text-zinc-500">{{ task.detail }}</span>
          </div>
        </div>

        <!-- right: scrollable time ruler + lanes -->
        <div class="shrink-0" :style="{ width: contentW + 'px' }">
          <!-- ruler (sticky on vertical scroll) -->
          <div class="sticky top-0 z-10 relative h-7 border-b border-white/15 bg-neutral-950">
            <div
              v-for="hour in hours"
              :key="hour"
              class="absolute top-0 h-full flex flex-col justify-center"
              :style="{ left: hourLeft(hour) + 'px' }"
            >
              <span class="text-[9px] text-zinc-500 -translate-x-1/2">{{ formatHour(hour) }}</span>
            </div>
          </div>

          <!-- lanes -->
          <div class="relative">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="relative"
              :style="{ height: rowHeight + 'px' }"
            >
              <!-- hour gridlines -->
              <div
                v-for="hour in hours"
                :key="hour"
                class="absolute top-0 bottom-0 border-l border-white/[0.06]"
                :style="{ left: hourLeft(hour) + 'px' }"
              ></div>

              <!-- task marker -->
              <div
                v-motion
                class="absolute top-1/2 -translate-y-1/2 cursor-pointer"
                :class="barClass(task.priority)"
                :style="{ left: barLeftPx(task) + 'px', width: barWidthPx(task) + 'px', height: markerH + 'px' }"
                :initial="{ width: '0px' }"
                :animate="{ width: barWidthPx(task) + 'px' }"
                :transition="{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.15 }"
                @mouseenter="onHover(task, $event)"
                @mousemove="onMove($event)"
              ></div>
            </div>

            <!-- now marker -->
            <div
              v-if="nowLeft !== null"
              class="absolute top-0 bottom-0 w-px bg-white z-10 pointer-events-none"
              :style="{ left: nowLeft + 'px' }"
            >
              <span class="absolute -top-0.5 -translate-x-1/2 text-[9px] bg-white text-black px-1">now</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex items-center gap-4 px-4 h-9 border-t border-white/15 shrink-0">
      <div
        v-for="l in legend"
        :key="l.label"
        class="flex items-center gap-1.5"
      >
        <span class="w-2.5 h-2.5 inline-block" :class="l.cls"></span>
        <span class="text-[9px] uppercase tracking-wider text-zinc-400">{{ l.label }}</span>
      </div>
      <span class="ml-auto text-[9px] uppercase tracking-wider text-zinc-500">hover a block for details</span>
    </div>

      <!-- Hover tooltip: fixed to viewport so scroll/clipping can't cut it -->
      <div
        v-if="hover && hover.task"
        class="fixed z-50 w-60 pointer-events-none bg-white text-black border border-black p-3"
        :style="{ left: tipX() + 'px', top: tipY() + 'px' }"
      >
        <div class="flex items-start justify-between gap-2">
          <h3 class="text-[12px] font-bold leading-tight">{{ hover.task.title }}</h3>
          <span
            class="shrink-0 mt-0.5 px-1.5 py-0.5 text-[8px] font-bold uppercase tracking-widest"
            :class="tagClass(hover.task.priority)"
          >{{ labelFor(hover.task.priority) }}</span>
        </div>
        <p class="mt-1 text-[10.5px] tabular-nums text-zinc-700">{{ hover.task.detail }}</p>
        <p class="mt-1.5 text-[11px] leading-snug text-zinc-600">{{ hover.task.desc }}</p>
      </div>
    </div>
</template>
<script setup lang="ts">
import { computed, reactive } from 'vue'
import Icon from '../../components/Icon.vue'
import { ganttEndHour, ganttStartHour, ganttSpan, ganttTasks, type Priority } from './mock'

const props = withDefaults(defineProps<{ tasks?: typeof ganttTasks }>(), {
  tasks: () => ganttTasks,
})

const rowHeight = 46
const markerH = 12

// The timeline is drawn on a fixed pixel scale so it can be scrolled
// horizontally without squashing the bars down.
const hourW = 84
const contentW = ganttSpan * hourW
const pxPerMin = contentW / (ganttSpan * 60)

const hours = computed(() => {
  const list: number[] = []
  for (let h = ganttStartHour; h <= ganttEndHour; h++) list.push(h)
  return list
})

const hourLeft = (hour: number) => (hour - ganttStartHour) * hourW
const barLeftPx = (t: { start: number }) => t.start * pxPerMin
const barWidthPx = (t: { start: number; end: number }) => (t.end - t.start) * pxPerMin

function formatHour(hour: number): string {
  const h = hour % 12 === 0 ? 12 : hour % 12
  return h + (hour >= 12 ? 'p' : 'a')
}

const barClass = (p: Priority) =>
  ({
    important: 'bg-white',
    do_it: 'bg-zinc-300',
    chill: 'bg-transparent border border-dashed border-white/60',
  })[p]

const legend = [
  { label: 'Important', cls: 'bg-white' },
  { label: 'Do it', cls: 'bg-zinc-300' },
  { label: 'Chill', cls: 'border border-dashed border-white/60' },
]

const labelMap: Record<Priority, string> = {
  important: 'Important',
  do_it: 'Do it',
  chill: 'Chill',
}
const labelFor = (p: Priority) => labelMap[p]
const tagClass = (p: Priority) =>
  ({
    important: 'bg-black text-white',
    do_it: 'bg-zinc-500 text-white',
    chill: 'bg-black text-white border border-white/70',
  })[p]

// ---------------------------------------------------------------------------
// Tooltip: fixed-position card that follows the cursor.
// ---------------------------------------------------------------------------
const hover = reactive<{ task: (typeof ganttTasks)[number] | null; x: number; y: number }>({
  task: null,
  x: 0,
  y: 0,
})

function onHover(task: (typeof ganttTasks)[number], e: MouseEvent) {
  hover.task = task
  onMove(e)
}

function onMove(e: MouseEvent) {
  hover.x = e.clientX
  hover.y = e.clientY
}

function hideTooltip() {
  hover.task = null
}

function tipX(): number {
  return Math.min(hover.x + 16, (window?.innerWidth ?? 1024) - 260)
}

function tipY(): number {
  return Math.max(hover.y - 8 - 160, 8)
}

// Position of the current time within the Gantt range (px), if midday.
const nowLeft = computed<number | null>(() => {
  const now = new Date()
  const mins = now.getHours() * 60 + now.getMinutes()
  const startMins = ganttStartHour * 60
  const spanMins = ganttSpan * 60
  if (mins < startMins || mins > startMins + spanMins) return null
  return (mins - startMins) * pxPerMin
})
</script>
