<template>
  <div class="w-full lg:h-full flex flex-col lg:flex-row gap-2">
    <!-- Left (lg): timetable as a Gantt chart (30% of width, full height) -->
    <div class="w-full lg:w-[30%] lg:min-w-[280px] lg:h-full shrink-0 h-[360px]">
      <GanttChart class="h-full" />
    </div>

    <!-- Right (lg): vertical 30/70 split (stats on top, suggestions below) -->
    <div class="w-full lg:flex-1 min-w-0 flex flex-col gap-2">
      <!-- top (lg): stats -->
      <div class="flex flex-col border border-white/15 h-[200px] lg:h-[30%] min-h-[96px]">
        <div class="flex items-center gap-2 h-9 px-3 border-b border-white/15 bg-neutral-950">
          <Icon name="activity" :size="14" class="text-white" />
          <h3 class="text-[10px] font-bold uppercase tracking-[0.22em] text-white sora">Overview</h3>
          <span class="ml-auto text-[9px] text-zinc-500">this week</span>
        </div>
        <StatsPanel class="flex-1" />
      </div>

      <!-- bottom (lg): suggestions -->
      <div class="flex flex-col border border-white/15 flex-1 min-h-[240px]">
        <div class="flex items-center gap-2 h-9 px-3 border-b border-white/15 bg-neutral-950">
          <Icon name="suggestions" :size="14" class="text-white" />
          <h3 class="text-[10px] font-bold uppercase tracking-[0.22em] text-white sora">Suggestions</h3>
          <span class="ml-auto text-[9px] text-zinc-500">generated from your day</span>
        </div>
        <SuggestionsPanel class="flex-1" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Icon from '../../components/Icon.vue'
import GanttChart from './GanttChart.vue'
import StatsPanel from './StatsPanel.vue'
import SuggestionsPanel from './SuggestionsPanel.vue'
</script>