export type RuntimeMode = 'browser' | 'local'

export interface Concept {
  title: string
  metaphor: string
  body: string
  code?: string
}

export interface DayPlan {
  day: string
  goal: string
  task: string
}

export interface MistakeTip {
  symptom: string
  cause: string
  fix: string
}

export interface Example {
  id: string
  title: string
  focus: string
  success: string
  code: string
  /** Shown when browser run is unavailable or for Calibre weeks */
  expectedOutput?: string
  localCommand?: string
}

export interface Week {
  id: number
  title: string
  emoji: string
  stage: string
  runtime: RuntimeMode
  bigIdea: string
  goals: string[]
  concepts: Concept[]
  days: DayPlan[]
  mistakes: MistakeTip[]
  examples: Example[]
  checklist: string[]
  nextPreview: string
}
