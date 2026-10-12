import type { Week } from '../types'

export const week3: Week = {
  id: 3,
  title: '列表：list / lindex / llength / lappend',
  emoji: '🍬',
  stage: '基础 Tcl',
  runtime: 'browser',
  bigIdea:
    '列表像一串用空格隔开的糖果。可以数有几颗（llength）、拿第几颗（lindex，从 0 开始！）、再加一颗（lappend）。',
  goals: [
    '会创建列表',
    '会用 lindex 取元素（记住从 0 数）',
    '会用 llength 数长度',
    '会用 lappend 追加',
  ],
  concepts: [
    {
      title: 'list：创建列表',
      metaphor: '可以想成：一串用空格隔开的糖果',
      body: 'set fruits [list 苹果 香蕉 橙子] 做出水果清单。命令名是 list。',
      code: 'set fruits [list 苹果 香蕉 橙子]\nputs $fruits',
    },
    {
      title: 'lindex：取第几个元素',
      metaphor: '从 0 开始数：第 1 个下标是 0',
      body: 'lindex $fruits 0 拿到第一个元素。',
      code: 'puts [lindex $fruits 0]',
    },
    {
      title: 'llength / lappend',
      metaphor: '数长度 / 往末尾追加',
      body: 'llength 返回个数；lappend 往列表末尾加元素。',
      code: 'lappend fruits 葡萄\nputs [llength $fruits]',
    },
  ],
  days: [
    { day: 'Day 1', goal: '水果清单', task: '创建并打印列表' },
    { day: 'Day 2', goal: '取元素', task: '打印第 1、2、最后一项' },
    { day: 'Day 3', goal: '数长度', task: '打印共有 N 种' },
    { day: 'Day 4', goal: '追加', task: 'lappend 两种新水果' },
    { day: 'Day 5', goal: '课表', task: '今日课表小作品' },
  ],
  mistakes: [
    {
      symptom: '拿到的不是想要的那一项',
      cause: '忘记从 0 开始数',
      fix: '第 1 个用 lindex $L 0',
    },
  ],
  checklist: ['会创建列表', '会 lindex / llength / lappend', '完成课表作品'],
  nextPreview: '第 4 周：if 判断 + for/foreach 循环。',
  examples: [
    {
      id: '01',
      title: '水果清单',
      focus: '创建 list',
      success: '打印水果',
      code: `set fruits [list 苹果 香蕉 橙子]
puts $fruits
`,
    },
    {
      id: '02',
      title: '取第几个',
      focus: 'lindex',
      success: '打印指定水果',
      code: `set fruits [list 苹果 香蕉 橙子 葡萄]
puts "第1个：[lindex $fruits 0]"
puts "第2个：[lindex $fruits 1]"
puts "最后：[lindex $fruits 3]"
`,
    },
    {
      id: '03',
      title: '数一数',
      focus: 'llength',
      success: '打印个数',
      code: `set fruits [list 苹果 香蕉 橙子]
set n [llength $fruits]
puts "共有 $n 种水果"
`,
    },
    {
      id: '04',
      title: '再加两颗',
      focus: 'lappend',
      success: '列表变长',
      code: `set fruits [list 苹果 香蕉]
lappend fruits 橙子 葡萄
puts $fruits
puts "现在有 [llength $fruits] 种"
`,
    },
    {
      id: '05',
      title: '颜色列表',
      focus: '练习',
      success: '打印喜欢的颜色',
      code: `set colors [list 红 橙 黄 绿 蓝]
puts "彩虹开头：[lindex $colors 0]"
puts "一共 [llength $colors] 种颜色"
`,
    },
    {
      id: '10',
      title: '今日课表（本周作品）',
      focus: '列表综合',
      success: '打印第几节课',
      code: `# 10_schedule.tcl
set lessons [list 语文 数学 英语 体育 美术]
puts "===== 今日课表 ====="
puts "第1节：[lindex $lessons 0]"
puts "第2节：[lindex $lessons 1]"
puts "第3节：[lindex $lessons 2]"
puts "第4节：[lindex $lessons 3]"
puts "第5节：[lindex $lessons 4]"
puts "一共 [llength $lessons] 节课"
puts "===================="
`,
    },
  ],
}
