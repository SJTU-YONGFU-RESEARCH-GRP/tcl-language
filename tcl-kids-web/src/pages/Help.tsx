import { Link } from 'react-router-dom'

export function Help() {
  return (
    <main className="page">
      <header className="page-head">
        <h1>给家长 / 老师</h1>
        <p>孩子负责写脚本、看结果；大人负责环境与陪伴节奏。</p>
      </header>

      <section className="panel">
        <h2>这个网站做什么</h2>
        <ul>
          <li>用中文、生活比喻讲解 Tcl（面向几乎零基础）。</li>
          <li>
            第 1–6 周：浏览器内可点「运行」（教学用 Tcl 子集，不是完整 tclsh）。
          </li>
          <li>
            第 7–10 周：讲解 Calibre DESIGNrev；真正跑脚本请用实验室仓库。
          </li>
        </ul>
      </section>

      <section className="panel">
        <h2>和参考仓库的关系</h2>
        <p>
          课程内容改编自{' '}
          <a
            href="https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language"
            target="_blank"
            rel="noreferrer"
          >
            SJTU-YONGFU-RESEARCH-GRP/tcl-language
          </a>
          。完整讲义、Makefile、calibredrv 脚本仍以该仓库为准。
        </p>
        <pre className="code-block">{`# 在实验室仓库根目录
make help
make week1-01          # 第 1–6 周：tclsh
make week7-01          # 第 7–10 周：calibredrv
make help-tcl
make help-calibre`}</pre>
      </section>

      <section className="panel">
        <h2>家里练习（第 1–6 周）</h2>
        <ol>
          <li>安装 Tcl，确认终端能运行 <code>tclsh</code>。</li>
          <li>也可以先只在本网站练习，再迁移到本地文件。</li>
          <li>Day 2 之后尽量不要替孩子打字：练的是「修改 → 运行 → 看输出」。</li>
        </ol>
      </section>

      <section className="panel">
        <h2>实验室（第 7–10 周）</h2>
        <ul>
          <li>需要已配置的 <code>calibredrv</code> 环境（见仓库 setup 脚本）。</li>
          <li>孩子写脚本；GUI / VNC 打开 GDS 由大人协助验收。</li>
          <li>卡壳顺序：跑最小例题 → 看报错 → 查本周讲义 → 查手册 HTML TOC。</li>
        </ul>
      </section>

      <p>
        <Link className="btn btn-primary" to="/roadmap">
          查看路线图
        </Link>
      </p>
    </main>
  )
}
