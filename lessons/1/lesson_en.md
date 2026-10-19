# Week 1 — The Computer Can Talk: `puts` and Script Files

> Part of the [10-week Tcl learning plan](../../PLAN.md).  
> Goal this week: make the computer print text for you, and understand what a `.tcl` file is.

---

## Learning goals

By the end of this week, you should be able to:

1. Open a terminal and start Tcl with `tclsh`.
2. Use `puts` to print one or more lines of text to the screen.
3. Create a `.tcl` script file, save Tcl commands inside it, and run the file with `tclsh`.
4. Write `#` comments that explain what each important line is doing.
5. Finish a self-introduction card script on your own (based on `10_self_intro_card.tcl`).

When you can do all five without copying every character from this page, Week 1 is done.

---

## Big idea (in everyday words)

A computer is like a helpful robot. It does **exactly** what you write — no more, no less. If you ask it to print three lines, it prints three lines. If you forget a quote mark, it may stop and show an error instead of guessing what you meant.

| Tcl idea | Everyday metaphor | What you will do with it this week |
|----------|-------------------|------------------------------------|
| Script `.tcl` | A **to-do list** for the robot | Save commands in a file and reuse them |
| `puts` | “Please **say this out loud** (print it)” | Make the screen show your words |
| `#` comment | A sticky note for humans; the robot **ignores** it | Leave reminders for yourself |
| `tclsh my.tcl` | “Robot, please **follow this list**” | Run a whole file in one command |

### The 3-Step Tcl Mental Model (Core Concept)

No matter how large your script becomes, the Tcl interpreter evaluates every line following a strict three-step cycle:

```text
Step 1: Argument Grouping
   Split words by whitespace; group tokens using quotes "" or curly braces {}.
      ↓
Step 2: Value Substitution
   If arguments are enclosed in double quotes, evaluate $variables, [commands], and \escapes.
      ↓
Step 3: Command Invocation
   Look up the first word in the command table (e.g. puts) and pass the substituted arguments.
```

You do **not** need variables, loops, lists, or Calibre yet. This week is only about speaking: print text, understand grouping, save a script, and add comments.

---

## What you need before you start

### Tools

1. A terminal (command line) on your computer.
2. Tcl installed so the program `tclsh` can be found.
3. A text editor to create `.tcl` files (any plain-text editor is fine: VS Code / Cursor, nano, Notepad++, etc.).

### Check that Tcl works

In the terminal, type:

```bash
tclsh
```

If Tcl is installed, you usually see a prompt such as `%` (the exact look can differ). That means you are **inside** the Tcl shell and can type Tcl commands.

Inside `tclsh`, type this line and press Enter:

```tcl
puts "Hello, I am learning Tcl!"
```

You should see:

```text
Hello, I am learning Tcl!
```

Then leave the Tcl shell:

```tcl
exit
```

You are back in the normal terminal.

### Run a script file in one shot

You do not have to stay inside `tclsh`. From the project root folder (`tcl-language`), you can run:

```bash
tclsh lessons/1/01_hello.tcl
```

That means: “Start Tcl, read every line in this file from top to bottom, then finish.”

If you already moved into the lesson folder:

```bash
cd lessons/1
tclsh 01_hello.tcl
```

Both ways are correct. Pick one habit and stick with it while you practice.

---

## Concept 1 — `puts` means “print this”

`puts` is short for **put string**: put a piece of text onto the screen (and usually move to the next line afterward).

### The shape of a `puts` command

```tcl
puts "Hello"
```

Broken into parts:

| Part | Example | Meaning |
|------|---------|---------|
| Command name | `puts` | The action: print |
| Space | (one space) | Separates the command from its argument |
| Argument (the text) | `"Hello"` | What to print |

### Rules to remember this week

1. Write `puts`, then a space, then the text you want.
2. If the text has spaces, wrap it in **double quotes** `"..."`.
3. Each normal `puts` prints **one line**, then moves the cursor to the next line.
4. Spelling matters: `Puts`, `PUTS`, or `put` are not the same as `puts` in Tcl.

### Expected output vs what you typed

If you run:

```tcl
puts "Hello, I am learning Tcl!"
puts "My name is Amy."
puts "I like the color blue."
```

