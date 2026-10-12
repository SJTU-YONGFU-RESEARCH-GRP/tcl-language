import type { Week } from '../types'

export const week5: Week = {
  id: 5,
  title: 'proc 与文件：自定义命令',
  emoji: '🛠️',
  stage: '基础 Tcl',
  runtime: 'browser',
  bigIdea:
    'proc 像训练一只会做事的小狗：给它名字、参数和身体，以后喊名字它就干活。文件像本子：打开、写、读、合上。',
  goals: [
    '会写并调用 proc',
    '会用 return 带回结果',
    '会简单写文件 / 读文件（浏览器里用虚拟文件）',
    '完成「工具箱」小作品',
  ],
  concepts: [
    {
      title: 'proc：定义自己的命令',
      metaphor: '可以想成：训练一个会做事的小帮手',
      body: '写法：proc 名字 {参数} {身体}，然后直接写名字调用。命令名是 proc。',
      code: 'proc greet {name} {\n  puts "Hi $name!"\n}\ngreet "小明"',
    },
    {
      title: 'return：返回结果',
      metaphor: '把算好的结果交回来',
      body: '用 [命令名 参数] 接到返回值。',
      code: 'proc add {a b} {\n  return [expr {$a + $b}]\n}\nputs [add 3 4]',
    },
    {
      title: '文件读写',
      metaphor: '打开本子写字再合上',
      body: '浏览器教室里用虚拟文件练习；在电脑上则写入真正的 tmp/ 目录。',
      code: 'set f [open diary.txt w]\nputs $f "今天学了 proc"\nclose $f',
    },
  ],
  days: [
    { day: 'Day 1', goal: 'greet', task: '写问好 proc' },
    { day: 'Day 2', goal: 'add', task: '写加法并 return' },
    { day: 'Day 3', goal: '写文件', task: '写入几句话' },
    { day: 'Day 4', goal: '读文件', task: '读回并打印' },
    { day: 'Day 5', goal: '工具箱', task: '至少 3 个 proc' },
  ],
  mistakes: [
    {
      symptom: 'invalid command name "greet"',
      cause: '还没定义就调用，或名字拼错',
      fix: '先写 proc greet ... 再调用',
    },
  ],
  checklist: ['会写 proc', '会 return', '完成工具箱'],
  nextPreview: '第 6 周 OOP：模具（类）做出真玩具（对象）。',
  examples: [
    {
      id: '01',
      title: '问好小帮手',
      focus: 'proc',
      success: '打印 Hi',
      code: `proc greet {name} {
  puts "Hi $name!"
}
greet "小明"
greet "同学"
`,
    },
    {
      id: '02',
      title: '加法小帮手',
      focus: 'return',
      success: '打印 7',
      code: `proc add {a b} {
  return [expr {$a + $b}]
}
puts "3+4=[add 3 4]"
`,
    },
    {
      id: '03',
      title: '打印列表',
      focus: 'proc + foreach',
      success: '逐项打印',
      code: `proc printList {items} {
  foreach x $items {
    puts "- $x"
  }
}
printList [list 铅笔 橡皮 尺子]
`,
    },
    {
      id: '04',
      title: '写日记',
      focus: 'open / puts / close',
      success: '写入虚拟文件',
      code: `set f [open diary.txt w]
puts $f "今天学会了 proc"
puts $f "明天要学 OOP"
close $f
puts "已写入 diary.txt"
`,
    },
    {
      id: '05',
      title: '读日记',
      focus: 'gets',
      success: '读回内容',
      code: `set f [open diary.txt w]
puts $f "第一行日记"
puts $f "第二行日记"
close $f

set f [open diary.txt r]
set line1 [gets $f]
set line2 [gets $f]
close $f
puts "读到：$line1"
puts "读到：$line2"
`,
    },
    {
      id: '10',
      title: '工具箱（本周作品）',
      focus: '多个 proc',
      success: '至少 3 个小帮手',
      code: `# 10_toolbox.tcl
proc greet {name} {
  puts "你好，$name！"
}
proc add {a b} {
  return [expr {$a + $b}]
}
proc showList {items} {
  puts "清单："
  foreach x $items {
    puts " * $x"
  }
}

greet "小明"
puts "2+5 = [add 2 5]"
showList [list 作业 跑步 读 Tcl]
`,
    },
  ],
}
