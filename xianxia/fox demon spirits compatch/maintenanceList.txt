# XIANXIA MOD — CORRECTED CODEX CHANGELOG

## CURRENT STATE (TRUTH, NOT CLAIMS)

### Systems that EXIST but are NOT COMPLETE

* Jianghu Grand Gathering → currently a decision + event chain (NOT a real activity)
* Dao Exchange → same issue (decision wrapper, not activity system)
* Jianghu leaderboard → based on win counters, NOT actual prowess
* Sect succession/conflict → exists but too weak in gameplay impact
* Spirit vein / sacred mountain → implemented but shallow economy impact
* Initialization → partially correct but relies on maintenance loops to fix gaps
* Fox spirits → fully integrated in runtime, but architecture still messy (core + compatch overlap)

### Systems that are STABLE (keep and expand)

* Magic treasure crafting backend
* Artifact pool and scaling system
* Modifier library (sect, alchemy, jianghu, etc.)
* Disciple / path recruitment framework
* Core AI cultivation loop (but needs optimization, not replacement)

---

# CORE DESIGN RULES (MANDATORY)

1. STOP building systems as:
   decision → event → reward

2. START building systems as:

   * activities
   * interactions
   * persistent world states

3. Runtime > documentation

   * If code and changelog conflict → CODE is correct

4. No duplicate systems across:

   * core mod
   * fox compatch

---

# MAJOR FIXES (IN ORDER)

---

## 1. REBUILD JIANGHU GRAND GATHERING (CRITICAL)

### Problem

* Currently:

  * decision
  * triggers events (1870–1872)
  * gives random rewards/stress
* No real gathering of characters

### Required Fix

Convert into FULL ACTIVITY system:

CREATE:

```
common/activities/jianghu_grand_gathering_activity.txt
```

Must include:

* activity type
* invited participants (cultivators, sect members, rivals)
* phases:

  * arrival
  * sparring / duels
  * exchanges
  * climax event
* outcomes tied to:

  * prowess
  * traits
  * sect affiliation

REMOVE:

* reliance on event-only chain as primary system

KEEP:

* event chain only as flavor inside activity

---

## 2. REBUILD DAO EXCHANGE AS ACTIVITY

### Problem

* Currently identical flaw as gathering
* Uses feast logic + event wrapper

### Required Fix

* Create dedicated Dao Exchange activity
* Focus on:

  * learning
  * philosophy alignment
  * sect influence
  * relationship shifts

---

## 3. FIX JIANGHU LEADERBOARD

### Problem

* Uses:

  * `jianghu_tourney_wins_total`
* NOT actual strength

### Required Fix

SPLIT INTO TWO SYSTEMS:

### A. Strength Ranking (NEW)

* Based on:

  * prowess (primary)
  * cultivation traits (secondary weight)

### B. Fame Ranking (KEEP)

* Based on:

  * tournaments
  * gatherings
  * achievements

UPDATE:

```
xianxia_world.1890
```

REMOVE:

* win-only ranking as "strongest"

---

## 4. CLEAN INITIALIZATION SYSTEM

### Problem

* Initialization uses:

  * `every_ruler`
* Then patched by maintenance loops

### Required Fix

* Proper startup pass:

  * assign cultivation
  * assign sect roles
  * assign fox states

REDUCE:

* reliance on monthly/yearly fixes

---

## 5. REDUCE PULSE OVERUSE (PERFORMANCE + STABILITY)

### Problem

Too many:

* `every_living_character` loops
* monthly heavy passes

### Required Fix

MOVE LOGIC TO:

* on_game_start
* on_character_death
* on_title_change
* on_activity_complete

KEEP monthly ONLY for:

* dynamic systems (e.g. rankings)

---

## 6. SPIRIT VEIN / SACRED MOUNTAIN REWORK

### Current State

* Modifiers exist
* Effects are generic

### Required Fix

MAKE THEM FEEL LIKE:

* cultivation economy (spirit stones)

### Add:

* clear gold identity = spirit stones
* winner/loser system:

  * winner gains stacking income
  * loser gets reduced income

### Improve:

* capital impact
* sect territorial identity

---

## 7. SECT SUCCESSION CRISIS (MAKE IT REAL)

### Current State

* Modifiers exist
* Impact too weak

### Required Fix

CRISIS SHOULD:

* heavily reduce opinion
* increase faction pressure
* risk rebellion
* disrupt capital economy

ADD:

* stronger negative modifiers
* chain escalation events

---

## 8. FOX SPIRITS — CORE SYSTEM CONSOLIDATION

### Decision: FOX IS CORE

### Required Fix

REMOVE split logic between:

* main mod
* compatch

### Core mod must contain:

* awakening
* possession
* lineage inheritance
* AI behavior
* social reaction system

### Compatch should ONLY contain:

* compatibility tweaks
* optional flavor
* visual/asset support

### Additional Improvements

* strengthen:

  * possession gameplay
  * social consequences
  * sect reactions
* ensure:

  * fox systems integrate with:

    * sects
    * rankings
    * activities

---

## 9. DECISION SYSTEM CLEANUP

### Problem

Too many shallow decisions

### Required Fix

For EACH decision:

* classify:

  * keep simple
  * expand chain
  * convert to interaction
  * convert to activity

DO NOT:

* leave systems as one-click reward generators

---

## 10. MAGIC TREASURE SYSTEM (EXPAND, DON'T REBUILD)

### Status

* One of the strongest systems

### Keep:

* crafting effect system
* artifact pool
* tier scaling

### Improve:

* acquisition sources
* world integration
* rivalries over artifacts

---

## 11. DOCUMENTATION + STRUCTURE FIX

### Problem

* changelog contains:

  * duplicate sections
  * false “completed” systems
  * mirror confusion

### Required Fix

* Runtime is source of truth
* Update mirrors AFTER runtime fixes
* Remove misleading completion notes

---

# FINAL PRIORITY ORDER

1. Grand Gathering → real activity
2. Dao Exchange → real activity
3. Leaderboard split (prowess vs fame)
4. Initialization cleanup
5. Reduce pulse overuse
6. Spirit vein economy pass
7. Sect crisis strengthening
8. Fox system consolidation
9. Decision system cleanup
10. Documentation correction

---

# DESIGN TARGET

The mod should feel like:

* a living cultivation world
* not a menu of decisions

If a system does not:

* involve other characters
* create persistent state
* affect the world

→ it is not finished
