import type { Week } from '../types'

export const week8: Week = {
  id: 8,
  title: '在图纸上画画：polygon / wire / text',
  emoji: '✏️',
  stage: 'CalibreDRV',
  runtime: 'local',
  bigIdea:
    '选好房间（cell）和彩纸（layer），用点连出形状（polygon），还能画小路（wire）和写名字（text），最后 gdsout 存成 GDS。',
  goals: [
    '会 create cell / layer',
    '会 create polygon（坐标是一个个数字）',
    '会 create text（加分：wire）',
    '会 gdsout 写出文件',
  ],
  concepts: [
    {
      title: 'cell / layer',
      metaphor: '房间 / 透明彩纸',
      body: '先建 cell 和 layer，再在上面画。',
      code: '$L create cell TOP\n$L create layer 1.0',
    },
    {
      title: 'polygon 坐标',
      metaphor: '用点连形状',
      body: '坐标必须展开成数字；若是 list，可用 eval。',
      code: '$L create polygon TOP 1 0 0 100 100',
    },
    {
      title: 'gdsout 保存',
      metaphor: '把画好的图存进书包',
      body: '$L gdsout tmp/my.gds TOP',
      code: '$L gdsout tmp/week8.gds TOP',
    },
  ],
  days: [
    { day: 'Day 1', goal: '跑通方块', task: 'examples/create_box.tcl' },
    { day: 'Day 2', goal: '改尺寸', task: '试不同层号写法' },
    { day: 'Day 3', goal: '加文字', task: 'create text' },
    { day: 'Day 4', goal: '加导线', task: 'create wire' },
    { day: 'Day 5', goal: '作品', task: 'polygon + text 写出 GDS' },
  ],
  mistakes: [
    {
      symptom: 'polygon 参数错误',
      cause: '坐标还包在一层 list 里',
      fix: '展开数字，或 eval $L create polygon ... $coords',
    },
  ],
  checklist: ['会画 ≥2 种几何', '成功 gdsout'],
  nextPreview: '第 9 周：打开 GDS，用查询 API「问图纸问题」。',
  examples: [
    {
      id: '01',
      title: '画一个方块',
      focus: 'polygon + gdsout',
      success: '生成 GDS',
      localCommand: 'make week8-01',
      expectedOutput: '写出 tmp/ 下的 gds 文件',
      code: `set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create polygon TOP 1.0 0 0 100 100
$L gdsout tmp/week8_box.gds TOP
puts "已写出 tmp/week8_box.gds"
exit
`,
    },
    {
      id: '02',
      title: '方块 + 名字',
      focus: 'create text',
      success: '图上有文字',
      localCommand: 'make week8-02',
      code: `set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create polygon TOP 1.0 0 0 100 100
$L create text TOP 1.0 10 110 "HELLO"
$L gdsout tmp/week8_text.gds TOP
puts "完成：方块 + HELLO"
exit
`,
    },
    {
      id: '03',
      title: '小路 wire',
      focus: 'create wire',
      success: '画出有宽度的线',
      localCommand: 'make week8-03',
      code: `set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 2.0
$L create wire TOP 2.0 10 0 50  50 50  100 50
$L gdsout tmp/week8_wire.gds TOP
puts "完成：一条小路"
exit
`,
    },
    {
      id: '10',
      title: '多图形作品',
      focus: 'polygon + text (+ wire)',
      success: '组合写出 GDS',
      localCommand: 'make week8-10',
      code: `set L [layout create]
$L units microns 1000
$L create cell TOP
$L create layer 1.0
$L create layer 2.0
$L create polygon TOP 1.0 0 0 100 100
$L create wire TOP 2.0 10 0 50  50 50  100 50
$L create text TOP 1.0 10 110 "MYCHIP"
$L gdsout tmp/week8_multi.gds TOP
puts "毕业小图：tmp/week8_multi.gds"
exit
`,
    },
  ],
}
