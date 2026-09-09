<template>
  <div class="h-full w-full flex flex-col bg-neutral-950 border border-white/15 min-h-0">
    <!-- Toolbar -->
    <div class="h-11 flex items-center gap-3 px-3 border-b border-white/15 shrink-0">
      <Icon name="tasks" :size="15" class="text-white" />
      <h2 class="text-[11px] font-bold tracking-[0.22em] text-white uppercase sora">Tasks</h2>
      <span class="text-[10px] text-zinc-500 tabular-nums">{{ tasks.length }}</span>

      <div class="ml-auto flex items-center gap-2 shrink-0">
        <input
          v-model="query"
          type="text"
          placeholder="Search…"
          class="h-8 w-36 px-2.5 bg-transparent border border-white/15 text-white text-[11px] placeholder:text-zinc-500 outline-none"
        />
        <button
          class="h-8 px-3 flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider bg-white text-black"
          @click="openCreate"
        >
          <Icon name="plus" :size="14" />
          <span class="hidden sm:inline">New</span>
        </button>
      </div>
    </div>

    <!-- Filter tabs -->
    <div class="flex items-center gap-px bg-white/10 px-1 py-1 shrink-0">
      <button
        v-for="f in filters"
        :key="f.id"
        class="px-3 h-7 text-[10px] font-bold uppercase tracking-wider"
        :class="filter === f.id ? 'bg-white text-black' : 'bg-neutral-900 text-white hover:bg-neutral-800'"
        @click="filter = f.id"
      >
        {{ f.label }}<span class="ml-1.5 text-[9px] tabular-nums opacity-70">{{ countFor(f.id) }}</span>
      </button>
    </div>

    <!-- List -->
    <div class="flex-1 overflow-y-auto min-h-0">
      <!-- error -->
      <div
        v-if="error"
        class="mx-3 my-3 px-3 py-2 border border-white/15 bg-neutral-900 text-[11px] text-zinc-300"
      >
        <span class="font-bold text-white uppercase tracking-wider text-[10px] mr-2">API unreachable</span>
        {{ error }} — start the backend (uv run python -m syfu.main) and refresh.
      </div>

      <!-- loading -->
      <div v-else-if="loading" class="py-10 text-center text-[11px] text-zinc-500 uppercase tracking-widest">
        Loading…
      </div>

      <!-- empty -->
      <div v-else-if="visibleTasks.length === 0" class="py-12 flex flex-col items-center gap-3 text-zinc-500">
        <Icon name="listChecks" :size="26" />
        <p class="text-[12px] text-zinc-400">No tasks {{ query ? 'matching &quot;' + query + '&quot;' : 'here' }}.</p>
      </div>

      <!-- rows -->
      <div
        v-for="(task, i) in visibleTasks"
        :key="task.id"
        v-motion
        class="flex items-start gap-3 px-3 py-2.5 border-b border-white/[0.08] bg-neutral-950"
        :class="task.completed ? 'opacity-60' : ''"
        :initial="{ opacity: 0, y: 10 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.35, delay: Math.min(i * 0.04, 0.3) }"
      >
        <!-- complete toggle -->
        <button
          class="w-5 h-5 shrink-0 flex items-center justify-center border border-white/30"
          :class="task.completed ? 'bg-white text-black' : 'text-white'"
          :title="task.completed ? 'Mark incomplete' : 'Mark complete'"
          @click="toggleComplete(task)"
        >
          <Icon :name="task.completed ? 'circleCheck' : 'circle'" :size="15" />
        </button>

        <!-- body -->
        <div class="min-w-0 flex-1">
          <p class="text-[13px] font-semibold text-white truncate">{{ task.title }}</p>
          <p v-if="task.description" class="text-[11px] text-zinc-400 line-clamp-2">{{ task.description }}</p>
          <div v-if="task.assocDate || task.deadline" class="mt-1 flex items-center gap-2 text-[10px] tabular-nums text-zinc-500">
            <span v-if="task.deadline">
              <Icon name="clock" :size="11" class="mr-1 inline" />{{ formatDate(task.deadline) }}
            </span>
            <span v-if="task.assocDate">
              <Icon name="calendarDays" :size="11" class="mr-1 inline" />{{ formatDate(task.assocDate) }}
            </span>
          </div>
        </div>

        <!-- meta + actions -->
        <div class="flex items-center gap-2 shrink-0">
          <span
            class="px-1.5 py-0.5 text-[8px] font-bold uppercase tracking-widest"
            :class="prioClass(task.priority)"
          >{{ labelFor(task.priority) }}</span>
          <button class="w-6 h-6 flex items-center justify-center border border-white/15 text-white" title="Edit" @click="openEdit(task)">
            <Icon name="pencil" :size="12" />
          </button>
          <button class="w-6 h-6 flex items-center justify-center border border-white/15 text-white" title="Delete" @click="removeTask(task)">
            <Icon name="trash" :size="12" />
          </button>
        </div>
      </div>
    </div>
