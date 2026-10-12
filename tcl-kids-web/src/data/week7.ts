import type { Week } from '../types'

export const week7: Week = {
  id: 7,
  title: 'layout create 与句柄（handle）',
  emoji: '📄',
  stage: 'CalibreDRV',
  runtime: 'local',
  bigIdea:
    'Calibre 里的 layout 用起来就像对象：layout create 很像 Pet new，返回的句柄存进 $L，之后写 $L 方法名 ...。本周在实验室跑脚本，网站只帮你读懂。',
  goals: [
    '理解句柄（handle）是什么',
    '会写 layout create 并 puts $L',
    '会对照 OOP：$L create cell ≈ 对象做事',
    '能在实验室用 make / calibredrv 跑通',
  ],
  concepts: [
    {
      title: '句柄像名片',
      metaphor: '拿到图纸的编号，以后都用这个编号说话',
      body: 'set L [layout create] 得到句柄；之后都写 $L ...',
      code: 'set L [layout create]\nputs "handle=$L"',
    },
    {
      title: 'OOP 对照',
      metaphor: '模具做出玩具 / 拿出空白图纸',
      body: 'Pet new ↔ layout create；$cat speak ↔ $L create cell',
      code: '$L create cell TOP\n$L create layer 1',
    },
  ],
  days: [
    { day: 'Day 1', goal: '环境', task: '大人确认 calibredrv 可用' },
    { day: 'Day 2', goal: '跑示例', task: 'hello_calibre.tcl' },
    { day: 'Day 3', goal: '空 layout', task: '打印句柄' },
    { day: 'Day 4', goal: '对照表', task: 'Pet vs layout' },
    { day: 'Day 5', goal: '小作品', task: '自我介绍 + 空 layout' },
  ],
  mistakes: [
    {
      symptom: '网站里点运行没反应 / 提示实验室',
      cause: 'Calibre 不能在浏览器里跑',
      fix: '复制代码到实验室，用 make week7-01',
    },
  ],
  checklist: ['能解释句柄', '实验室能跑通脚本'],
  nextPreview: '第 8 周：画 polygon / wire / text，并写出 GDS。',
  examples: [
    {
      id: '01',
      title: '创建空 layout',
      focus: 'layout create',
      success: '打印句柄',
      localCommand: 'make week7-01',
      expectedOutput: 'handle=...（一串内部名字）',
      code: `# 需要 calibredrv（实验室）
set L [layout create]
puts "handle=$L"
puts "我拿到了一张空白图纸！"
exit
`,
    },
    {
      id: '02',
      title: '建 cell 和 layer',
      focus: '对象方法',
      success: '创建 TOP 与层',
      localCommand: 'make week7-02',
      expectedOutput: '创建 cell/layer 无报错',
      code: `set L [layout create]
$L create cell TOP
$L create layer 1
puts "已创建 cell TOP 和 layer 1"
exit
`,
    },
    {
      id: '03',
      title: 'OOP 对照打印',
      focus: '概念巩固',
      success: '理解对照',
      localCommand: 'make week7-03',
      code: `puts "Pet new          <->  layout create"
puts "\\$cat speak      <->  \\$L create cell"
set L [layout create]
puts "我的图纸句柄：$L"
exit
`,
    },
    {
      id: '10',
      title: '打招呼 + 空图纸（作品）',
      focus: '综合',
      success: '介绍自己并创建 layout',
      localCommand: 'make week7-10',
      code: `puts "===== 第7周作品 ====="
puts "我是小明，今天学习 layout create"
set L [layout create]
puts "空白图纸句柄：$L"
puts "下次要在上面画画！"
exit
`,
    },
  ],
}
