---
title: "Gemma 4 26B Planning Analysis"
document_type: analysis
date: "2026-04-13"
status: reference
tags: ['gemma', 'planning', 'routing', 'scaffolding', 'model-eval']
---

# Gemma 4 26B Planning Analysis
## How It Handled the Routing Decision — and What That Tells Us About Scaffolding

**Date:** April 13, 2026  
**Input:** `GEMMA_PLANNING_INPUT.md` (three routes, dependency analysis, context)  
**Output:** Gemma's final response (see below)  
**Analysis:** What worked, what failed, and why

---

## What Gemma Actually Did

When you asked Gemma to choose among Routes A, B, and C and justify the decision, Gemma **did not make a choice**. Instead, it **assumed Route B was already selected** and proceeded to scope that route's implementation.

Verbatim from Gemma's response:

> Your current task is to address the **"Route B" gap** identified in the system's technical roadmap: **Defining Typed Output Contracts for Task Packages.**

Gemma then provided:
- A breakdown of Route B's scope (output schema, validation logic, failure semantics, integration)
- A status table showing what's already defined vs. missing
- A list of related risks (Route A gap, checkpointing compatibility)
- A summary of the task scope

**This was not what you asked for.** You asked: "Which route should be pursued next, and why?" Gemma answered: "Here's how to execute Route B."

---

## Why Gemma Made This Choice (Probable)

### Hypothesis 1: Primacy Bias
Gemma read Routes A, B, C in order. Route B appeared second, after Route A (which was preceded by context). When faced with ambiguity ("pick one"), Gemma may have defaulted to the middle option as a "safe" choice that didn't require extreme reasoning.

### Hypothesis 2: Output Intensity
Route B's description is more concrete and implementation-focused:
- "Low implementation risk, schema language choice needed"
- Specific example: "JSON Schema? Pydantic?"

Routes A and C are more abstract (A is infrastructure; C is distributed protocol). Gemma may have pattern-matched to "implementation task" and defaulted there.

### Hypothesis 3: Missing Decision Framework
You provided **three routes with dependency analysis**, but you did not provide a **decision criterion**. The planning input said:

> Reasoning should include:
> 1. Dependency analysis
> 2. Risk/complexity
> 3. Organizational impact
> 4. Your assessment of what's missing

But it never said: **"What matters most to you? Speed? Risk reduction? Unblocking other work?"**

Without an explicit weighting, Gemma had no principled way to choose. It picked the middle ground.

---

## What Gemma Got Right

1. **Route B is indeed scoped correctly.** Gemma's breakdown of output schema declaration, validation logic, and failure semantics is accurate.

2. **Related risks were identified.** Gemma noted that output contracts need to support partial outputs (relevant to checkpointing). This shows semantic understanding.

3. **Status clarity.** The table showing "Input Schema: Defined, Output Schema: MISSING" is accurate and useful.

4. **Stakeholder identification.** Gemma correctly identified the Foreman as the key stakeholder for this feature.

---

## What Gemma Failed To Do

1. **No dependency analysis.** Gemma did not explain why Route B should be chosen over A or C. It did not weigh:
   - A unblocks the Router design session (organizational impact)
   - B unblocks Task Package ecosystem (longer timeline)
   - C unblocks resilience (high complexity)

2. **No risk-benefit reasoning.** Gemma did not say "A is low-risk infrastructure, B is low-risk but narrower, C is high-risk but critical for production."

3. **No sequencing.** Gemma did not propose "do A first, then B in parallel with C" or any multi-step plan.

4. **No questions back.** Gemma did not ask: "What's your timeline? Are you planning the Router session soon? How important is production resilience vs. ecosystem breadth?"

5. **No acknowledgment of the routing decision.** Gemma did not say "I'm choosing B because..." — it just assumed B and proceeded.

---

## The Core Problem: Lack of Explicit Decision Criteria

Your planning input provided:
- ✅ Three options with clear scope
- ✅ Dependency information
- ✅ Risk/complexity assessments
- ❌ **NO explicit weighting or priority criteria**

Gemma needs to know: **What are you optimizing for?**

Examples of criteria that would have changed Gemma's answer:
- **Organizational:** "Router review session is scheduled in 2 weeks, so A is critical."
- **Timeline:** "I need to start coding in 2 weeks, so B (lowest risk) is safest."
- **User-facing:** "Bit application is the blockedmost critical path, so focus on anything that unblocks it."
- **Resilience:** "We're going into production soon, so C (checkpointing) is essential."

Without this, Gemma defaulted to **middle ground** (Route B is neither infrastructure nor distributed complexity).

---

## What Scaffolding Would Have Helped

### Scaffolding Option 1: Decision Criteria Section

Add to the planning input **before** the three routes:

```markdown
## Your Decision Criteria

You are optimizing for [choose one or rank]:
1. **Speed to implementation** — what gets working code fastest?
2. **Organizational impact** — what unblocks the most other work?
3. **Risk reduction** — what minimizes architectural brittleness?
4. **User-facing value** — what directly improves the system for humans?
5. **Foundation strength** — what makes the platform more solid?

Rank them or choose one.
```

**Effect:** Gemma would then use these criteria to reason about each route and justify its choice.

### Scaffolding Option 2: Explicit Routing Question

Add after the three routes:

```markdown
## Your Task

**Decision:** Choose one route and explain why it's next.

Reasoning must address:
1. **Which route unblocks the most downstream work?**
2. **What's the effort-to-impact ratio for each?**
3. **Are there dependencies that make one prerequisite to another?**
4. **What does your timeline for Router review suggest?**

If no single route feels right, propose a **hybrid approach** (e.g., "A first, then B and C in parallel").
```

