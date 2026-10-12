import { Link } from 'react-router-dom'
import { useMemo, useState } from 'react'
import { weeks } from '../data/weeks'
import { isWeekUnlocked, loadProgress, weekStars } from '../lib/progress'

export function Roadmap() {
  const [tick, setTick] = useState(0)
  const progress = useMemo(() => loadProgress(), [tick])

  return (
    <main className="page">
      <header className="page-head">
        <h1>10 周路线图</h1>
        <p>从「电脑说话」走到「画出自己的芯片小图」。完成几道例题就会解锁下一周。</p>
        <button type="button" className="btn btn-ghost" onClick={() => setTick((t) => t + 1)}>
          刷新进度
        </button>
      </header>

      <ol className="roadmap-list">
        {weeks.map((week) => {
          const unlocked = isWeekUnlocked(week.id, progress)
          const stars = weekStars(
            week.id,
            week.examples.map((e) => e.id),
            progress,
          )
          return (
            <li key={week.id} className={unlocked ? 'week-card' : 'week-card locked'}>
              <div className="week-card-top">
                <span className="week-emoji" aria-hidden>
                  {week.emoji}
                </span>
                <div>
                  <p className="week-stage">{week.stage}</p>
                  <h2>
                    第 {week.id} 周 · {week.title}
                  </h2>
                </div>
              </div>
              <p className="week-idea">{week.bigIdea}</p>
              <div className="week-card-meta">
                <span>
                  ⭐ {stars}/{week.examples.length}
                </span>
                <span>{week.runtime === 'browser' ? '浏览器可运行' : '实验室 Calibre'}</span>
              </div>
              {unlocked ? (
                <Link className="btn btn-primary" to={`/week/${week.id}`}>
                  进入本周
                </Link>
              ) : (
                <span className="lock-note">先完成上一周的几道例题再来～</span>
              )}
            </li>
          )
        })}
      </ol>
    </main>
  )
}
