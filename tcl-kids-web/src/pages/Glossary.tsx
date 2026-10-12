const terms = [
  { word: '脚本（.tcl）', meaning: '给电脑的「任务清单」。把命令写进文件，以后还能再跑。' },
  { word: 'puts', meaning: '请电脑把一句话打印到屏幕上。' },
  { word: '注释 #', meaning: '给自己看的小纸条，电脑会忽略。' },
  { word: '变量', meaning: '带标签的盒子。set 放进去，$ 取出来。' },
  { word: '列表 list', meaning: '一串用空格隔开的糖果。可以数、拿、再加。' },
  { word: 'if', meaning: '条件分支命令。成立时执行大括号里的代码；常配合 else / elseif。生活里可以说「如果……就……」，代码里请写 if。' },
  { word: '循环', meaning: '重复做事：for / foreach / while。' },
  { word: 'proc', meaning: '小帮手：训练好以后喊名字就会干活。' },
  { word: '类（class）', meaning: '玩具的模具图纸。' },
  { word: '对象（object）', meaning: '按模具做出的真玩具。' },
  { word: '方法（method）', meaning: '玩具会做的动作。' },
  { word: '句柄 handle', meaning: '图纸的名片编号。拿到 $L 以后才能跟它说话。' },
  { word: 'layout', meaning: '芯片版图（一张可以画画的图纸）。' },
  { word: 'GDS', meaning: '把画好的版图存成文件，方便以后打开看。' },
]

export function Glossary() {
  return (
    <main className="page">
      <header className="page-head">
        <h1>小词典</h1>
        <p>遇到不懂的词，先来这里看一眼比喻解释。</p>
      </header>
      <dl className="glossary-list">
        {terms.map((t) => (
          <div key={t.word} className="glossary-item">
            <dt>{t.word}</dt>
            <dd>{t.meaning}</dd>
          </div>
        ))}
      </dl>
    </main>
  )
}
