/**
 * Educational Tcl subset for kids (Weeks 1–6).
 * Not a full Tcl — covers puts/set/expr/list/if/loops/proc and a tiny TclOO.
 */

export type RunResult = {
  ok: boolean
  output: string
  error?: string
  mode: 'browser' | 'fallback'
}

type ProcDef = { args: string[]; body: string }
type ClassDef = {
  vars: string[]
  constructorArgs: string[]
  constructorBody: string
  methods: Record<string, ProcDef>
}

type ObjectInst = {
  className: string
  vars: Record<string, string>
}

class TclInterp {
  vars: Record<string, string> = {}
  procs: Record<string, ProcDef> = {}
  classes: Record<string, ClassDef> = {}
  objects: Record<string, ObjectInst> = {}
  files: Record<string, string> = {}
  output: string[] = []
  nonewline = false
  steps = 0
  maxSteps = 50_000
  objCounter = 0

  run(script: string): void {
    this.execBody(script)
  }

  private bump(): void {
    this.steps += 1
    if (this.steps > this.maxSteps) {
      throw new Error('运行太久了——可能是死循环。请检查 while / for。')
    }
  }

  private execBody(body: string): string {
    const commands = splitCommands(body)
    let last = ''
    for (const cmd of commands) {
      this.bump()
      const trimmed = stripComments(cmd).trim()
      if (!trimmed) continue
      last = this.evalCommand(trimmed)
    }
    return last
  }

  private evalCommand(cmd: string): string {
    const words = parseWords(cmd)
    if (words.length === 0) return ''

    // Object method call: $obj method args...
    if (words[0].startsWith('$') && words.length >= 2) {
      const objName = this.substWord(words[0])
      const method = words[1]
      const args = words.slice(2).map((w) => this.substWord(w))
      return this.callObjectMethod(objName, method, args)
    }

    const name = this.substWord(words[0])
    const args = words.slice(1)

    if (name === 'puts') return this.cmdPuts(args)
    if (name === 'set') return this.cmdSet(args)
    if (name === 'expr') return this.cmdExpr(args)
    if (name === 'list') return args.map((a) => this.substWord(a)).join(' ')
    if (name === 'lindex') return this.cmdLindex(args)
    if (name === 'llength') return this.cmdLlength(args)
    if (name === 'lappend') return this.cmdLappend(args)
    if (name === 'if') return this.cmdIf(args)
    if (name === 'for') return this.cmdFor(args)
    if (name === 'foreach') return this.cmdForeach(args)
    if (name === 'while') return this.cmdWhile(args)
    if (name === 'proc') return this.cmdProc(args)
    if (name === 'return') {
      const v = args.length ? this.substWord(args[0]) : ''
      throw { __return: v }
    }
    if (name === 'exit') return ''
    if (name === 'incr') return this.cmdIncr(args)
    if (name === 'append') return this.cmdAppend(args)
    if (name === 'open') return this.cmdOpen(args)
    if (name === 'close') return ''
    if (name === 'gets') return this.cmdGets(args)
    if (name === 'file') return this.cmdFile(args)
    if (name === 'info') return this.cmdInfo(args)
    if (name === 'string') return this.cmdString(args)
    if (name === 'oo::class') return this.cmdOoClass(args)
    if (this.procs[name]) return this.callProc(name, args.map((a) => this.substWord(a)))
    if (this.classes[name] && args[0] === 'new') {
      return this.cmdNew(name, args.slice(1).map((a) => this.substWord(a)))
    }

    throw new Error(`找不到命令：${name}`)
  }

  private substWord(word: string): string {
    // Brace literal — no substitution
    if (word.startsWith('{') && word.endsWith('}')) {
      return word.slice(1, -1)
    }
    // Quoted or bare — substitute $ and []
    let s = word
    if (s.startsWith('"') && s.endsWith('"')) {
      s = s.slice(1, -1)
    }
    return this.substitute(s)
  }

