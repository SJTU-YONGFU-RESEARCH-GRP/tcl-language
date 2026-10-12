import type { Week } from '../types'

export const week4: Week = {
  id: 4,
  title: '条件与循环：if / for / foreach / while',
  emoji: '🔁',
  stage: '基础 Tcl',
  runtime: 'browser',
  bigIdea:
    '程序可以判断（如果下雨就带伞），也可以重复做事（把每颗糖果都尝一遍）。本周学 if、for、foreach、while。',
  goals: [
    '会写 if / else',
    '会用 foreach 遍历列表',
    '会用 for 数数',
    '会用 while 重复到条件结束',
  ],
  concepts: [
    {
      title: 'if / else：条件分支',
      metaphor: '生活里可以说「如果下雨就带伞」；代码里请写 if，不要写成中文「如果」',
      body: '条件写在花括号里；成立就执行后面大括号里的命令。还可以配合 else / elseif。',
      code: 'if {$score >= 60} {\n  puts "Pass"\n} else {\n  puts "Fail"\n}',
    },
    {
      title: 'foreach：遍历列表',
      metaphor: '把列表里每一项依次处理一遍',
      body: '写法：foreach 变量名 列表 { 身体 }',
      code: 'foreach f {苹果 香蕉} {\n  puts $f\n}',
    },
    {
      title: 'for / while：循环',
      metaphor: '重复执行，直到条件结束',
      body: 'for 适合固定次数；while 适合「条件还成立就继续」。',
      code: 'for {set i 1} {$i <= 5} {incr i} {\n  puts $i\n}',
    },
  ],
  days: [
    { day: 'Day 1', goal: '及格判断', task: '分数 Pass/Fail' },
    { day: 'Day 2', goal: 'foreach', task: '遍历水果' },
    { day: 'Day 3', goal: 'for', task: '打印 1 到 10' },
    { day: 'Day 4', goal: 'while', task: '倒数发射' },
    { day: 'Day 5', goal: '小游戏', task: '猜数字骨架' },
  ],
  mistakes: [
    {
      symptom: '条件好像总不对',
      cause: '比较写错或忘了 $',
      fix: '写成 if {$score >= 60} { ... }',
    },
  ],
  checklist: ['会 if', '会 foreach 或 for', '完成一个小循环作品'],
  nextPreview: '第 5 周：proc 小帮手 + 读写文件。',
  examples: [
    {
      id: '01',
      title: '及格了吗？',
      focus: 'if / else',
      success: '打印 Pass 或 Fail',
      code: `set score 85
if {$score >= 60} {
  puts "Pass"
} else {
  puts "Fail"
}
`,
    },
    {
      id: '02',
      title: '遍历水果',
      focus: 'foreach',
      success: '每种水果一行',
      code: `set fruits [list 苹果 香蕉 橙子]
foreach f $fruits {
  puts "我喜欢 $f"
}
`,
    },
    {
      id: '03',
      title: '数到 10',
      focus: 'for',
      success: '打印 1..10',
      code: `for {set i 1} {$i <= 10} {incr i} {
  puts $i
}
`,
    },
    {
      id: '04',
      title: '倒数发射',
      focus: 'while',
      success: '5..1 然后发射',
      code: `set n 5
while {$n >= 1} {
  puts $n
  incr n -1
}
puts "发射！"
`,
    },
    {
      id: '05',
      title: '偶数打印',
      focus: 'if + for',
      success: '只打印偶数',
      code: `for {set i 1} {$i <= 10} {incr i} {
  if {[expr {$i % 2}] == 0} {
    puts "$i 是偶数"
  }
}
`,
    },
    {
      id: '10',
      title: '猜数字（本周作品）',
      focus: '条件综合',
      success: '根据猜测打印提示',
      code: `# 10_guess.tcl — 改 set guess 试不同数字
set secret 7
set guess 5

puts "我想了一个 1-10 的数字"
if {$guess == $secret} {
  puts "答对了！"
} elseif {$guess < $secret} {
  puts "太小了"
} else {
  puts "太大了"
}
`,
    },
  ],
}
