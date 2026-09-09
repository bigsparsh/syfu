// ---------------------------------------------------------------------------
// Mock data powering the dashboard. No backend is wired up yet (AGENTS.md),
// so these fixtures stand in for the data the task tools / API would return.
// ---------------------------------------------------------------------------

export type Priority = 'important' | 'do_it' | 'chill'

export interface GanttTask {
  id: string
  title: string
  /** Start time in minutes from the Gantt start hour. */
  start: number
  /** End time in minutes from the Gantt start hour. */
  end: number
  priority: Priority
  /** Human-friendly time range, e.g. "08:00 – 09:00". */
  detail: string
  /** Longer description surfaced in the hover tooltip. */
  desc: string
}

export interface Stat {
  label: string
  value: string
  sub: string
  icon: string
}

export interface Suggestion {
  id: string
  icon: string
  title: string
  body: string
  cta: string
}

/** The Gantt chart runs from this hour of the day until `endHour`. */
export const ganttStartHour = 8
export const ganttEndHour = 18
export const ganttSpan = ganttEndHour - ganttStartHour // hours

export const ganttTasks: GanttTask[] = [
  { id: 'g1', title: 'Deep work block', start: 0, end: 60, priority: 'important', detail: '08:00 – 09:00', desc: 'Heads-down focus on the calendar graph. No Slack, no email.' },
  { id: 'g2', title: 'Review pull requests', start: 75, end: 120, priority: 'do_it', detail: '09:15 – 10:00', desc: '3 open PRs from the tasks router branch need a look.' },
  { id: 'g3', title: 'Standup + planning', start: 120, end: 150, priority: 'chill', detail: '10:00 – 10:30', desc: 'Team sync, then set priorities for the day.' },
  { id: 'g4', title: 'Ship task endpoints', start: 150, end: 240, priority: 'important', detail: '10:30 – 12:00', desc: 'Wire create/update/delete through the tools and push the router.' },
  { id: 'g5', title: 'Lunch', start: 240, end: 270, priority: 'chill', detail: '12:00 – 12:30', desc: 'Walk + lunch break, out of the office.' },
  { id: 'g6', title: 'Design review', start: 300, end: 360, priority: 'do_it', detail: '13:00 – 14:00', desc: 'Walk through the new Gantt tooltip interactions with design.' },
  { id: 'g7', title: 'Framing notes', start: 390, end: 450, priority: 'do_it', detail: '14:30 – 15:30', desc: 'Turn the design feedback into actionable follow-ups.' },
  { id: 'g8', title: 'Write docs', start: 480, end: 540, priority: 'important', detail: '16:00 – 17:00', desc: 'Draft the API reference for the task endpoints.' },
]

export const stats: Stat[] = [
  { label: 'Tasks done', value: '12', sub: 'of 18 this week', icon: 'check' },
  { label: 'In progress', value: '4', sub: '2 need attention', icon: 'listChecks' },
  { label: 'Focus time', value: '5.5h', sub: '+ 40 min vs avg', icon: 'timer' },
  { label: 'Streak', value: '9', sub: 'days in a row', icon: 'target' },
]

export const suggestions: Suggestion[] = [
  {
    id: 's1',
    icon: 'sparkles',
    title: 'Push deadline for Homework to Friday',
    body: 'You have 2 empty focus blocks in the afternoon. Reserving one now keeps your evening free.',
    cta: 'Reschedule',
  },
  {
    id: 's2',
    icon: 'lightbulb',
    title: 'Batch your shallow tasks together',
    body: 'Reviewing PRs and emails back-to-back saves ~25 min of context switching today.',
    cta: 'Add block',
  },
  {
    id: 's3',
    icon: 'timer',
    title: 'Take a focus break at 15:30',
    body: 'You have been in deep work since 10:30. A 20 min walk usually boosts your next block.',
    cta: 'Remind me',
  },
  {
    id: 's4',
    icon: 'trendingUp',
    title: 'Wrap up the day at 17:00',
    body: 'Based on your schedule, ending on time today protects tomorrow’s deep work block.',
    cta: 'Lock in',
  },
]