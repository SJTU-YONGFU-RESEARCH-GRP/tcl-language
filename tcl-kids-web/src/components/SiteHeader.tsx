import { Link, NavLink } from 'react-router-dom'
import { loadProgress } from '../lib/progress'
import { weeks } from '../data/weeks'

export function SiteHeader() {
  const progress = loadProgress()
  const totalDone = Object.keys(progress.completed).length
  const totalExamples = weeks.reduce((n, w) => n + w.examples.length, 0)

  return (
    <header className="site-header">
      <Link to="/" className="brand">
        <span className="brand-mark" aria-hidden>
          Tcl
        </span>
        <span className="brand-text">Tcl 小课堂</span>
      </Link>
      <nav className="nav">
        <NavLink to="/roadmap">路线图</NavLink>
        <NavLink to="/glossary">小词典</NavLink>
        <NavLink to="/help">给大人</NavLink>
      </nav>
      <div className="stars-pill" title="已完成的例题">
        ⭐ {totalDone}/{totalExamples}
      </div>
    </header>
  )
}
