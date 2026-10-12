import type { Week } from '../types'

export const week10: Week = {
  id: 10,
  title: '毕业作品：层次 create ref',
  emoji: '🎓',
  stage: 'CalibreDRV',
  runtime: 'local',
  bigIdea:
    '大图纸可以由小房间拼起来：create ref 把一个 cell「放」进另一个 cell。毕业作品要组合创建 + 几何 + 查询三类 API。',
  goals: [
    '理解 cell 引用（placement）',
    '会 create ref',
    '组合创建、几何、查询完成毕业作品',
    '写出自己的 GDS',
  ],
  concepts: [
    {
      title: 'create ref',
      metaphor: '把小积木摆进大盒子',
      body: '在父 cell 里引用子 cell，并可指定坐标。',
      code: '$L create ref TOP CHILD 0 0',
    },
    {
      title: '毕业检查',
      metaphor: '交出作品并自检',
      body: '创建 → 画画 → gdsout → 再查询确认。',
      code: 'puts [$L cells]\nputs [$L layers]',
    },
  ],
  days: [
    { day: 'Day 1', goal: '学 ref', task: '最小 create ref' },
    { day: 'Day 2', goal: '两层结构', task: 'CHILD + TOP' },
    { day: 'Day 3', goal: '加几何', task: '子 cell 里画图' },
    { day: 'Day 4', goal: '自检', task: '查询报告' },
    { day: 'Day 5', goal: '毕业', task: 'my_graduation.tcl' },
  ],
  mistakes: [
    {
      symptom: 'ref 了不存在的 cell',
      cause: '子 cell 还没创建',
      fix: '先 create cell CHILD，再 create ref',
    },
  ],
  checklist: ['会 create ref', '毕业 GDS 能打开并查询'],
  nextPreview: '恭喜毕业！可回到实验室仓库继续加分题（iterator 等）。',
  examples: [
    {
      id: '01',
      title: '最小引用',
      focus: 'create ref',
      success: 'TOP 引用 CHILD',
      localCommand: 'make week10-01',
      code: `set L [layout create]
$L units microns 1000
$L create cell CHILD
$L create cell TOP
$L create layer 1.0
$L create polygon CHILD 1.0 0 0 50 50
$L create ref TOP CHILD 0 0
$L gdsout tmp/week10_ref.gds TOP
puts "已写出带引用的 GDS"
exit
`,
    },
    {
      id: '02',
      title: '摆两次积木',
      focus: '多个 ref',
      success: '同一 CHILD 放两处',
      localCommand: 'make week10-02',
      code: `set L [layout create]
$L units microns 1000
$L create cell CHILD
$L create cell TOP
$L create layer 1.0
$L create polygon CHILD 1.0 0 0 40 40
$L create ref TOP CHILD 0 0
$L create ref TOP CHILD 60 0
$L gdsout tmp/week10_two.gds TOP
puts "两块积木摆好了"
exit
`,
    },
    {
      id: '10',
      title: '毕业作品',
      focus: '创建+几何+查询',
      success: '完整毕业 GDS',
      localCommand: 'make week10-10',
      expectedOutput: 'tmp/week10_graduation.gds + 报告',
      code: `# 10_graduation.tcl — 请改成你的名字与图案
set L [layout create]
$L units microns 1000
$L create cell BADGE
$L create cell TOP
$L create layer 1.0
$L create layer 2.0

# 几何
$L create polygon BADGE 1.0 0 0 80 80
$L create text BADGE 2.0 10 90 "TCL"
$L create ref TOP BADGE 0 0
$L create ref TOP BADGE 100 0

$L gdsout tmp/week10_graduation.gds TOP
puts "===== 毕业报告 ====="
puts "cells=[$L cells]"
puts "layers=[$L layers]"
puts "topcell=[$L topcell]"
puts "文件：tmp/week10_graduation.gds"
puts "恭喜毕业！"
exit
`,
    },
  ],
}
