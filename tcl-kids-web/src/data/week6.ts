import type { Week } from '../types'

export const week6: Week = {
  id: 6,
  title: 'TclOO：class / object / method',
  emoji: '🧸',
  stage: 'OOP',
  runtime: 'browser',
  bigIdea:
    '类是玩具的「模具图纸」，对象是按模具做出的真玩具，方法是玩具会做的动作。看到 $某东西 动词 ...，多半在跟对象说话。',
  goals: [
    '能用自己的话解释：类 / 对象 / 方法',
    '会写 oo::class create',
    '会 new 出对象并调用方法',
    '完成「宠物店」小作品',
  ],
  concepts: [
    {
      title: 'oo::class：定义类',
      metaphor: '可以想成：玩具的模具图纸',
      body: '写 oo::class create Pet { ... }。类（class）是模具，不是中文「类」这个字本身去当命令。',
      code: 'oo::class create Pet {\n  variable name\n  ...\n}',
    },
    {
      title: 'new：创建对象',
      metaphor: '可以想成：按模具做出一只真的猫',
      body: 'set cat [Pet new "Mimi" "cat"] 得到一个对象（object）。',
      code: 'set cat [Pet new "Mimi" "cat"]\n$cat speak',
    },
    {
      title: 'method：对象的方法',
      metaphor: '对象会做的动作',
      body: '在类里用 method 定义；调用时写 $对象 方法名。',
      code: 'method introduce {} {\n  puts "I am $name"\n}',
    },
  ],
  days: [
    { day: 'Day 1', goal: '画图理解', task: '类 vs 对象 vs 方法' },
    { day: 'Day 2', goal: '跑通 Pet', task: '照抄最小例子' },
    { day: 'Day 3', goal: '加方法', task: 'rename 改名' },
    { day: 'Day 4', goal: '新类 Robot', task: 'beep / move' },
    { day: 'Day 5', goal: '宠物店', task: '1 类 2 对象 3 方法' },
  ],
  mistakes: [
    {
      symptom: '找不到方法',
      cause: '方法名拼错，或对错了对象',
      fix: '检查 $obj 方法名 是否一致',
    },
  ],
  checklist: ['能解释类/对象/方法', '能独立跑一个 TclOO 脚本'],
  nextPreview: '第 7 周进 Calibre：layout create 很像 Pet new，$L create cell 很像 $cat speak。',
  examples: [
    {
      id: '01',
      title: '最小宠物',
      focus: 'class + new',
      success: '宠物自我介绍',
      code: `oo::class create Pet {
  variable name kind

  constructor {n k} {
    set name $n
    set kind $k
  }

  method introduce {} {
    puts "I am $name, a $kind."
  }
}

set cat [Pet new "Mimi" "cat"]
$cat introduce
`,
    },
    {
      id: '02',
      title: '会说话',
      focus: 'method + if',
      success: '猫叫 / 狗叫',
      code: `oo::class create Pet {
  variable name kind

  constructor {n k} {
    set name $n
    set kind $k
  }

  method speak {} {
    if {$kind eq "cat"} {
      puts "$name: meow!"
    } else {
      puts "$name: woof!"
    }
  }
}

set a [Pet new "Mimi" "cat"]
set b [Pet new "Buddy" "dog"]
$a speak
$b speak
`,
    },
    {
      id: '03',
      title: '改名字',
      focus: '改属性',
      success: '改名后再介绍',
      code: `oo::class create Pet {
  variable name

  constructor {n} {
    set name $n
  }

  method rename {newName} {
    set name $newName
  }

  method introduce {} {
    puts "我叫 $name"
  }
}

set p [Pet new "小花"]
$p introduce
$p rename "大花"
$p introduce
`,
    },
    {
      id: '04',
      title: '机器人',
      focus: '另一个类',
      success: 'beep 和 move',
      code: `oo::class create Robot {
  variable name

  constructor {n} {
    set name $n
  }

  method beep {} {
    puts "$name: 哔哔！"
  }

  method move {steps} {
    puts "$name 走了 $steps 步"
  }
}

set r [Robot new "R2"]
$r beep
$r move 3
`,
    },
    {
      id: '10',
      title: '宠物店（本周作品）',
      focus: '综合 OOP',
      success: '1 类 2 对象 3 方法',
      code: `# 10_pet_shop.tcl
oo::class create Pet {
  variable name kind

  constructor {n k} {
    set name $n
    set kind $k
  }

  method introduce {} {
    puts "欢迎！我是 $name（$kind）"
  }

  method speak {} {
    if {$kind eq "cat"} {
      puts "$name: meow!"
    } else {
      puts "$name: woof!"
    }
  }

  method trick {} {
    puts "$name 表演了一个小把戏！"
  }
}

puts "===== 宠物店开张 ====="
set a [Pet new "Mimi" "cat"]
set b [Pet new "Buddy" "dog"]
$a introduce
$a speak
$a trick
$b introduce
$b speak
$b trick
puts "===== 欢迎再来 ====="
`,
    },
  ],
}
