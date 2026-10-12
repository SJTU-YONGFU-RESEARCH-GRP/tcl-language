# Tcl 小课堂（`tcl-kids-web`）

面向几乎零基础小学生的 **中文 Tcl 互动教学网站**（Vite + React）。

> 与仓库根目录 [`website/`](../website/)（MkDocs 讲义站）是 **并行的另一套前端**：本目录强调浏览器内点「运行」、生活比喻讲解；课程内容改编自本仓库 `PLAN.md` / `lessons/`。

- **作者 / 分支贡献**：[@xingguangyaoyu](https://github.com/xingguangyaoyu)
- 第 1–6 周：浏览器里点「运行」（教学用 Tcl 子集，不是完整 `tclsh`）
- 第 7–10 周：Calibre 讲义 + 复制代码到实验室用 `make weekN-XX` 运行

## 本地查看

```bash
cd tcl-kids-web
npm install
npm run dev
```

终端会打印本地地址（一般是 `http://localhost:5173`）。用浏览器打开即可。

## 常用页面

| 地址 | 内容 |
|------|------|
| `/` | 首页 |
| `/roadmap` | 10 周路线图 |
| `/week/1` | 第 1 周讲义 |
| `/week/1/example/01` | 第 1 周例题（可点运行） |
| `/glossary` | 小词典 |
| `/help` | 给家长 / 老师 |

## 构建静态网站

```bash
npm run build
npm run preview
```

`dist/` 可部署到静态托管。`node_modules/` 与 `dist/` 已 gitignore。

## 说明

- 浏览器运行器覆盖课程常用命令（`puts` / `set` / `expr` / list / `if` / 循环 / `proc` / 简易 TclOO）。
- 标题与概念名 **保留英文 Tcl 命令**，中文只做解释（避免把 `if` 硬译成「如果……就……」这类标题）。
- Calibre / `calibredrv` 无法在浏览器中运行。
