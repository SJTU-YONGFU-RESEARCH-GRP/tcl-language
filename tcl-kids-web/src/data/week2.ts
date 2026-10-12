import type { Week } from '../types'

export const week2: Week = {
  id: 2,
  title: '变量与字符串：set / $ / expr',
  emoji: '📦',
  stage: '基础 Tcl',
  runtime: 'browser',
  bigIdea:
    '变量像带标签的盒子：set 把东西放进去，$ 把东西取出来。改盒子里的内容，同一份脚本就能打印不同结果。',
  goals: [
    '会用 set 存名字、数字',
    '会用 $变量名 取出来打印',
    '会用 expr 做简单加减',
    '完成「成绩单」小作品',
  ],
  concepts: [
    {
      title: 'set：给变量赋值',
      metaphor: '可以想成：给盒子贴标签 name，再放进内容',
      body: '命令是 set。写 set name "小明" 之后，变量 name 的值就是「小明」。',
      code: 'set name "小明"\nputs $name',
    },
    {
      title: '$：取出变量的值',
      metaphor: '可以想成：打开贴着 name 标签的盒子',
      body: '在双引号里写 $name，Tcl 会替换成变量里的值。命令名旁边请保留 $，不要改成中文。',
      code: 'puts "我的名字是 $name"',
    },
    {
      title: 'expr：做算术',
      metaphor: '可以想成：请计算器帮忙算一算',
      body: '年龄 +1 要写：expr {$age + 1}（花括号里写算式更安全）。',
      code: 'set age 10\nputs [expr {$age + 1}]',
    },
  ],
  days: [
    { day: 'Day 1', goal: '三个变量', task: '名字、学校、年级' },
    { day: 'Day 2', goal: '拼句子', task: 'puts "My name is $name"' },
    { day: 'Day 3', goal: '改值', task: '改变量再打印，观察变化' },
    { day: 'Day 4', goal: '算术', task: '用 expr 算年龄+1' },
    { day: 'Day 5', goal: '成绩单', task: '三门课分数 + 总分' },
  ],
  mistakes: [
    {
      symptom: '打印出 $name 而不是名字',
      cause: '用了花括号包住整句，或漏了 $',
      fix: '用双引号："你好 $name"',
    },
    {
      symptom: 'can\'t read "name"',
      cause: '还没 set 就用了 $name',
      fix: '先 set name "..."',
    },
  ],
  checklist: [
    '我会 set 和 $',
    '我会拼一句话',
    '我会用 expr 做加减',
    '我完成了成绩单',
  ],
  nextPreview: '第 3 周学列表：一串用空格隔开的糖果。',
  examples: [
    {
      id: '01',
      title: '一个变量',
      focus: 'set + puts',
      success: '打印出名字',
      code: `set name "小明"
puts $name
`,
    },
    {
      id: '02',
      title: '三个变量',
      focus: '多个盒子',
      success: '打印名字、学校、年级',
      code: `set name "小明"
set school "实验小学"
set grade "四年级"
puts $name
puts $school
puts $grade
`,
    },
    {
      id: '03',
      title: '用 $ 拼句子',
      focus: '双引号里的变量',
      success: '一句完整自我介绍',
      code: `set name "小明"
set age 10
puts "我的名字是 $name，今年 $age 岁。"
`,
    },
    {
      id: '04',
      title: '改变量',
      focus: '观察变化',
      success: '前后打印不同',
      code: `set color "蓝色"
puts "以前喜欢 $color"
set color "绿色"
puts "现在喜欢 $color"
`,
    },
    {
      id: '05',
      title: '年龄 +1',
      focus: 'expr',
      success: '打印明年年龄',
      code: `set age 10
set next [expr {$age + 1}]
puts "今年 $age 岁，明年 $next 岁。"
`,
    },
    {
      id: '06',
      title: '拼接两段文字',
      focus: '字符串拼接',
      success: '拼成一句话',
      code: `set hello "你好"
set who "同学"
puts "$hello，$who！"
`,
    },
    {
      id: '09',
      title: '简单算术',
      focus: '加减乘',
      success: '算出结果',
      code: `set a 3
set b 5
puts "和 = [expr {$a + $b}]"
puts "积 = [expr {$a * $b}]"
`,
    },
    {
      id: '10',
      title: '成绩单（本周作品）',
      focus: '变量 + expr',
      success: '三门课与总分',
      code: `# 10_report_card.tcl — 请改成你的分数
set name "小明"
set math 95
set chinese 90
set english 88
set total [expr {$math + $chinese + $english}]

puts "===== 成绩单 ====="
puts "姓名：$name"
puts "数学：$math"
puts "语文：$chinese"
puts "英语：$english"
puts "总分：$total"
puts "=================="
`,
    },
  ],
}