the screen should show exactly three lines:

```text
Hello, I am learning Tcl!
My name is Amy.
I like the color blue.
```

Notice: the word `puts` and the quote marks do **not** appear in the output. Only the text inside the quotes is printed.

### Practice without a file first

1. Start `tclsh`.
2. Type one `puts` line; press Enter; check the output.
3. Type a second `puts` line; check again.
4. Type `exit` when finished.

When that feels comfortable, move to Concept 2 and save the same ideas in a file.

---

## Concept 2 — A `.tcl` file is a script (full walkthrough)

Typing inside `tclsh` is good for tiny experiments. Real practice means saving a **script**: a plain text file whose name ends with `.tcl`, filled with Tcl commands.

### Why scripts matter

| Interactive `tclsh` | Script file `.tcl` |
|---------------------|--------------------|
| You type one line at a time | You write many lines once |
| Easy to forget what you typed | You can open the file tomorrow and still see everything |
| Great for a 10-second test | Great for homework, projects, and Calibre later |

### Step-by-step: create and run your first full script

Follow these steps carefully the first time. After that, you can go faster.

#### Step 1 — Choose a folder

Work from the project root, or from `lessons/1`. Example (project root):

```bash
cd /path/to/tcl-language
```

(Use your real path. On this machine the project is often `/home/yongfu/proj/tcl-language`.)

#### Step 2 — Create a new file

Create a new plain-text file named `my_first.tcl`.  
You may put it in `lessons/1/` next to the other examples, or in a practice folder you choose. What matters is that you know the path when you run `tclsh`.

#### Step 3 — Type a complete first script

Open `my_first.tcl` and enter the following **full** script (not a short stub). Every line has a job:

```tcl
# my_first.tcl
# Week 1 — my first complete Tcl script
# Run from project root:
#   tclsh lessons/1/my_first.tcl
# Or, if this file is in the current folder:
#   tclsh my_first.tcl

# ----- header: who wrote this and why -----
puts "================================"
puts "   My First Tcl Script"
puts "================================"

# ----- body: facts about me (change these words!) -----
puts "Hello, I am learning Tcl!"
puts "My name is Amy."
puts "I am 10 years old."
puts "My favorite color is blue."
puts "Today I learned puts and .tcl files."

# ----- footer: end of the card -----
puts "================================"
puts "Script finished. Great job!"
```

What each part is doing:

1. **Top comments** — tell humans the file name, the week, and how to run it. Tcl ignores these lines.
2. **Header `puts` lines** — print a clear title banner so output is easy to read.
3. **Body `puts` lines** — the real content (your facts). Change the name, age, and color to your own.
4. **Footer `puts` lines** — mark the end so you know the script ran all the way through.

#### Step 4 — Save the file

Save as plain text with the `.tcl` extension. Do not save as a Word document or rich text.

#### Step 5 — Run it

From the folder that makes the path correct:

```bash
tclsh my_first.tcl
```

or, if the file lives under `lessons/1` and you are at the project root:

```bash
tclsh lessons/1/my_first.tcl
```

#### Step 6 — Read the output and compare

You should see a banner, several fact lines, and a closing banner. If something is missing, open the file again and check:

- Did every `puts` line have matching quotes?
- Did you save the file before running?
- Are you running the same file you edited (correct path)?

#### Step 7 — Edit and run again

Change one line (for example, the favorite color), save, and run `tclsh` again. Seeing the new output is proof that **you** control the script.

### How Tcl reads a script

Tcl reads the file **from the first line to the last line**:

1. If the line is empty → skip (nothing to do).
2. If the line starts with `#` (or the rest of the line after `#` is a comment) → ignore that comment text.
3. If the line is a command such as `puts "..."` → run it.
4. Then go to the next line, until the file ends.

There is no “start button” inside the file. The start button is the shell command `tclsh yourfile.tcl`.

---

## Concept 3 — `#` comments are notes for you

Anything after `#` on a line is a **comment**. Tcl does not print it and does not treat it as a command.

### Whole-line comments

```tcl
# This entire line is only for me to read
puts "The computer still prints this"
```

### End-of-line comments

You can also put a short note after a command. In Tcl, a semicolon `;` can separate commands on one line; a common style is:

