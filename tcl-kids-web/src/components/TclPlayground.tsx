import { useEffect, useState } from 'react'
import type { Example, RuntimeMode } from '../types'
import { runTcl } from '../lib/tclRunner'

type Props = {
  example: Example
  runtime: RuntimeMode
  weekId: number
  onSuccess?: () => void
}

export function TclPlayground({ example, runtime, weekId, onSuccess }: Props) {
  const [code, setCode] = useState(example.code)
  const [output, setOutput] = useState('')
  const [error, setError] = useState('')
  const [status, setStatus] = useState<'idle' | 'ok' | 'err'>('idle')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    setCode(example.code)
    setOutput('')
    setError('')
    setStatus('idle')
  }, [example.id, example.code, weekId])

  function handleRun() {
    if (runtime === 'local') {
      setStatus('idle')
      setError('')
      setOutput(
        [
          '这一周需要在实验室用 Calibre 运行（浏览器里跑不了芯片工具）。',
          '',
          example.localCommand
            ? `推荐命令：${example.localCommand}`
            : '请在 tcl-language 仓库里按讲义运行。',
          example.expectedOutput ? `\n预期结果：${example.expectedOutput}` : '',
          '',
          '你可以先点「复制代码」，粘贴到实验室脚本里。',
        ].join('\n'),
      )
      setStatus('ok')
      onSuccess?.()
      return
    }

    const result = runTcl(code)
    if (result.ok) {
      setOutput(result.output || '(没有打印内容——试试加一行 puts)')
      setError('')
      setStatus('ok')
      onSuccess?.()
    } else {
      setOutput(result.output)
      setError(result.error ?? '出错了')
      setStatus('err')
    }
  }

  function handleReset() {
    setCode(example.code)
    setOutput('')
    setError('')
    setStatus('idle')
  }

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div className="playground">
      <div className="playground-toolbar">
        <span className="runtime-badge" data-mode={runtime}>
          {runtime === 'browser' ? '浏览器里运行' : '实验室运行'}
        </span>
        <div className="toolbar-actions">
          {runtime === 'browser' ? (
            <button type="button" className="btn btn-primary" onClick={handleRun}>
              运行
            </button>
          ) : (
            <button type="button" className="btn btn-primary" onClick={handleRun}>
              查看怎么跑
            </button>
          )}
          <button type="button" className="btn btn-ghost" onClick={handleReset}>
            重置
          </button>
          <button type="button" className="btn btn-ghost" onClick={handleCopy}>
            {copied ? '已复制' : '复制代码'}
          </button>
        </div>
      </div>

      <label className="editor-label" htmlFor="tcl-editor">
        在这里改代码（先改一个字再运行！）
      </label>
      <textarea
        id="tcl-editor"
        className="editor"
        spellCheck={false}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={14}
      />

      <div className={`output-panel status-${status}`}>
        <div className="output-title">屏幕输出</div>
        {error ? <pre className="output-error">{error}</pre> : null}
        <pre className="output-body">{output || '点「运行」看看电脑说什么…'}</pre>
        {status === 'ok' ? <div className="celebrate">太棒了！⭐ 已记上一颗星</div> : null}
      </div>
    </div>
  )
}
