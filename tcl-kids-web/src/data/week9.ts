import type { Week } from '../types'

export const week9: Week = {
  id: 9,
  title: '查询 API：peek / topcell / cells / layers',
  emoji: '🔍',
  stage: 'CalibreDRV',
  runtime: 'local',
  bigIdea:
    '不只会画，还要会问：这张图有哪些房间（cells）？哪些彩纸（layers）？大门牌叫什么（topcell）？layout peek 还能隔着窗户偷看。',
  goals: [
    '会 layout create $gds 打开文件',
    '会 $L topcell / cells / layers / bbox',
    '认识 layout peek',
    '写出一份 GDS 报告脚本',
  ],
  concepts: [
    {
      title: '打开图纸',
      metaphor: '把作业本从书包拿出来',
      body: 'set L [layout create $gds -dt_expand]',
      code: 'set L [layout create my.gds -dt_expand]',
    },
    {
      title: '查询 API',
      metaphor: '问图纸问题',
      body: 'topcell、cells、layers、exists、bbox',
      code: 'puts [$L topcell]\nputs [$L cells]',
    },
    {
      title: 'peek 偷看',
      metaphor: '隔着窗户数房间',
      body: '不完整加载也能列 cell/layer',
      code: 'puts [layout peek $gds -cells]',
    },
  ],
  days: [
    { day: 'Day 1', goal: 'inspect', task: '跑 inspect_gds.tcl' },
    { day: 'Day 2', goal: '查询', task: 'topcell/cells/layers' },
    { day: 'Day 3', goal: 'exists+bbox', task: '友好提示' },
    { day: 'Day 4', goal: 'peek 对比', task: 'peek vs create' },
    { day: 'Day 5', goal: '报告', task: 'report_gds.tcl' },
  ],
  mistakes: [
    {
      symptom: '找不到 GDS',
      cause: '路径不对',
      fix: '先用第 8 周生成的 tmp/*.gds',
    },
  ],
  checklist: ['能打开自己的 GDS', '用 ≥4 个查询 API 打报告'],
  nextPreview: '第 10 周：create ref 做层次，完成毕业作品。',
  examples: [
    {
      id: '01',
      title: 'peek 偷看',
      focus: 'layout peek',
      success: '列出 cells/layers',
      localCommand: 'make week9-01',
      code: `set gds "tmp/week8_box.gds"
puts "peek cells:  [layout peek $gds -cells]"
puts "peek layers: [layout peek $gds -layers]"
puts "peek top:    [layout peek $gds -topcell]"
exit
`,
    },
    {
      id: '02',
      title: '打开并查询',
      focus: '$L 查询',
      success: '打印 topcell 等',
      localCommand: 'make week9-02',
      code: `set gds "tmp/week8_box.gds"
set L [layout create $gds -dt_expand]
puts "topcell=[$L topcell]"
puts "cells=[$L cells]"
puts "layers=[$L layers]"
exit
`,
    },
    {
      id: '03',
      title: 'exists + bbox',
      focus: '判断与包围盒',
      success: '有 TOP 就打印 bbox',
      localCommand: 'make week9-03',
      code: `set gds "tmp/week8_box.gds"
set L [layout create $gds -dt_expand]
if {[$L exists cell TOP]} {
  puts "bbox TOP = [$L bbox TOP]"
} else {
  puts "没有叫 TOP 的房间"
}
exit
`,
    },
    {
      id: '10',
      title: 'GDS 报告（作品）',
      focus: '综合查询',
      success: '一份完整报告',
      localCommand: 'make week9-10',
      code: `set gds "tmp/week8_multi.gds"
puts "===== GDS 报告 ====="
puts "文件：$gds"
puts "peek cells:  [layout peek $gds -cells]"
puts "peek layers: [layout peek $gds -layers]"
set L [layout create $gds -dt_expand]
puts "topcell=[$L topcell]"
puts "cells=[$L cells]"
puts "layers=[$L layers]"
if {[$L exists cell TOP]} {
  puts "bbox TOP = [$L bbox TOP]"
}
puts "===== 报告结束 ====="
exit
`,
    },
  ],
}