<!-- Create / Edit form -->
    <transition name="slide">
      <form
        v-if="formOpen"
        class="flex flex-wrap items-end gap-2 px-3 py-2.5 border-t border-white/15 bg-neutral-950"
        @submit.prevent="submit"
      >
        <div class="flex flex-col min-w-0">
          <label class="text-[8px] uppercase tracking-widest text-zinc-500 mb-0.5">Title</label>
          <input v-model="draft.title" required type="text" class="h-8 w-40 px-2 bg-transparent border border-white/20 text-white text-[11px] outline-none" />
        </div>
        <div class="flex flex-col min-w-0">
          <label class="text-[8px] uppercase tracking-widest text-zinc-500 mb-0.5">Description</label>
          <input v-model="draft.description" type="text" class="h-8 w-44 px-2 bg-transparent border border-white/20 text-white text-[11px] outline-none" />
        </div>
        <div class="flex flex-col">
          <label class="text-[8px] uppercase tracking-widest text-zinc-500 mb-0.5">Priority</label>
          <select v-model="draft.priority" class="h-8 px-2 bg-neutral-900 border border-white/20 text-white text-[11px] outline-none">
            <option value="important">Important</option>
            <option value="do_it">Do it</option>
            <option value="chill">Chill</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label class="text-[8px] uppercase tracking-widest text-zinc-500 mb-0.5">Assoc date</label>
          <input v-model="draft.assocDate" type="datetime-local" class="h-8 px-2 bg-transparent border border-white/20 text-white text-[10px] outline-none" />
        </div>
        <div class="flex flex-col">
          <label class="text-[8px] uppercase tracking-widest text-zinc-500 mb-0.5">Deadline</label>
          <input v-model="draft.deadline" type="datetime-local" class="h-8 px-2 bg-transparent border border-white/20 text-white text-[10px] outline-none" />
        </div>
        <button type="submit" class="h-8 px-3 flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider bg-white text-black" :disabled="busy">
          {{ editing ? 'Save' : 'Create' }}
        </button>
        <button type="button" class="h-8 px-2.5 text-[10px] font-bold uppercase tracking-wider border border-white/20 text-white" @click="closeForm" :disabled="busy">
          Cancel
        </button>
      </form>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import Icon from '../../components/Icon.vue'
import {
  createTasks,
  deleteTasks,
  listTasks,
  setTaskCompleted,
  updateTasks,
  type Priority,
  type Task,
} from '../../lib/tasksApi'