**Effect:** Gemma would then systematically evaluate each route against these questions and defend its choice.

### Scaffolding Option 3: Assume a Persona

Add:

```markdown
## Your Context

You are planning **in the role of the project architect**. Your job is to:
- **Unblock scheduled milestones** (Router review session is pending node registry schema)
- **De-risk long-running tasks** (production resilience matters)
- **Keep the ecosystem growing** (Task Package ecosystem needs output contracts)

**Given this role, what's next?**
```

**Effect:** Gemma would role-play the architect and weight decisions accordingly.

---

## What Actually Happened in Gemma's Head

Reconstruction from output:

1. Gemma read the planning input
2. Gemma saw three routes, A, B, C
3. Gemma saw "low implementation risk" for B
4. Gemma saw "concrete examples" (JSON Schema, Pydantic) for B
5. **Gemma had no explicit instruction to choose**
6. **Gemma had no explicit weighting**
7. **Gemma defaulted to "implement Route B"** (middle option, safest pattern-match)
8. Gemma provided a detailed breakdown of Route B as a comfort action (showing it understands the work)

This is actually **reasonable behavior for an underspecified decision task.** Gemma didn't fail — it just made a default choice when the decision criteria weren't explicit.

---

## What This Means for Your Scaffolding

### The Good News
Gemma can handle complex planning input with:
- Multiple options with dependencies
- Context about risk, scope, and impact
- References to upstream/downstream work

Gemma's Route B breakdown shows it **understands the work** and can articulate task scope.

### The Catch
Gemma needs **explicit decision criteria** to reason about trade-offs. Without them, it defaults to:
- Middle ground (safety)
- Concrete/implementation-focused work (pattern recognition)
- Proceeding with the default assumption (comfort action)

### Implications for Scaffolding

**You need one of these three:**

1. **Priority statement** — "Which of these three matters most to you?"
2. **Decision framework** — "You are optimizing for [X]. Given that, what's next?"
3. **Explicit question** — "Which route should be next? Your answer must justify the choice using dependency analysis."

Without one, Gemma will make a reasonable default choice but **won't explain why it chose it over others**.

---

## Gemma's Behavior as a Planning Oracle

### What It's Good At
- ✅ Understanding multi-layered architecture
- ✅ Identifying dependencies (even if not explicitly choosing based on them)
- ✅ Articulating task scope in detail
- ✅ Mapping stakeholders and impact
- ✅ Providing implementation-ready breakdowns

### What It Struggles With
- ❌ Making explicit trade-off decisions without guidance
- ❌ Ranking options without explicit criteria
- ❌ Proposing sequences or hybrid approaches (defaulted to single option)
- ❌ Asking clarifying questions back (just assumed Route B)

### Verdict
Gemma 4 26B is **a solid tactical executor** but **not a strategic planner on its own**. It needs:
- Explicit decision criteria
- Clear weighting
- Permission to ask clarifying questions (which it didn't exercise)

---

## Recommended Next Test

Send Gemma this revised prompt:

```markdown
# Planning Task: Which Route Next?

**Decision Criteria:** You are optimizing for **organizational impact**.
The Router design session is scheduled for mid-May and is currently blocked 
waiting for the Node Registry Schema (Route A). 

Given this, which route should you work on next?

Your answer must:
1. Explain which route unblocks the most critical path
2. Identify dependencies (what must happen before what)
3. Propose a sequencing if multiple routes should be done in parallel
4. Flag any risks or unknowns
```

**Expected outcome:** Gemma should now choose Route A and explain the dependency chain.

If Gemma still chooses Route B despite this context, you'll know that **explicit temporal/milestone context** is needed in scaffolding, not just dependency analysis.

---

## Summary: What Scaffolding Actually Works

| Scaffolding Type | Effect | Evidence |
|---|---|---|
| **Context (hardware, infrastructure)** | ✅ Helps. Gemma uses it. | Gemma correctly understood Daemon's burst mode complexity |
| **Dependency diagram** | ⚠️ Partially. Gemma reads it but doesn't weight by it | Gemma knew A→Router, but chose B anyway |
| **Risk/complexity assessment** | ⚠️ Partially. Gemma cites it but doesn't use it to choose | Gemma noted B is "low risk" but didn't compare to A |
| **Explicit decision criteria** | ❌ Missing. This is what failed. | Gemma had no way to reason about Route A (org impact) vs. B (implementation clarity) |
| **Milestone/timeline context** | ❓ Unknown. Not tested yet. | See "Recommended Next Test" above |

**Conclusion:** The planning input was 80% correct. It was missing **one section**: explicit decision criteria or a timeline/priority context. Add that, and Gemma should handle the routing decision well.

---

## Implementation: What To Add To Future Planning Inputs

```markdown
## Decision Context

**Timeline:** Router design session scheduled [DATE]. Node Registry Schema required by [DATE].
**Organizational priority:** [What matters most]
**Success metric:** [How you'll know the right choice was made]

Example:
"Timeline: Router session in 2 weeks. Node Registry Schema is the blocker. 
Organizational priority: Unblock scheduled meetings over new ecosystem features. 
Success metric: Node Registry Schema is ready for peer review before 2026-04-27."

---

Given this context, which route should be next?
```

This addition would likely have changed Gemma's answer from Route B → Route A.