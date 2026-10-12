import type { Week } from '../types'

export const week1: Week = {
  id: 1,
  title: 'puts 与脚本：让电脑打印文字',
  emoji: '💬',
  stage: '基础 Tcl',
  runtime: 'browser',
  bigIdea:
    '电脑像听话的机器人：你写什么，它就做什么。本周只练「说话」——用 puts 打印文字，并把命令存进 .tcl 文件。',
  goals: [
    '用 puts 把文字打印到屏幕',
    '知道 .tcl 脚本像「任务清单」',
    '会写 # 注释（给自己看的小纸条）',
    '完成一张自我介绍卡',
  ],
  concepts: [
    {
      title: 'puts = 把字打印出来',
      metaphor: '对机器人说：「请把这句话说出来」',
      body: '先写 puts，空一格，再用英文双引号包住要说的话。拼写必须正好是 puts（小写）。',
      code: 'puts "Hello, I am learning Tcl!"',
    },
    {
      title: '.tcl 文件就是脚本',
      metaphor: '一张可以反复执行的任务清单',
      body: '把好多行命令写进文件，保存后再运行。明天打开还能看见全部内容。',
      code: 'puts "第一行"\nputs "第二行"',
    },
    {
      title: '# 注释',
      metaphor: '给自己看的小纸条，电脑会忽略',
      body: '以 # 开头的整行不会执行。好注释说明「这段在做什么」。',
      code: '# 打印欢迎语\nputs "你好！"',
    },
  ],
  days: [
    { day: 'Day 1', goal: '证明能跑', task: '运行 01，看到 Hello 那一行' },
    { day: 'Day 2', goal: '介绍自己', task: '改 02，打印名字、年龄、颜色' },
    { day: 'Day 3', goal: '更长脚本', task: '完成五行 puts（例题 03）' },
    { day: 'Day 4', goal: '注释', task: '给重要段落加 # 说明' },
    { day: 'Day 5', goal: '本周作品', task: '做自我介绍卡（例题 10）' },
  ],
  mistakes: [
    {
      symptom: 'extra characters after close-quote',
      cause: '引号不成对',
      fix: '数一数 "，每段文字只留一对',
    },
    {
      symptom: 'invalid command name',
      cause: '命令拼错（Puts / put）',
      fix: '改成小写 puts',
    },
    {
      symptom: '方括号 [ ] 报错',
      cause: 'Tcl 把 [ ] 当「先执行」',
      fix: '用花括号：puts {[ ] 项目}',
    },
  ],
  checklist: [
    '我会用 puts 打印自己选的文字',
    '我知道脚本是 .tcl 文件',
    '我会写有用的 # 注释',
    '我完成了自己的介绍卡',
  ],
  nextPreview: '第 2 周学变量：带标签的盒子。set name "小明" 把字放进去，$name 取出来。',
  examples: [
    {
      id: '01',
      title: '第一次打招呼',
      focus: '第一个 puts',
      success: '屏幕打印一行 Hello',
      code: `# 01_hello.tcl — 第一次打招呼
puts "Hello, I am learning Tcl!"
`,
    },
    {
      id: '02',
      title: '关于我',
      focus: '多行介绍',
      success: '打印出三行事实',
      code: `# 02_about_me.tcl — 请改成你自己的信息
puts "我的名字是小明。"
puts "我今年 10 岁。"
puts "我喜欢的颜色是蓝色。"
`,
    },
    {
      id: '03',
      title: '五行脚本',
      focus: '从上到下执行',
      success: '五行按顺序全部出现',
      code: `# 03_five_lines.tcl
puts "第 1 行：今天开始学 Tcl"
puts "第 2 行：电脑会听我的话"
puts "第 3 行：一行一行往下跑"
puts "第 4 行：我可以改文字再跑"
puts "第 5 行：完成！"
`,
    },
    {
      id: '04',
      title: '加上注释',
      focus: '# 注释',
      success: '输出正确，注释解释文件',
      code: `# 04_with_comments.tcl
# 页眉：标题
puts "==== 我的笔记 ===="

# 正文：今天学到的
puts "今天学会了 puts"
puts "注释是给自己看的"

# 页脚
puts "==== 结束 ===="
`,
    },
    {
      id: '05',
      title: '空行使段落清晰',
      focus: '可读性',
      success: '输出分成清楚段落',
      code: `# 05_blank_lines.tcl
puts "早上"
puts "吃早餐"

puts "中午"
puts "去学校"

puts "晚上"
puts "写 Tcl 练习"
`,
    },
    {
      id: '06',
      title: '字符画小猫',
      focus: '用字符画画',
      success: '出现小猫图形',
      code: `# 06_ascii_art.tcl
puts " /\\_/\\"
puts "( o.o )"
puts " > ^ <"
puts "  小猫"
`,
    },
    {
      id: '07',
      title: '购物清单',
      focus: '编号清单版式',
      success: '标题、条目、页脚都打印',
      code: `# 07_shopping_list.tcl
puts "===== 购物清单 ====="
puts "1. 苹果"
puts "2. 牛奶"
puts "3. 面包"
puts "===================="
`,
    },
    {
      id: '08',
      title: '三行小故事',
      focus: '开头 / 中间 / 结尾',
      success: '故事结构完整',
      code: `# 08_story_three_lines.tcl
puts "从前有个小朋友打开了电脑。"
puts "他输入 puts，屏幕立刻说话了。"
puts "从此他爱上了 Tcl！"
`,
    },
    {
      id: '09',
      title: '菜单卡片',
      focus: '用符号做边框',
      success: '菜单卡清晰可读',
      code: `# 09_menu_card.tcl
puts "+------------------+"
puts "|   今日菜单       |"
puts "| 1. 米饭          |"
puts "| 2. 青菜          |"
puts "| 3. 汤            |"
puts "+------------------+"
`,
    },
    {
      id: '10',
      title: '自我介绍卡（本周作品）',
      focus: '完整小作品',
      success: '改成你自己的信息',
      code: `# 10_self_intro_card.tcl — 本周作品：请改成你的信息！
# 页眉
puts "========================"
puts "      自我介绍卡"
puts "========================"

# 正文
puts "姓名：小明"
puts "学校：实验小学"
puts "年龄：10"
puts "爱好：画画 / Tcl"
puts "我想学会：让电脑听我的话"

# 页脚
puts "========================"
puts "Tcl 第 1 周 · 完成！"
`,
    },
    {
      id: '11',
      title: '不加换行（加分）',
      focus: 'puts -nonewline',
      success: 'Loading... 在同一行',
      code: `# 11_puts_without_newline.tcl
puts -nonewline "Loading"
puts -nonewline "."
puts -nonewline "."
puts -nonewline "."
puts " 完成！"
`,
    },
    {
      id: '12',
      title: '检查清单与方括号',
      focus: '用 {} 原样打印 [ ]',
      success: '方框正确显示',
      code: `# 12_run_checklist.tcl
puts "今天的检查清单："
puts {[ ] 打开网站}
puts {[ ] 跑通例题 01}
puts {[x] 学会 puts}
puts "真棒！"
`,
    },
  ],
}