  private substitute(s: string): string {
    let out = ''
    for (let i = 0; i < s.length; i++) {
      const ch = s[i]
      if (ch === '\\' && i + 1 < s.length) {
        const n = s[i + 1]
        if (n === 'n') {
          out += '\n'
          i++
          continue
        }
        if (n === 't') {
          out += '\t'
          i++
          continue
        }
        out += n
        i++
        continue
      }
      if (ch === '[') {
        const end = findMatching(s, i, '[', ']')
        const inner = s.slice(i + 1, end)
        out += this.evalCommand(inner.trim())
        i = end
        continue
      }
      if (ch === '$') {
        if (s[i + 1] === '{') {
          const end = s.indexOf('}', i + 2)
          const name = s.slice(i + 2, end)
          out += this.vars[name] ?? ''
          i = end
          continue
        }
        let j = i + 1
        while (j < s.length && /[A-Za-z0-9_]/.test(s[j])) j++
        const name = s.slice(i + 1, j)
        out += this.vars[name] ?? ''
        i = j - 1
        continue
      }
      out += ch
    }
    return out
  }

  private cmdPuts(args: string[]): string {
    let nonewline = false
    let words = args
    if (words[0] === '-nonewline') {
      nonewline = true
      words = words.slice(1)
    }
    // channel? skip if looks like channel var from open
    if (words.length >= 2 && (words[0].startsWith('$') || this.files[this.substWord(words[0])] !== undefined || words[0].startsWith('file'))) {
      const chan = this.substWord(words[0])
      const text = this.substWord(words[1] ?? '')
      this.files[chan] = (this.files[chan] ?? '') + text + (nonewline ? '' : '\n')
      return ''
    }
    const text = words.map((w) => this.substWord(w)).join(' ')
    if (nonewline) {
      if (this.output.length === 0) this.output.push('')
      this.output[this.output.length - 1] += text
    } else {
      this.output.push(text)
    }
    return ''
  }

  private cmdSet(args: string[]): string {
    if (args.length === 1) {
      const name = stripVarName(args[0])
      if (!(name in this.vars)) throw new Error(`变量还不存在：${name}`)
      return this.vars[name]
    }
    const name = stripVarName(args[0])
    const value = this.substWord(args[1])
    this.vars[name] = value
    return value
  }

