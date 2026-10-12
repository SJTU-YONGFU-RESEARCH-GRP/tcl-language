import { Link, useParams } from 'react-router-dom'
import { getWeek } from '../data/weeks'
import { exampleKey, isWeekUnlocked, loadProgress } from '../lib/progress'

export function WeekPage() {
  const { weekId } = useParams()
  const id = Number(weekId)
  const week = getWeek(id)
  const progress = loadProgress()

  if (!week) {
    return (
      <main className="page">
        <h1>找不到这一周</h1>
        <Link to="/roadmap">回路线图</Link>
      </main>
    )
  }

  const unlocked = isWeekUnlocked(week.id, progress)

  return (
    <main className="page week-page">
      <header className="page-head">
        <p className="eyebrow">
          {week.emoji} {week.stage} ·{' '}
          {week.runtime === 'browser' ? '可在网站运行' : '实验室运行'}
        </p>
        <h1>
          第 {week.id} 周 · {week.title}
        </h1>
        <p className="lead">{week.bigIdea}</p>
        {!unlocked ? (
          <p className="lock-note">这一周还锁着。可以先浏览，完成上一周例题后会解锁星星。</p>
        ) : null}
      </header>

      <section className="panel">
        <h2>学完你能做什么</h2>
        <ul>
          {week.goals.map((g) => (
            <li key={g}>{g}</li>
          ))}
        </ul>
      </section>

      <section className="panel">
        <h2>大想法（生活比喻）</h2>
        <div className="concept-grid">
          {week.concepts.map((c) => (
            <article key={c.title} className="concept-card">
              <h3>{c.title}</h3>
              <p className="metaphor">比喻：{c.metaphor}</p>
              <p>{c.body}</p>
              {c.code ? <pre className="code-block">{c.code}</pre> : null}
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>每日练习（30～45 分钟）</h2>
        <table className="simple-table">
          <thead>
            <tr>
              <th>天</th>
              <th>目标</th>
              <th>做什么</th>
            </tr>
          </thead>
          <tbody>
            {week.days.map((d) => (
              <tr key={d.day}>
                <td>{d.day}</td>
                <td>{d.goal}</td>
                <td>{d.task}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="panel">
        <h2>例题（先跑再懂）</h2>
        <ul className="example-list">
          {week.examples.map((ex) => {
            const done = !!progress.completed[exampleKey(week.id, ex.id)]
            return (
              <li key={ex.id}>
                <Link to={`/week/${week.id}/example/${ex.id}`}>
                  <span className="ex-id">{ex.id}</span>
                  <span className="ex-title">
                    {ex.title} {done ? '⭐' : ''}
                  </span>
                  <span className="ex-focus">{ex.focus}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </section>

      <section className="panel">
        <h2>常见错误（别怕）</h2>
        <table className="simple-table">
          <thead>
            <tr>
              <th>现象</th>
              <th>常见原因</th>
              <th>怎么办</th>
            </tr>
          </thead>
          <tbody>
            {week.mistakes.map((m) => (
              <tr key={m.symptom}>
                <td>{m.symptom}</td>
                <td>{m.cause}</td>
                <td>{m.fix}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="panel">
        <h2>本周检查清单</h2>
        <ul>
          {week.checklist.map((c) => (
            <li key={c}>{c}</li>
          ))}
        </ul>
        <p className="next-preview">下一周预告：{week.nextPreview}</p>
        <div className="row-actions">
          <Link className="btn btn-primary" to={`/week/${week.id}/example/${week.examples[0].id}`}>
            从例题 {week.examples[0].id} 开始
          </Link>
          {week.id < 10 ? (
            <Link className="btn btn-ghost" to={`/week/${week.id + 1}`}>
              下一周
            </Link>
          ) : null}
        </div>
      </section>
    </main>
  )
}
