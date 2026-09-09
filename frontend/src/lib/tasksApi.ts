// ---------------------------------------------------------------------------
// Typed client for the backend task API (proxied through `/api` in dev).
// Mirror of the FastAPI router in backend/src/syfu/api/routers/tasks.py.
// ---------------------------------------------------------------------------

export type Priority = 'important' | 'do_it' | 'chill'

export interface Task {
  id: string
  title: string
  description: string | null
  assocDate: string | null
  deadline: string | null
  priority: Priority
  completed: boolean
}

export interface TaskDraft {
  title: string
  description?: string | null
  assocDate?: string | null
  deadline?: string | null
  priority?: Priority
  completed?: boolean
}

export interface TaskUpdate {
  id: string
  title?: string | null
  description?: string | null
  assocDate?: string | null
  deadline?: string | null
  priority?: Priority
  completed?: boolean
}

const BASE = '/api/tasks'

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    try {
      const body = await res.json()
      if (body && body.detail) detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
    } catch {
      /* non-json error body */
    }
    throw new Error(detail)
  }
  return (await res.json()) as T
}

/** GET /api/tasks — list every task. */
export async function listTasks(): Promise<Task[]> {
  return handle<Task[]>(await fetch(BASE))
}

/** GET /api/tasks/search?title=... — search tasks by title fragment(s). */
export async function searchTasks(title: string[]): Promise<Task[]> {
  const params = new URLSearchParams()
  title.forEach((t) => params.append('title', t))
  return handle<Task[]>(await fetch(`${BASE}/search?${params.toString()}`))
}

/** POST /api/tasks — create one or more tasks. */
export async function createTasks(tasks: TaskDraft[]): Promise<Task[]> {
  return handle<Task[]>(
    await fetch(BASE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tasks }),
    }),
  )
}

/** PATCH /api/tasks — update one or more existing tasks. */
export async function updateTasks(tasks: TaskUpdate[]): Promise<{ message: string }> {
  return handle<{ message: string }>(
    await fetch(BASE, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tasks),
    }),
  )
}

/** PATCH /api/tasks/:id/complete — toggle completion on a single task. */
export async function setTaskCompleted(id: string, completed: boolean): Promise<{ message: string }> {
  return handle<{ message: string }>(
    await fetch(`${BASE}/${id}/complete`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed }),
    }),
  )
}

/** DELETE /api/tasks — delete tasks by their ids. */
export async function deleteTasks(ids: string[]): Promise<{ message: string }> {
  return handle<{ message: string }>(
    await fetch(BASE, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids }),
    }),
  )
}