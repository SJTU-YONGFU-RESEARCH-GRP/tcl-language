import type { Week } from '../types'
import { week1 } from './week1'
import { week2 } from './week2'
import { week3 } from './week3'
import { week4 } from './week4'
import { week5 } from './week5'
import { week6 } from './week6'
import { week7 } from './week7'
import { week8 } from './week8'
import { week9 } from './week9'
import { week10 } from './week10'

export const weeks: Week[] = [
  week1,
  week2,
  week3,
  week4,
  week5,
  week6,
  week7,
  week8,
  week9,
  week10,
]

export function getWeek(id: number): Week | undefined {
  return weeks.find((w) => w.id === id)
}

export function getExample(weekId: number, exampleId: string) {
  const week = getWeek(weekId)
  if (!week) return undefined
  const example = week.examples.find((e) => e.id === exampleId)
  if (!example) return undefined
  return { week, example }
}
