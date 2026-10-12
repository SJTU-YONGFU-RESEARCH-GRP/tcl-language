const KEY = 'tcl-kids-progress-v1'

export type ProgressState = {
  completed: Record<string, boolean> // `${week}-${exampleId}`
  unlockedWeek: number
}

function defaultState(): ProgressState {
  return { completed: {}, unlockedWeek: 1 }
}

export function loadProgress(): ProgressState {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return defaultState()
    const parsed = JSON.parse(raw) as ProgressState
    return {
      completed: parsed.completed ?? {},
      unlockedWeek: parsed.unlockedWeek ?? 1,
    }
  } catch {
    return defaultState()
  }
}

export function saveProgress(state: ProgressState): void {
  localStorage.setItem(KEY, JSON.stringify(state))
}

export function exampleKey(week: number, exampleId: string): string {
  return `${week}-${exampleId}`
}

export function markComplete(week: number, exampleId: string, totalExamples: number): ProgressState {
  const state = loadProgress()
  state.completed[exampleKey(week, exampleId)] = true
  const doneCount = Object.keys(state.completed).filter((k) => k.startsWith(`${week}-`)).length
  // Unlock next week after finishing at least half, or the week project (id starting with 10)
  if (doneCount >= Math.min(5, totalExamples) || exampleId.startsWith('10')) {
    state.unlockedWeek = Math.max(state.unlockedWeek, week + 1)
  }
  saveProgress(state)
  return state
}

export function isWeekUnlocked(week: number, state: ProgressState): boolean {
  return week <= state.unlockedWeek
}

export function weekStars(week: number, exampleIds: string[], state: ProgressState): number {
  return exampleIds.filter((id) => state.completed[exampleKey(week, id)]).length
}
