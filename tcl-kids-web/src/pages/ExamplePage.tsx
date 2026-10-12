import { Link, useParams } from 'react-router-dom'
import { useState } from 'react'
import { getExample } from '../data/weeks'
import { TclPlayground } from '../components/TclPlayground'
import { markComplete } from '../lib/progress'

export function ExamplePage() {
  const { weekId, exampleId } = useParams()
  const data = getExample(Number(weekId), String(exampleId))
  const [justStarred, setJustStarred] = useState(false)

  if (!data) {
    return (
      <main className="page">
        <h1>找不到这道例题</h1>
        <Link to="/roadmap">回路线图</Link>
      </main>
    )
  }

  const { week, example } = data
  const idx = week.examples.findIndex((e) => e.id === example.id)
  const prev = week.examples[idx - 1]
  const next = week.examples[idx + 1]

  return (
    <main className="page example-page">
      <header className="page-head">
        <p className="eyebrow">
          <Link to={`/week/${week.id}`}>第 {week.id} 周</Link> · 例题 {example.id}
        </p>
        <h1>{example.title}</h1>
        <p className="lead">
          练习重点：{example.focus}。怎样算成功：{example.success}
        </p>
        {justStarred ? <p className="celebrate">已记录进度 ⭐</p> : null}
      </header>

      <TclPlayground
        weekId={week.id}
        example={example}
        runtime={week.runtime}
        onSuccess={() => {
          markComplete(week.id, example.id, week.examples.length)
          setJustStarred(true)
        }}
      />

      <nav className="example-nav">
        {prev ? (
          <Link to={`/week/${week.id}/example/${prev.id}`}>← {prev.id} {prev.title}</Link>
        ) : (
          <span />
        )}
        <Link to={`/week/${week.id}`}>回本周讲义</Link>
        {next ? (
          <Link to={`/week/${week.id}/example/${next.id}`}>
            {next.id} {next.title} →
          </Link>
        ) : week.id < 10 ? (
          <Link to={`/week/${week.id + 1}`}>下一周 →</Link>
        ) : (
          <Link to="/roadmap">看完整路线图</Link>
        )}
      </nav>
    </main>
  )
}
