# Week 15 — Toys That Do Things: Classes, Objects, Methods (TclOO)

> Part of the [Tcl-first plan](../../PLAN.md) (**M20** weeks 11–20).  
> Goal this week: use TclOO (`oo::class`) to build **molds → toys → actions**.

---

## Learning goals

By the end of this week, you should be able to:

1. Explain in your own words: **class** (mold), **object** (real toy), **method** (action).
2. Write `oo::class create Pet { ... }` with `variable`, `constructor`, and `method`.
3. Create objects with `[Pet new "Mimi" "cat"]` and call `$obj introduce`.
4. Add a new method (for example `rename {newName}`) and change object state.
5. Create a second class (`Robot`) with multiple methods.
6. Finish a **pet shop** script: 1 class, 2+ objects, 3+ methods.

Tcl 8.6+ includes TclOO — use plain `tclsh`, no extra install.

---

## Big idea (in everyday words)

| OOP / TclOO | Everyday metaphor | Tcl shape |
|-------------|-------------------|-----------|
| Class | Toy **mold** | `oo::class create Pet { ... }` |
| Object | Real toy from the mold | `set cat [Pet new "Mimi" "cat"]` |
| `variable name` | Name tag on each toy | Inside class body |
| `constructor` | What happens when toy is made | `constructor {n k} { set name $n }` |
| `method speak` | Trick the toy can do | `method speak {} { ... }` |
| `$cat speak` | "Do your trick!" | Object command + method name |

**From Week 5:** A `proc` is a helper without an owner. A **method** belongs to an **object**.

**Bridge to Calibre (Week 21):** You will not write `oo::class create layout`, but:

```tcl
set L [layout create]   ;# like Pet new
$L create cell TOP       ;# like $cat speak
```

---

## What you need before you start

### Prerequisites

- Weeks 1–5: variables, lists, `if`, loops, `proc`, files.

### Environment

```bash
make check
```

Tcl 8.6 includes TclOO automatically.

---

## Concept 1 — Class, object, method (Day 1–2)

### Full Pet example (from PLAN)

```tcl
oo::class create Pet {
    variable name kind

    constructor {n k} {
        set name $n
        set kind $k
    }

    method introduce {} {
        puts "I am $name, a $kind."
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
$a introduce
$a speak
```

### Anatomy table

| Piece | Role |
|-------|------|
| `oo::class create Pet` | Define class named Pet |
| `variable name kind` | Instance variables (each object has its own) |
| `constructor {n k}` | Runs when `Pet new ...` is called |
| `method introduce {}` | Action with no extra args |
| `[Pet new "Mimi" "cat"]` | Create object |
| `$a introduce` | Call method on object `$a` |

### Two objects, one class

```tcl
set a [Pet new "Mimi" "cat"]
set b [Pet new "Buddy" "dog"]
```

Same mold (`Pet`), different toys (`$a` and `$b`). See `02_pet_two_objects.tcl`.

---

## Concept 2 — Methods can change state (Day 3)

```tcl
method rename {newName} {
    set name $newName
    puts "(Name changed to $name)"
}
```

Call: `$cat rename "Snowball"` then `$cat introduce`.

The object's **variable** `name` updates; next method call sees the new value.

---

## Concept 3 — Robot class (Day 4)

```tcl
oo::class create Robot {
    variable name steps

    constructor {n} {
        set name $n
        set steps 0
    }

    method move {count} {
        set steps [expr {$steps + $count}]
        puts "$name moved $count step(s). Total: $steps"
    }
}
```

Methods can take arguments: `move {count}` → `$bot move 3`.

See `04_robot_basic.tcl` and `05_robot_move.tcl`.

---

## Concept 4 — Pet shop project (Day 5)

`10_pet_shop.tcl` includes:

- Class `Pet` with `name`, `kind`, `age`
- Methods: `introduce`, `speak`, `birthday`
- Three objects: `$p1`, `$p2`, `$p3`

Optional: copy to `examples/my_oop_pets.tcl` and customize.

---

## Concept 5 — Bonus patterns

### foreach over objects

```tcl
set shop [list $a $b $c]
foreach p $shop {
    $p speak
}
```

See `09_foreach_objects.tcl`.

### Subclass (optional)

```tcl
oo::class create Cat {
    superclass Pet
    method speak {} { puts "$name: meow!" }
}
```

See `11_cat_superclass.tcl` — a specialized mold.

---

## Daily practice

| Day | Goal | Files |
|-----|------|-------|
| Day 1 | Draw mold vs toys vs methods | Paper + read `06_class_and_object_words.tcl` |
| Day 2 | Run Pet example | `01_pet_basic.tcl`, `02_pet_two_objects.tcl` |
| Day 3 | Add `rename` | `03_pet_rename.tcl` |
| Day 4 | Robot class | `04_robot_basic.tcl`, `05_robot_move.tcl` |
| Day 5 | **Pet shop** | `10_pet_shop.tcl` |

Bonus: `07`–`09`, `11`, `12`.

### Week checklist

- [ ] I can explain class / object / method.
- [ ] I can write `oo::class create` with constructor and methods.
- [ ] I can create objects with `ClassName new`.
- [ ] I can call `$obj methodName`.
- [ ] I added a method to a class.
- [ ] I finished the pet shop project.

---

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `unknown method` | Typo in method name | Match `method speak` and `$obj speak` |
| Wrong name in method | Forgot `variable name` | Declare `variable name` at top of class |
| `invalid command name "Pet"` | Class not defined yet | Put `oo::class create` before `Pet new` |
| `$name` empty in method | Constructor did not set it | Check `constructor` body |
| `Pet new` vs `$a speak` | Confused class vs object | `new` on class; methods on `$object` |
| Subclass `can't read "name"` | Method did not declare `variable name` | Add `variable name` inside each method that uses it |

---

## Example scripts

```bash
make week15-01
make week15
make list WEEK=6
```

| # | File | Practice |
|---|------|----------|
| 01 | `01_pet_basic.tcl` | First Pet class |
| 02 | `02_pet_two_objects.tcl` | Two objects |
| 03 | `03_pet_rename.tcl` | rename method |
| 04 | `04_robot_basic.tcl` | Robot + beep |
| 05 | `05_robot_move.tcl` | move + state |
| 06 | `06_class_and_object_words.tcl` | Vocabulary |
| 07 | `07_constructor_args.tcl` | Multi-arg constructor |
| 08 | `08_method_with_if.tcl` | method + if |
| 09 | `09_foreach_objects.tcl` | foreach objects |
| 10 | `10_pet_shop.tcl` | **Week project** |
| 11 | `11_cat_superclass.tcl` | superclass bonus |
| 12 | `12_run_checklist.tcl` | Checklist |

---

## Challenge

Extend `10_pet_shop.tcl`:

1. Add method `feed {}` that increases energy or age message  
2. Fourth pet object  
3. List all pets in `foreach` and call `speak`  
4. One `#` comment block explaining class vs object  
5. Copy finished version to `examples/my_oop_pets.tcl`  

---

## Looking ahead

**Week 16 — TclOO advanced**, then workshops through Week 20.  
**Week 21 — Calibre:** `set L [layout create]` behaves like making a layout **object**. Same **object.method** pattern.

Parents run `./scripts/setup_calibredrv.sh`; you write scripts and read results.

---

## Parent / teacher note

- OOP vocabulary can stay informal (mold / toy / trick) until it clicks.
- Each example file redefines classes — that is OK for learning; one file = one complete story.
- Success: child runs `make week15-10` and explains which part is the mold and which are the toys.