```tcl
puts "The computer still prints this"   ;# this note explains the puts line
```

For Week 1, whole-line comments above each section are enough.

### What makes a good comment

Good comments answer: *What is this part doing, and why is it here?*

| Better comment | Weaker comment | Why |
|----------------|----------------|-----|
| `# Print my favorite color` | `# puts` | Explains purpose, not only the command name |
| `# Title banner for the intro card` | `# line 1` | Describes the role of the block |
| `# Change this line to your real name` | `# text` | Tells the next editor what to do |

### Comments that do not run code

If you put `#` at the beginning of a `puts` line, that `puts` will **not** run:

```tcl
# puts "This will NOT appear on the screen"
puts "This WILL appear on the screen"
```

That is useful when you want to temporarily turn off a line without deleting it.

---

## Concept 4 — Quotes, spaces, and special characters (Week 1 detail)

### Double quotes `"..."`

Use double quotes for almost all text this week:

```tcl
puts "Hello world"
puts "Name: Amy"
```

Quotes tell Tcl: “this whole piece is one argument,” even when it contains spaces.

### Single word without quotes

This can work for one word with no spaces:

```tcl
puts Hello
```

It prints `Hello`. As a beginner habit, still prefer quotes: `puts "Hello"`.

### Why matching quotes matter

Each opening `"` needs a closing `"`.

| Typed | Problem |
|-------|---------|
| `puts "Hello` | Missing closing quote → error |
| `puts Hello"` | Stray quote → error |
| `puts "She said "hi""` | Inner quotes confuse Tcl (advanced topic; avoid for now) |

For Week 1, keep strings simple: one pair of quotes around the whole message.

### Square brackets `[...]` are special in Tcl

In Tcl, `[something]` means “run `something` as a command and use its result.” So this is dangerous if you only wanted to print boxes:

```tcl
puts "[ ] not ready"   ;# Tcl tries to run a command named space — not what we want
```

To print square brackets literally in Week 1, use curly braces (braces turn off that substitution):

```tcl
puts {[ ] not ready}
```

See `12_run_checklist.tcl` for a full working example.

### Curly braces `{...}` — only what you need this week

You do **not** need to master braces yet. You only need them if you must print characters that Tcl would otherwise treat specially (like `[` and `]`). Week 2 and later will explain braces together with variables.

---

## Daily practice (≈30–45 minutes each day)

Work in order. Each day builds on the day before.

| Day | Goal | What to do in detail | Suggested file |
|-----|------|----------------------|----------------|
| Day 1 | Prove Tcl runs | Start `tclsh`, print `Hello, I am learning Tcl!`, then run `01_hello.tcl` | `01_hello.tcl` |
| Day 2 | Talk about yourself | Print your name, age, and favorite color on separate lines; edit the sample to your facts | `02_about_me.tcl` |
| Day 3 | Longer script | Write **five** `puts` lines in one file; run with `tclsh`; confirm all five lines appear | `03_five_lines.tcl` |
| Day 4 | Comments | Add a `#` comment before every important `puts` (or section) explaining its job | `04_with_comments.tcl` |
| Day 5 | Week project | Build or customize a self-introduction card with a clear border and several facts | `10_self_intro_card.tcl` |

Extra practice days (if you finish early): run `05` through `09`, then the bonus files `11` and `12`.

### Week checklist

- [ ] I can open a terminal and run `tclsh`.
- [ ] I can use `puts` to print text I chose.
- [ ] I can create a `.tcl` file, save it, and run it with `tclsh`.
- [ ] I can add useful `#` comments that explain sections of my script.
- [ ] I finished my own self-introduction card (not only the sample name “Amy”).

---

## Common mistakes (and fixes)

