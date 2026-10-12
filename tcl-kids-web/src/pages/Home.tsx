import { Link } from 'react-router-dom'

export function Home() {
  return (
    <main className="page home">
      <section className="hero">
        <div className="hero-glow" aria-hidden />
        <p className="hero-brand">Tcl 小课堂</p>
        <h1 className="hero-title">跟电脑说话，从一行 puts 开始</h1>
        <p className="hero-sub">
          专为几乎零基础的小学生准备：生活比喻、先跑再懂、一步一个小招。
        </p>
        <div className="hero-cta">
          <Link className="btn btn-primary btn-lg" to="/week/1">
            开始第 1 周
          </Link>
          <Link className="btn btn-ghost btn-lg" to="/roadmap">
            看 10 周路线图
          </Link>
        </div>
      </section>

      <section className="home-strip">
        <div>
          <h2>先玩后懂</h2>
          <p>点运行，先看屏幕说话，再问为什么。</p>
        </div>
        <div>
          <h2>一次一个小招</h2>
          <p>今天 puts，明天变量，绝不一次塞满。</p>
        </div>
        <div>
          <h2>后面还能画芯片</h2>
          <p>第 7–10 周对接实验室 Calibre（大人帮忙开环境）。</p>
        </div>
      </section>
    </main>
  )
}
