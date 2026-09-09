<template>
  <span
    class="bw-icon"
    :style="{ fontSize: size + 'px' }"
    role="img"
    aria-hidden="true"
    v-html="markup"
  ></span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import home from 'lucide-static/icons/home.svg?raw'
import listTodo from 'lucide-static/icons/list-todo.svg?raw'
import folder from 'lucide-static/icons/folder.svg?raw'
import calendarDays from 'lucide-static/icons/calendar-days.svg?raw'
import lightbulb from 'lucide-static/icons/lightbulb.svg?raw'
import messageSquare from 'lucide-static/icons/message-square.svg?raw'
import barChart from 'lucide-static/icons/bar-chart-3.svg?raw'
import panelLeftClose from 'lucide-static/icons/panel-left-close.svg?raw'
import panelLeft from 'lucide-static/icons/panel-left.svg?raw'
import timer from 'lucide-static/icons/timer.svg?raw'
import target from 'lucide-static/icons/target.svg?raw'
import sparkles from 'lucide-static/icons/sparkles.svg?raw'
import check from 'lucide-static/icons/check.svg?raw'
import listChecks from 'lucide-static/icons/list-checks.svg?raw'
import chevronsLeft from 'lucide-static/icons/chevrons-left.svg?raw'
import clock from 'lucide-static/icons/clock-1.svg?raw'
import trendingUp from 'lucide-static/icons/trending-up.svg?raw'
import arrowUpRight from 'lucide-static/icons/arrow-up-right.svg?raw'
import inbox from 'lucide-static/icons/inbox.svg?raw'
import activity from 'lucide-static/icons/activity.svg?raw'
import x from 'lucide-static/icons/x.svg?raw'
import menu from 'lucide-static/icons/menu.svg?raw'
import plus from 'lucide-static/icons/plus.svg?raw'
import pencil from 'lucide-static/icons/pencil.svg?raw'
import trash from 'lucide-static/icons/trash.svg?raw'
import search from 'lucide-static/icons/search.svg?raw'
import circle from 'lucide-static/icons/circle.svg?raw'
import circleCheck from 'lucide-static/icons/circle-check.svg?raw'

const ICONS: Record<string, string> = {
  home,
  tasks: listTodo,
  projects: folder,
  timetable: calendarDays,
  suggestions: lightbulb,
  chat: messageSquare,
  analytics: barChart,
  collapse: panelLeftClose,
  expand: panelLeft,
  timer,
  target,
  sparkles,
  check,
  listChecks,
  chevronsLeft,
  clock,
  trendingUp,
  arrowUpRight,
  inbox,
  activity,
  x,
  menu,
  plus,
  pencil,
  trash,
  search,
  circle,
  circleCheck,
}

const props = defineProps<{ name: string; size?: number }>()

const markup = computed(() => ICONS[props.name] ?? ICONS.home)
</script>

<style scoped>
.bw-icon {
  display: inline-flex;
  line-height: 1;
  color: currentColor;
}
.bw-icon :deep(svg) {
  width: 1em;
  height: 1em;
}
</style>