// ---------------------------------------------------------------------------
// View state
// ---------------------------------------------------------------------------
const tasks = ref<Task[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const query = ref('')
const busy = ref(false)

const filters = [
  { id: 'all', label: 'All' },
  { id: 'active', label: 'Active' },
  { id: 'done', label: 'Done' },
] as const
const filter = ref<'all' | 'active' | 'done'>('all')

const visibleTasks = computed(() => {
  const q = query.value.trim().toLowerCase()
  let list = tasks.value
  if (q) list = list.filter((t) => t.title.toLowerCase().includes(q))
  if (filter.value === 'active') list = list.filter((t) => !t.completed)
  if (filter.value === 'done') list = list.filter((t) => t.completed)
  return list
})

const countFor = (id: 'all' | 'active' | 'done') =>
  id === 'all'
    ? tasks.value.length
    : id === 'active'
      ? tasks.value.filter((t) => !t.completed).length
      : tasks.value.filter((t) => t.completed).length

// ---------------------------------------------------------------------------
// Loading
// ---------------------------------------------------------------------------
async function load() {
  loading.value = true
  error.value = null
  try {
    tasks.value = await listTasks()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
    tasks.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)

// ---------------------------------------------------------------------------
// Row actions
// ---------------------------------------------------------------------------
async function toggleComplete(task: Task) {
  const prev = task.completed
  task.completed = !prev // optimistic
  try {
    await setTaskCompleted(task.id, !prev)
  } catch (e) {
    task.completed = prev
    error.value = e instanceof Error ? e.message : String(e)
  }
}

async function removeTask(task: Task) {
  if (!window.confirm(`Delete "${task.title}"?`)) return
  busy.value = true
  try {
    await deleteTasks([task.id])
    tasks.value = tasks.value.filter((t) => t.id !== task.id)
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    busy.value = false
  }
}

// ---------------------------------------------------------------------------
// Create / Edit form
// ---------------------------------------------------------------------------
const editing = ref<Task | null>(null)
const formOpen = ref(false)
const draft = reactive({
  title: '',
  description: '',
  priority: 'chill' as Priority,
  assocDate: '',
  deadline: '',
})

function openCreate() {
  editing.value = null
  draft.title = ''
  draft.description = ''
  draft.priority = 'chill'
  draft.assocDate = ''
  draft.deadline = ''
  formOpen.value = true
}

function openEdit(task: Task) {
  editing.value = task
  draft.title = task.title
  draft.description = task.description ?? ''
  draft.priority = task.priority
  draft.assocDate = dtToInput(task.assocDate)
  draft.deadline = dtToInput(task.deadline)
  formOpen.value = true
}

function closeForm() {
  formOpen.value = false
  editing.value = null
}

const dtToInput = (v: string | null) => (v && v.length >= 16 ? v.slice(0, 16) : '')
const inputToDt = (v: string) => (v ? v + ':00' : null)

async function submit() {
  busy.value = true
  error.value = null
  try {
    if (editing.value) {
      await updateTasks([
        {
          id: editing.value.id,
          title: draft.title,
          description: draft.description || null,
          priority: draft.priority,
          assocDate: inputToDt(draft.assocDate),
          deadline: inputToDt(draft.deadline),
        },
      ])
    } else {
      const created = await createTasks([
        {
          title: draft.title,
          description: draft.description || null,
          priority: draft.priority,
          assocDate: inputToDt(draft.assocDate),
          deadline: inputToDt(draft.deadline),
        },
      ])
      tasks.value = [...tasks.value, ...created]
    }
    closeForm()
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    busy.value = false
  }
}

// ---------------------------------------------------------------------------
// Presentation helpers
// ---------------------------------------------------------------------------
const labelFor = (p: Priority) =>
  ({ important: 'Important', do_it: 'Do it', chill: 'Chill' })[p]

const prioClass = (p: Priority) =>
  ({
    important: 'bg-white text-black',
    do_it: 'bg-zinc-300 text-black',
    chill: 'bg-black text-white border border-white/50',
  })[p]

function formatDate(iso: string): string {
  const d = new Date(iso)
  if (isNaN(d.getTime())) return iso
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${pad(d.getMonth() + 1)}/${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}
</script>