| What you see / do | What it usually means | Fix |
|-------------------|----------------------|-----|
| `command not found: tclsh` | Tcl is not installed, or the terminal cannot find it | Ask an adult to install Tcl; close and reopen the terminal; retry `tclsh` |
| `extra characters after close-quote` | Quotes are missing, extra, or mismatched | Count `"` marks; keep one matching pair around each string |
| `invalid command name "..."` | Typo in the command word, or a broken line | Check that the command is exactly `puts` |
| Nothing seems to happen | You are inside `tclsh` but have not typed a command yet | Type a `puts "..."` line, or run a `.tcl` file from the terminal |
| Chinese / special characters look wrong | Terminal encoding is not UTF-8 | Switch the terminal to UTF-8; or practice with plain English first |
| Script seems “old” / changes missing | You edited one path but ran another, or forgot to save | Save the file; confirm the path passed to `tclsh` |
| `[ ]` disappears or causes an error in `puts` | Tcl treats `[...]` as “run a command” | Print with braces: `puts {[ ] item}` (see `12_run_checklist.tcl`) |

---

## Example scripts in this folder (full list)

Easiest way (from the project root, using the Makefile):

```bash
make help          # show all make targets
make week1-01      # run one example (01..12)
make week1         # run all Week 1 examples in order
make run WEEK=1 EX=10
```

Or call `tclsh` yourself:

```bash
tclsh lessons/1/01_hello.tcl
tclsh lessons/1/02_about_me.tcl
tclsh lessons/1/03_five_lines.tcl
tclsh lessons/1/04_with_comments.tcl
tclsh lessons/1/05_blank_lines.tcl
tclsh lessons/1/06_ascii_art.tcl
tclsh lessons/1/07_shopping_list.tcl
tclsh lessons/1/08_story_three_lines.tcl
tclsh lessons/1/09_menu_card.tcl
tclsh lessons/1/10_self_intro_card.tcl
tclsh lessons/1/11_puts_without_newline.tcl
tclsh lessons/1/12_run_checklist.tcl
```

| # | File | What you practice | What success looks like |
|---|------|-------------------|-------------------------|
| 01 | `01_hello.tcl` | First `puts` | One hello line prints |
| 02 | `02_about_me.tcl` | Several lines about a person | Three fact lines print |
| 03 | `03_five_lines.tcl` | A longer top-to-bottom script | All five lines appear in order |
| 04 | `04_with_comments.tcl` | `#` comments | Output still correct; comments explain the file |
| 05 | `05_blank_lines.tcl` | Blank lines for readability | Sections are easy to read in the file and output |
| 06 | `06_ascii_art.tcl` | Pictures made of characters | A small cat (or shape) appears |
| 07 | `07_shopping_list.tcl` | Numbered list layout | Title, items, and footer all print |
| 08 | `08_story_three_lines.tcl` | Short story structure | Beginning, middle, end |
| 09 | `09_menu_card.tcl` | Box-style layout with `+` and `\|` | A readable menu card |
| 10 | `10_self_intro_card.tcl` | **Week project** | A full intro card you can personalize |
| 11 | `11_puts_without_newline.tcl` | `puts -nonewline` (bonus) | `Loading...` appears on one line |
| 12 | `12_run_checklist.tcl` | Checklist + literal `[ ]` | Boxes print correctly with braces |

Open each file, read the comments at the top, run it, then change at least one string and run it again.

---

## Challenge (optional, full requirements)

Customize `10_self_intro_card.tcl` (or your own copy) so the printed card includes **all** of the following:

1. Your real name  
2. Your school or city  
3. Your age (or grade)  
4. Your favorite color or hobby  
5. One thing you want to learn in Tcl  
6. A top and bottom border made of `=` or `*` characters  
7. At least three `#` comments that explain the header, body, and footer  

Do **not** use variables yet unless you already started Week 2. Plain `puts` lines are the Week 1 solution.

---

## Looking ahead

**Week 2** introduces **variables**: labeled boxes that store values.

- `set name "Amy"` puts text into a box labeled `name`.
- `$name` opens that box and uses the value inside.
- `expr` will help with simple math (for example, age + 1).

This week you only print **fixed** text that you typed into the file. Next week the same script can print different values by changing what is stored in the boxes.

---

## Parent / teacher note

- Calibre / `calibredrv` is **not** required this week. Plain `tclsh` is enough.
- Success looks like: the learner can create or edit a `.tcl` file, save it, run it with `tclsh`, read the output, and explain at least one comment in their own words.
- If they get stuck: run examples `01` → `10` in order; then duplicate `10_self_intro_card.tcl` and change every personal fact.
- Avoid doing the typing for them after Day 2. The skill is “edit → save → run → read output,” not memorizing the sample name Amy.