  private cmdExpr(args: string[]): string {
    const raw = args.map((a) => this.substWord(a)).join(' ')
    const expr = raw.replace(/\{([^{}]*)\}/g, '$1')
    // safe-ish arithmetic / comparisons
    const js = expr
      .replace(/\beq\b/g, '===')
      .replace(/\bne\b/g, '!==')
      .replace(/\btrue\b/g, 'true')
      .replace(/\bfalse\b/g, 'false')
      .replace(/&&/g, '&&')
      .replace(/\|\|/g, '||')
    if (!/^[\d\s.+\-*/%<>=!&|()truefals"'A-Za-z_\u4e00-\u9fff]+$/.test(js.replace(/===|!==/g, ''))) {
      // still try if only numbers and ops
      if (!/^[\d\s.+\-*/%()<>=!&|]+$/.test(js)) {
        throw new Error(`还不支持这个算式：${raw}`)
      }
    }
    try {
      // eslint-disable-next-line no-new-func
      const result = Function(`"use strict"; return (${js});`)()
      if (typeof result === 'boolean') return result ? '1' : '0'
      return String(result)
    } catch {
      throw new Error(`算式出错：${raw}`)
    }
  }

  private cmdLindex(args: string[]): string {
    const list = this.substWord(args[0]).trim().split(/\s+/).filter(Boolean)
    const idx = Number(this.substWord(args[1]))
    return list[idx] ?? ''
  }

  private cmdLlength(args: string[]): string {
    const list = this.substWord(args[0]).trim()
    if (!list) return '0'
    return String(list.split(/\s+/).filter(Boolean).length)
  }

  private cmdLappend(args: string[]): string {
    const name = stripVarName(args[0])
    const items = args.slice(1).map((a) => this.substWord(a))
    const cur = this.vars[name] ?? ''
    const next = [cur, ...items].filter((x) => x !== '').join(' ').trim()
    this.vars[name] = next
    return next
  }

  private cmdIf(args: string[]): string {
    // if {cond} {body} [elseif {c} {b}]* [else {b}]
    let i = 0
    while (i < args.length) {
      if (i === 0 || args[i] === 'elseif') {
        if (args[i] === 'elseif') i++
        const condWord = args[i++]
        const bodyWord = args[i++]
        const cond = this.substWord(condWord)
        const truth = this.evalCondition(cond)
        if (truth) {
          return this.execBody(unwrapBraces(bodyWord))
        }
      } else if (args[i] === 'else') {
        i++
        const bodyWord = args[i++]
        return this.execBody(unwrapBraces(bodyWord))
      } else {
        break
      }
    }
    return ''
  }

  private evalCondition(cond: string): boolean {
    const c = cond.trim()
    // Try expr-style
    try {
      const v = this.cmdExpr([`{${c}}`])
      return v !== '0' && v !== '' && v !== 'false'
    } catch {
      return c !== '' && c !== '0'
    }
  }

  private cmdFor(args: string[]): string {
    // for {init} {cond} {step} {body}
    const init = unwrapBraces(args[0])
    const cond = unwrapBraces(args[1])
    const step = unwrapBraces(args[2])
    const body = unwrapBraces(args[3])
    this.execBody(init)
    let last = ''
    while (this.evalCondition(this.substitute(cond))) {
      this.bump()
      try {
        last = this.execBody(body)
      } catch (e) {
        if ((e as { __return?: string }).__return !== undefined) throw e
        throw e
      }
      this.execBody(step)
    }
    return last
  }

  private cmdForeach(args: string[]): string {
    // foreach var list body
    const varName = stripVarName(args[0])
    const list = this.substWord(args[1]).trim().split(/\s+/).filter(Boolean)
    const body = unwrapBraces(args[2])
    let last = ''
    for (const item of list) {
      this.bump()
      this.vars[varName] = item
      last = this.execBody(body)
    }
    return last
  }

  private cmdWhile(args: string[]): string {
    const cond = unwrapBraces(args[0])
    const body = unwrapBraces(args[1])
    let last = ''
    while (this.evalCondition(this.substitute(cond))) {
      this.bump()
      last = this.execBody(body)
    }
    return last
  }

  private cmdProc(args: string[]): string {
    const name = this.substWord(args[0])
    const argList = unwrapBraces(args[1]).trim().split(/\s+/).filter(Boolean)
    const body = unwrapBraces(args[2])
    this.procs[name] = { args: argList, body }
    return ''
  }

  private callProc(name: string, values: string[]): string {
    const def = this.procs[name]
    const saved = { ...this.vars }
    def.args.forEach((a, i) => {
      this.vars[a] = values[i] ?? ''
    })
    try {
      return this.execBody(def.body)
    } catch (e) {
      if (e && typeof e === 'object' && '__return' in e) {
        return String((e as { __return: string }).__return)
      }
      throw e
    } finally {
      this.vars = saved
    }
  }

  private cmdIncr(args: string[]): string {
    const name = stripVarName(args[0])
    const delta = args[1] ? Number(this.substWord(args[1])) : 1
    const next = String(Number(this.vars[name] ?? '0') + delta)
    this.vars[name] = next
    return next
  }

  private cmdAppend(args: string[]): string {
    const name = stripVarName(args[0])
    const bits = args.slice(1).map((a) => this.substWord(a)).join('')
    this.vars[name] = (this.vars[name] ?? '') + bits
    return this.vars[name]
  }

  private cmdOpen(args: string[]): string {
    const path = this.substWord(args[0])
    const mode = args[1] ? this.substWord(args[1]) : 'r'
    const chan = `file${Object.keys(this.files).length + 1}`
    if (mode.includes('w') || mode.includes('a')) {
      if (!mode.includes('a')) this.files[path] = ''
      this.files[chan] = path
      this.vars[`__chan_${chan}`] = path
    } else {
      this.files[chan] = path
      this.vars[`__chan_${chan}`] = path
      this.vars[`__pos_${chan}`] = '0'
    }
    return chan
  }

  private cmdGets(args: string[]): string {
    const chan = this.substWord(args[0])
    const path = this.vars[`__chan_${chan}`] ?? chan
    const content = this.files[path] ?? ''
    const lines = content.split('\n')
    const pos = Number(this.vars[`__pos_${chan}`] ?? '0')
    const line = lines[pos] ?? ''
    this.vars[`__pos_${chan}`] = String(pos + 1)
    if (args[1]) {
      const varName = stripVarName(args[1])
      this.vars[varName] = line
      return line === undefined || pos >= lines.length ? '-1' : String(line.length)
    }
    return line
  }

  private cmdFile(args: string[]): string {
    const sub = this.substWord(args[0])
    if (sub === 'join') {
      return args
        .slice(1)
        .map((a) => this.substWord(a))
        .join('/')
        .replace(/\/+/g, '/')
    }
    if (sub === 'mkdir') {
      return ''
    }
    if (sub === 'dirname') {
      const p = this.substWord(args[1])
      const i = p.lastIndexOf('/')
      return i >= 0 ? p.slice(0, i) : '.'
    }
    if (sub === 'normalize') return this.substWord(args[1])
    return ''
  }

  private cmdInfo(args: string[]): string {
    const sub = this.substWord(args[0])
    if (sub === 'script') return 'browser.tcl'
    return ''
  }

  private cmdString(args: string[]): string {
    const sub = this.substWord(args[0])
    if (sub === 'equal' || sub === 'eq') {
      return this.substWord(args[1]) === this.substWord(args[2]) ? '1' : '0'
    }
    if (sub === 'length') return String(this.substWord(args[1]).length)
    if (sub === 'tolower') return this.substWord(args[1]).toLowerCase()
    if (sub === 'toupper') return this.substWord(args[1]).toUpperCase()
    return ''
  }

  private cmdOoClass(args: string[]): string {
    // oo::class create Name { body }
    if (this.substWord(args[0]) !== 'create') throw new Error('请写 oo::class create 名字 { ... }')
    const className = this.substWord(args[1])
    const body = unwrapBraces(args[2])
    const def: ClassDef = {
      vars: [],
      constructorArgs: [],
      constructorBody: '',
      methods: {},
    }
    const parts = splitCommands(body)
    for (const part of parts) {
      const t = stripComments(part).trim()
      if (!t) continue
      const w = parseWords(t)
      if (w[0] === 'variable') {
        def.vars.push(...w.slice(1).map((x) => stripVarName(x)))
      } else if (w[0] === 'constructor') {
        def.constructorArgs = unwrapBraces(w[1]).trim().split(/\s+/).filter(Boolean)
        def.constructorBody = unwrapBraces(w[2])
      } else if (w[0] === 'method') {
        def.methods[w[1]] = {
          args: unwrapBraces(w[2]).trim().split(/\s+/).filter(Boolean),
          body: unwrapBraces(w[3]),
        }
      }
    }
    this.classes[className] = def
    return className
  }

  private cmdNew(className: string, args: string[]): string {
    const def = this.classes[className]
    this.objCounter += 1
    const handle = `::oo::Obj${this.objCounter}`
    const inst: ObjectInst = { className, vars: {} }
    def.vars.forEach((v) => {
      inst.vars[v] = ''
    })
    this.objects[handle] = inst
    // run constructor with object vars in scope
    const saved = { ...this.vars }
    Object.assign(this.vars, inst.vars)
    def.constructorArgs.forEach((a, i) => {
      this.vars[a] = args[i] ?? ''
    })
    try {
      this.execBody(def.constructorBody)
      // copy back class variables
      for (const v of def.vars) {
        if (v in this.vars) inst.vars[v] = this.vars[v]
      }
    } finally {
      this.vars = saved
    }
    return handle
  }

  private callObjectMethod(objName: string, method: string, args: string[]): string {
    const inst = this.objects[objName]
    if (!inst) throw new Error(`找不到对象：${objName}`)
    const def = this.classes[inst.className]
    const m = def.methods[method]
    if (!m) throw new Error(`${inst.className} 不会做：${method}`)
    const saved = { ...this.vars }
    Object.assign(this.vars, inst.vars)
    m.args.forEach((a, i) => {
      this.vars[a] = args[i] ?? ''
    })
    try {
      const result = this.execBody(m.body)
      for (const v of def.vars) {
        if (v in this.vars) inst.vars[v] = this.vars[v]
      }
      return result
    } catch (e) {
      if (e && typeof e === 'object' && '__return' in e) {
        for (const v of def.vars) {
          if (v in this.vars) inst.vars[v] = this.vars[v]
        }
        return String((e as { __return: string }).__return)
      }
      throw e
    } finally {
      this.vars = saved
    }
  }
}

function stripVarName(w: string): string {
  let s = w
  if (s.startsWith('$')) s = s.slice(1)
  if (s.startsWith('{') && s.endsWith('}')) s = s.slice(1, -1)
  return s
}

function unwrapBraces(w: string): string {
  const t = w.trim()
  if (t.startsWith('{') && t.endsWith('}')) return t.slice(1, -1)
  if (t.startsWith('"') && t.endsWith('"')) return t.slice(1, -1)
  return t
}

function findMatching(s: string, start: number, open: string, close: string): number {
  let depth = 0
  for (let i = start; i < s.length; i++) {
    if (s[i] === open) depth++
    else if (s[i] === close) {
      depth--
      if (depth === 0) return i
    }
  }
  throw new Error(`缺少配对的 ${close}`)
}

function stripComments(cmd: string): string {
  // Remove ;# comments and full-line #
  let out = ''
  let inQuote = false
  let inBrace = 0
  for (let i = 0; i < cmd.length; i++) {
    const ch = cmd[i]
    if (ch === '"' && inBrace === 0) inQuote = !inQuote
    if (!inQuote && ch === '{') inBrace++
    if (!inQuote && ch === '}' && inBrace) inBrace--
    if (!inQuote && inBrace === 0 && ch === '#') {
      if (i === 0 || /\s|;/.test(cmd[i - 1])) break
    }
    out += ch
  }
  return out.replace(/;\s*$/, '')
}

function splitCommands(script: string): string[] {
  const cmds: string[] = []
  let cur = ''
  let inQuote = false
  let brace = 0
  for (let i = 0; i < script.length; i++) {
    const ch = script[i]
    if (ch === '\\' && i + 1 < script.length) {
      cur += ch + script[i + 1]
      i++
      continue
    }
    if (ch === '"' && brace === 0) inQuote = !inQuote
    if (!inQuote && ch === '{') brace++
    if (!inQuote && ch === '}' && brace) brace--
    if (!inQuote && brace === 0 && (ch === '\n' || ch === ';')) {
      if (cur.trim()) cmds.push(cur)
      cur = ''
      continue
    }
    cur += ch
  }
  if (cur.trim()) cmds.push(cur)
  return cmds
}

function parseWords(cmd: string): string[] {
  const words: string[] = []
  let i = 0
  while (i < cmd.length) {
    while (i < cmd.length && /\s/.test(cmd[i])) i++
    if (i >= cmd.length) break
    if (cmd[i] === '{') {
      const end = findMatching(cmd, i, '{', '}')
      words.push(cmd.slice(i, end + 1))
      i = end + 1
      continue
    }
    if (cmd[i] === '"') {
      let j = i + 1
      let out = '"'
      while (j < cmd.length) {
        if (cmd[j] === '\\' && j + 1 < cmd.length) {
          out += cmd[j] + cmd[j + 1]
          j += 2
          continue
        }
        if (cmd[j] === '"') {
          out += '"'
          j++
          break
        }
        out += cmd[j]
        j++
      }
      words.push(out)
      i = j
      continue
    }
    let j = i
    while (j < cmd.length && !/\s/.test(cmd[j])) {
      if (cmd[j] === '[') {
        const end = findMatching(cmd, j, '[', ']')
        j = end + 1
        continue
      }
      j++
    }
    words.push(cmd.slice(i, j))
    i = j
  }
  return words
}

export function runTcl(script: string): RunResult {
  try {
    const interp = new TclInterp()
    interp.run(script)
    return {
      ok: true,
      output: interp.output.join('\n'),
      mode: 'browser',
    }
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    return {
      ok: false,
      output: '',
      error: msg,
      mode: 'browser',
    }
  }
}
