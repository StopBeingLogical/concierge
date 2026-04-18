---
title: "Analysis: Karpathy LLM Wiki Pattern vs Concierge Architecture"
document_type: analysis
date: "2026-04-11"
status: reference
tags: ['memory', 'tier-3', 'semantic-memory', 'compilation', 'lint', 'planner', 'knowledge-base', 'cache-prefill']
---

# Analysis: Karpathy LLM Wiki Pattern vs Concierge Architecture

*Karpathy's LLM Wiki is a knowledge management pattern that went viral (~12M views on X) approximately one week before this analysis. The core idea: treat an LLM as a compiler that transforms raw source documents into a structured, interlinked markdown wiki, maintained continuously through ingest, lint, and backfiling cycles. Analyzed here for relevance to Concierge's Tier 3 memory layer.*

---

## What the LLM Wiki Is

The pattern is built around a compiler analogy: raw source documents are source code, the LLM is the compiler, and the structured wiki is the compiled executable. The practical architecture has three components:

- **`raw/`** — immutable source documents (articles, notes, job outputs, anything)
- **`wiki/`** — compiled structured pages with backlinks and cross-references
- **Schema file (CLAUDE.md)** — defines structure, naming conventions, page templates, and operational rules; transforms a generic LLM into a disciplined knowledge worker

The operational loop cycles continuously: **ingest → query → lint → backfile → repeat.**

The specific innovation over RAG: synthesis happens at ingest time, not query time. The wiki stores pre-compiled, pre-linked knowledge rather than raw chunks. At query time the model reads structured pages rather than excavating raw material.

A v2 extension (rohitg00) added memory lifecycle management: confidence scoring, supersession tracking, Ebbinghaus-curve retention decay, consolidation tiers (working → episodic → semantic → procedural), and a typed entity/relationship graph layered on top of the pages.

---

## Core Verdict

**The LLM Wiki is not a competing or novel architecture relative to Concierge — it is a named instance of the continuous index/analysis/cache-prefill preparation task already envisioned in the Concierge design.**

Karpathy packaged as a novel pattern what Concierge already had as a first-principles design decision: synthesis work belongs at compile time, not query time. The Concierge Memory Spec describes the tier architecture; the LLM Wiki provides operational detail for what running that tier looks like in practice.

---

## What Maps Directly (Already in Concierge by Another Name)

| LLM Wiki concept | Concierge equivalent |
|---|---|
| `raw/` source folder | Unprocessed job outputs, ingested documents |
| Compilation pass | Continuous index / cache-prefill prep task |
| `wiki/` compiled pages | Tier 3 semantic memory |
| Schema file / CLAUDE.md | Task Package schema + memory tier conventions |
| Index.md + log.md navigation files | Tier 3 index structure |
| LLM-as-compiler | Planner executing synthesis jobs |
| No vector DB needed at personal scale | Consistent with Concierge's progressive disclosure model |

---

## What the LLM Wiki Adds (Operational Detail Not Yet in the Memory Spec)

These are not architectural additions — they are concrete operational mechanisms that the Memory Spec describes in structural terms but not procedural terms. Worth incorporating as spec detail, not as new layers.

### 1. The Lint Pass — Named, Scheduled, with Enumerated Failure Modes

The LLM Wiki defines "linting" as a specific, schedulable health-check job with explicit failure categories:
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages with no inbound links
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps fillable by external search

In Concierge terms: a low-priority background Planner job on a schedule with a typed output contract enumerating detected issues. Not user-initiated. Not continuous — periodic. This is the "how Tier 3 stays healthy" operational spec that the Memory Spec currently lacks.

### 2. The Backfiling Decision — Quality-Scored Gate at Job Close

The LLM Wiki makes explicit that query results and analysis outputs should be evaluated for filing back into the wiki as new pages. The question asked at the end of every interaction: *"Is this output durable knowledge worth preserving, or ephemeral?"*

In Concierge terms: a Foreman post-execution step after job close that runs a quality-scored "worth promoting to Tier 3?" decision on job outputs before they age out of working context. This is the mechanism by which completed jobs contribute to compounding knowledge rather than disappearing into logs.

### 3. The Supersession Model — Version Control for Knowledge Content

When a new source contradicts an existing wiki page, the old version is preserved but marked stale rather than deleted. Linked, timestamped, old version archived.

In Concierge terms: Tier 3 entries need a `status` field (current / superseded / deprecated) and a `superseded_by` reference. The Memory Spec probably doesn't address this explicitly yet. Without it, Tier 3 has no way to handle evolving knowledge without either accumulating contradictions or destroying provenance.

---

## Where the LLM Wiki Pattern Does Not Apply

The LLM Wiki is a single-user, single-node pattern with no concept of:
- Which node is responsible for compilation (Concierge: Planner, not Workbees)
- Job contracts or typed output schemas
- Multi-node coordination or distributed access to the compiled wiki
- Access control over who can write to compiled memory tiers

These gaps don't invalidate the operational detail above — they just mean the pattern needs to be applied at the correct layer (Planner-owned Tier 3 operations) rather than wholesale adopted.

---

## Recommended Concierge Integration Points

1. **Memory Spec addendum** — add the lint pass as a named scheduled Planner job with enumerated failure mode categories
2. **Memory Spec addendum** — add the supersession model (status field, superseded_by reference, archive-not-delete behavior) to Tier 3 entry schema
3. **Technical Spec open item** — add post-execution backfiling decision to Foreman job-close sequence: quality-scored gate determining whether job outputs are promoted to Tier 3
4. **Public communications** — the compiler analogy (raw → LLM → wiki) is a clean way to explain Concierge's Tier 3 memory to a technical audience on GitHub; consider borrowing the framing
