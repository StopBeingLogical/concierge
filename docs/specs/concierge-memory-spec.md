---
title: "Concierge — Memory System Specification"
document_type: spec
version: "5.0"
date: "2026-03"
status: current
tags: ['memory', 'tier-0', 'tier-1', 'tier-2', 'tier-3', 'vector-store', 'nidaba']
---

# Concierge: Memory System Specification

*The Technical Spec defines the contract. This document defines what's behind it.*

*v5 — March 2026*

---

## Framing

The Concierge memory system is not a database bolted onto a chat interface. It is the substrate that makes Concierge a continuously operating cognitive infrastructure rather than a stateless request-response loop.

Four distinct tiers serve four distinct purposes. Each has its own persistence model, write discipline, and access pattern. None of the four is optional. Together they give the system a working memory, an immutable audit trail, a durable knowledge store, and a semantic search archive.

**The Technical Spec (Section 9) is the authoritative interface contract.** This document defines the internal implementation of each tier — schemas, storage backends, write protocols, query interfaces, and the reference resolution protocol. When this document and the Technical Spec disagree, the Technical Spec governs the interface. This document governs everything below it.

---

## Tier Overview

| Tier | Name | Persistence | Write authority | Primary reader |
|---|---|---|---|---|
| Tier 0 | Active context | Session only | Bit | Bit, Planner |
| Tier 1 | Event log | Permanent | All layers (append) | Planner, Bit |
| Tier 2 | Structured facts | Persistent | Human-confirmed | Bit, Planner |
| Tier 3 | Vector archive | Persistent | NIDABA enrichment | Planner (via search) |

---

## Tier 0 — Active Context

### Purpose

Tier 0 is the system's short-term working memory for a single session. It holds the minimal in-flight state required for Bit and Planner to maintain continuity within a session — the current intent under development, active job references, and the current conversation thread.

Tier 0 does not persist beyond the session. When the session ends, Tier 0 is discarded. Nothing in Tier 0 is logged to Tier 1 — Tier 1 captures events, not session state. Nothing in Tier 0 is copied to Tier 2 — Tier 2 writes require explicit human confirmation.

### Storage

In-process memory in the Bit application process. Not written to disk. Not transmitted over the network. Tier 0 lives entirely in Bit's process space and is cleared on process exit.

### Schema

```json
{
  "schema_version": "1.0",
  "session_id": "<uuid v4 — generated at session start>",
  "session_started_at": "<ISO8601>",
  "active_intent": {
    "intent_id": "<uuid — null if no intent in progress>",
    "raw_input": "<the human's current expression — updated as conversation progresses>",
    "draft_intents": ["<candidate interpretations under development>"],
    "status": "<drafting|emitted|awaiting_plan|awaiting_approval|executing>"
  },
  "active_jobs": [
    {
      "job_id": "<uuid>",
      "status": "<queued|running|paused|completed|failed>",
      "plan_id": "<uuid>",
      "last_event_at": "<ISO8601>"
    }
  ],
  "conversation": [
    {
      "turn_id": "<uuid>",
      "role": "<human|bit>",
      "content": "<turn content>",
      "timestamp": "<ISO8601>",
      "intent_ref": "<intent_id if this turn produced an intent — null otherwise>"
    }
  ],
  "context_refs_resolved": [
    {
      "ref_id": "<from context_refs in Intent Artifact>",
      "tier": 0,
      "resolved_value": "<resolved fact or preference>"
    }
  ]
}
```

### Lifecycle

- Created: on session start by Bit
- Updated: continuously by Bit as conversation progresses
- Read by Planner: via Bit's defined interface only — the Planner does not access Tier 0 directly
- Cleared: on session end, process exit, or explicit session reset

### Planner Access to Tier 0

The Planner's read access to Tier 0 is mediated entirely through Bit. The Technical Spec states: "Tier 0: Bit's working memory only — Planner updates via Bit's defined interface, not directly."

In practice: when the Planner needs session state (current intent status, active job list), Bit provides a context snapshot as part of the message payload. The Planner does not hold a connection to Tier 0's storage — it receives a point-in-time view from Bit.

**Planner context snapshot (included in Planner request payloads when relevant):**

```json
{
  "session_id": "<uuid>",
  "active_intent_id": "<uuid — null if none>",
  "active_job_ids": ["<uuid>"],
  "conversation_turns_since_last_intent": 0
}
```

### Invariants

- Tier 0 is never written to disk
- Tier 0 is never transmitted between systems
- Session end clears Tier 0 — there is no tier-0 recovery after a crash
- The Planner reads Tier 0 only via Bit-provided snapshots — never directly

---

## Tier 1 — Event Log

### Purpose

Tier 1 is the system's immutable audit trail. Every job event, state transition, integrity violation, and scheduling event writes to Tier 1. Nothing is ever deleted from Tier 1. Nothing is ever modified in Tier 1 after write.

Tier 1 answers the question: *what happened, and in what order?*

### Storage

Append-only log file on local filesystem. Structured as newline-delimited JSON (NDJSON). One record per line. Writes are fsync'd before the write is considered complete — a record that is not on disk is not a record.

**Log file location:** `$CONCIERGE_DATA_DIR/tier1/events.ndjson`

**Rotation policy:** when the active log file exceeds `tier1.max_file_size_mb` (default 256 MB), a new log file is opened. Closed log files are never deleted. Rotation is transparent to readers.

**Compaction:** not permitted. Tier 1 records are permanent. No compaction, summarization, or pruning of any kind.

### Record Schema

```json
{
  "schema_version": "1.0",
  "record_id": "<uuid v4>",
  "written_at": "<ISO8601 — millisecond precision>",
  "emitting_layer": "<bit|planner|router|foreman|workbee>",
  "event_type": "<string — see taxonomy below>",
  "job_id": "<uuid — null for system events>",
  "execution_id": "<uuid — null if pre-execution>",
  "step_id": "<string — null if job-level event>",
  "payload": {}
}
```

**record_id** is UUID v4 — unique per record, no semantic content.

**written_at** uses the clock of the system writing the record. Cross-system clock skew is expected. The event log is ordered by write time within a single system. Cross-system ordering uses the `issued_at` field in the event payload, not `written_at`.

### Event Taxonomy

The event types written to Tier 1 are a superset of the execution events defined in Technical Spec Section 6. Tier 1 adds system-level and scheduling events not visible in the execution event stream.

**Job lifecycle events** (emitting layer: planner):

| event_type | Emitted when |
|---|---|
| `job.created` | Intent Artifact received by Planner |
| `job.plan_generated` | Execution Plan generated |
| `job.foundation_required` | Planner detects tool gap, raises Handanza |
| `job.approved` | Human approves Execution Plan |
| `job.denied` | Human denies Execution Plan — job enters Harkanza |
| `job.revision_requested` | Human requests plan revision |
| `job.resubmitted` | Human revises intent and resubmits from Harkanza |
| `job.queued` | Job Spec accepted by Router |
| `job.started` | First chunk dispatched |
| `job.completed` | All steps complete, Planner validates |
| `job.partial` | Execution complete with some failures |
| `job.failed` | Planner declines result |
| `job.paused` | NEEDS_INFO signal received |
| `job.resumed` | Human provides required input |
| `job.capability_exceeded` | Router cannot service step at acceptable quality |
| `job.cancelled` | Human cancels |
| `job.planner_validated` | Planner completes result validation |
| `job.foundation_complete` | Hašatar task complete, original job re-evaluated |

**Step lifecycle events** (emitting layer: foreman, workbee):

| event_type | Emitted when |
|---|---|
| `step.started` | Step begins executing |
| `step.completed` | Step finishes successfully |
| `step.failed` | Step fails |
| `step.timeout` | Step exceeds time budget |
| `step.skipped` | Step skipped due to dependency failure |
| `step.retrying` | Step retrying after failure |
| `step.paused` | Step emits NEEDS_INFO |
| `step.resumed` | Step resumes after NEEDS_INFO resolved |

**Scheduling events** (emitting layer: router):

| event_type | Emitted when |
|---|---|
| `chunk.posted` | Work Chunk posted to work pool |
| `chunk.leased` | Chunk leased by a Foreman |
| `chunk.completed` | Chunk result received and accepted |
| `chunk.failed` | Chunk result received and declined or lease expired |
| `chunk.returned_to_pool` | Lease expired, chunk re-available |
| `node.registered` | New system registered with Router |
| `node.reindex_required` | Heartbeat hash mismatch |
| `node.health_check_issued` | Router initiates health check |
| `node.health_check_resolved` | Health check response processed |
| `node.removed` | Node marked alive: false |

**Integrity events** (emitting layer: detecting layer):

| event_type | Emitted when |
|---|---|
| `integrity.violation` | SHA256 mismatch at any layer boundary |

Integrity events are written with full violation detail and are never purged regardless of any retention policy.

**System events** (emitting layer: bit, planner):

| event_type | Emitted when |
|---|---|
| `session.started` | New Bit session begins |
| `session.ended` | Bit session ends |
| `memory.tier2_write` | Tier 2 fact written after human confirmation |
| `memory.tier2_superseded` | Tier 2 fact superseded by newer write |
| `memory.tier3_enriched` | Tier 3 enrichment completed for a job |
| `gap.detected` | Capability or knowledge gap surfaced |
| `gap.resolved` | Gap resolved |
| `gap.dismissed` | Gap dismissed by human |

### Query Interface

Tier 1 is not a relational database. It is an append-only log. The supported query operations reflect this.

**Full scan:** read all records. Used for audit and integrity verification.

**Filtered scan:** read records matching one or more of: `job_id`, `execution_id`, `emitting_layer`, `event_type`, date range on `written_at`.

**Job trace:** retrieve all Tier 1 records for a given `job_id`, ordered by `written_at`. This reconstructs the full audit trail for a single job.

**Integrity event report:** retrieve all records where `event_type = integrity.violation`. Used for periodic integrity review.

The query interface is provided by the Tier 1 log reader service — a read-only process that does not hold write access to the log files. Write access is exclusive to the layer agents.

### Invariants

- Append-only: no record is ever modified or deleted after write
- fsync required: a record not fsynced is not a record
- Integrity events retained indefinitely regardless of any other policy
- Cross-system write order is not guaranteed — use payload `issued_at` for causal ordering, not `written_at`
- No compaction, summarization, or pruning permitted

---

## Tier 2 — Structured Facts

### Purpose

Tier 2 is the system's durable, human-curated knowledge store. It holds facts about the user, the user's context, and the user's preferences that inform Planner behavior across sessions. Unlike Tier 0 (cleared per session) and Tier 1 (append-only events), Tier 2 holds living facts — things that are true now and should remain true until explicitly changed.

Tier 2 answers the question: *what do we know about this person and their context that should shape how we work for them?*

**Critical discipline:** Tier 2 is never updated silently. Every write to Tier 2 requires explicit human confirmation through Bit. The Planner may propose a Tier 2 write. Bit surfaces the proposal. The human confirms or declines. Nothing writes to Tier 2 without this sequence completing.

### Storage

Structured JSON document store on local filesystem. Each fact is a document. Documents are keyed by `fact_id`. A simple indexed store — not a relational database, not a vector store.

**Store location:** `$CONCIERGE_DATA_DIR/tier2/facts/`

**Index file:** `$CONCIERGE_DATA_DIR/tier2/index.json` — contains all `fact_id`, `fact_type`, `key`, and `status` entries for fast lookup without reading full fact documents.

### Fact Schema

```json
{
  "schema_version": "1.0",
  "fact_id": "<uuid v4>",
  "fact_type": "<preference|setting|named_entity|behavioral_pattern>",
  "key": "<human-readable identifier — kebab-case, stable across versions>",
  "value": "<string|number|boolean|object>",
  "value_type": "<string|number|boolean|json_object>",
  "description": "<one sentence — what this fact represents>",
  "source": "<human_stated|inferred_and_confirmed|system_default>",
  "written_at": "<ISO8601>",
  "written_by": "<session_id of the session in which this was confirmed>",
  "confirmed_by": "<human identifier>",
  "supersedes": "<fact_id — null if original>",
  "status": "<active|superseded|archived>",
  "context_refs_type": "<preference|setting|named_entity|behavioral_pattern>"
}
```

### Fact Types

**`preference`** — how the user prefers the system to behave. Examples: preferred output format, verbosity level, whether to show reasoning steps, preferred language for technical content.

**`setting`** — explicit configuration values. Examples: approved sources list additions the user has confirmed, default priority lane for user-initiated jobs, workspace path.

**`named_entity`** — named things in the user's world that Concierge should recognize and use. Examples: project names and their descriptions, team member names and roles, frequently referenced paths or URLs.

**`behavioral_pattern`** — calibrated observations about how the user works, confirmed by the human. Examples: "user reviews candidate outputs before selection", "user prefers step-by-step reasoning visible in outputs", "user typically requests multiple candidates for writing tasks."

### Write Protocol

No fact enters Tier 2 without completing this sequence:

**Step 1 — Proposal.** The Planner or Bit proposes a new fact or fact update. The proposal includes: proposed `key`, `value`, `fact_type`, `description`, `source`.

**Step 2 — Surfacing.** Bit presents the proposal to the human in plain language: "The system has observed X and would like to remember it as: [fact description]. Confirm to save, decline to discard."

**Step 3 — Human decision.** Human confirms or declines. Decline discards the proposal — nothing is written. No retry on the same proposal without the human re-initiating.

**Step 4 — Write.** On confirmation, Bit writes the fact document. The confirmation is logged to Tier 1 as `memory.tier2_write`. The index is updated atomically.

**Step 5 — Supersession (for updates).** If a confirmed write updates an existing fact with the same `key`, the previous fact document is marked `status: superseded` with a reference to the new `fact_id`. The superseded record is retained. Tier 1 logs `memory.tier2_superseded`.

**Human-initiated writes:** the human may add, edit, or archive facts directly through Bit's memory management interface without a Planner proposal. The same write protocol applies — no fact writes without human confirmation.

### Read Protocol

Bit reads Tier 2 facts in two ways:

**Direct lookup:** by `fact_id` or `key` — used when displaying facts in the memory management interface.

**Context loading:** at session start or when composing an Intent Artifact, Bit loads a set of active facts relevant to the current conversation domain. The set is determined by a lightweight keyword match against fact `key` and `description` fields. This is not a semantic search — that is Tier 3's role. The result is included in the context provided to the Planner.

The Planner reads Tier 2 only through the `context_refs` mechanism in the Intent Artifact — it does not query Tier 2 directly. Bit is the Tier 2 reader.

### `context_refs` Integration

The `context_refs` field in the Intent Artifact carries references to specific Tier 2 facts that are relevant to the current intent. Bit populates `context_refs` from the context-loaded fact set.

```json
"context_refs": [
  {
    "tier": 2,
    "ref_id": "<fact_id>",
    "ref_type": "<preference|setting|named_entity|behavioral_pattern>",
    "key": "<human-readable key>",
    "resolved_value": "<the value of the fact at time of Intent Artifact emission>"
  }
]
```

`resolved_value` is included inline — the Planner does not need to resolve the reference against storage. The value is current as of Intent Artifact emission. If the fact changes between emission and plan generation (unlikely but possible in a long session), the Planner uses the `resolved_value` in the artifact, not the current storage value.

### Invariants

- No Tier 2 write occurs without explicit human confirmation
- Superseded facts are retained — never deleted
- `status: archived` is set when a human explicitly removes a fact — the record is retained, not deleted
- `source: inferred_and_confirmed` is the only valid source for Planner-proposed facts — the human confirmation is what makes it valid
- Tier 1 logs every Tier 2 write and supersession

---

## Tier 3 — Vector Archive

### Purpose

Tier 3 is the system's semantic search index. It grows over time from two sources: NIDABA enrichment (facts and context extracted from completed jobs) and direct corpus write operations. Tier 3 answers fuzzy, semantic questions that Tier 2's exact-key lookup cannot answer — finding relevant past context, surfacing related knowledge, and providing the Planner with domain-appropriate background before plan generation.

### Storage

Local vector store. The vector store holds embedding vectors alongside document chunks and metadata. The embedding model is a small, fast model suitable for local inference on CPU or iGPU — not an ensemble member, not a quality-critical path.

**Vector store location:** `$CONCIERGE_DATA_DIR/tier3/`

**Embedding model:** configured in `concierge.config.json` under `memory.tier3.embedding_model`. Defaults to a small sentence-transformer class model compatible with the host architecture. The embedding model is treated as a Tool Pool item — it is onboarded, versioned, and hash-verified like any other tool.

**Re-embedding policy:** when the embedding model is updated, existing embeddings become stale. A re-embedding background task (P3 priority) is triggered automatically. During re-embedding, the old index remains queryable. The new index replaces the old atomically on completion.

### Document Chunks

Tier 3 stores documents as chunks — not as whole documents. Chunking allows precise retrieval without loading irrelevant context.

**Chunk schema:**

```json
{
  "schema_version": "1.0",
  "chunk_id": "<uuid v4>",
  "source_type": "<nidaba_enrichment|corpus_write|execution_summary|job_artifact>",
  "source_id": "<job_id, artifact_id, or corpus document id>",
  "written_at": "<ISO8601>",
  "content": "<text content of this chunk>",
  "metadata": {
    "domain": "<domain or topic tag>",
    "job_id": "<uuid — null if not job-derived>",
    "package_id": "<task package — null if not job-derived>",
    "artifact_type": "<null if not artifact-derived>",
    "nidaba_enrichment_batch_id": "<uuid — null if not NIDABA-derived>"
  },
  "embedding_model_id": "<tool_id of the embedding model that produced the embedding>",
  "embedding_model_version": "<semver>",
  "embedding": ["<float — 768 or 1024 dimensional, model-dependent>"]
}
```

### NIDABA Enrichment Protocol

NIDABA enrichment is the process by which completed job outputs are distilled into Tier 3. It runs as a declared side effect of Task Package execution — only for packages with `telemetry.nidaba_enrichment: true`.

**Trigger:** Planner validation completes with `result: accepted`. Enrichment is initiated by the Planner after validation, before artifact delivery to Bit. Enrichment does not block delivery.

**Enrichment sequence:**

1. **Extract.** The Planner (or a dedicated enrichment Task Package) extracts facts, summaries, and knowledge units from the job's TaskResults and artifacts.
2. **Chunk.** Extracted content is chunked into Tier 3 chunk units. Chunk size target: 512 tokens, with a 64-token overlap between adjacent chunks.
3. **Embed.** Each chunk is embedded using the configured Tier 3 embedding model. This runs on the local system — it is not dispatched to the fleet.
4. **Write.** Chunks and embeddings are written to the Tier 3 vector store.
5. **Log.** Tier 1 records `memory.tier3_enriched` with the enrichment batch ID and count of chunks written.

**NIDABA enrichment is not reversible.** Chunks written to Tier 3 are permanent. If an enrichment batch produces clearly incorrect content, the chunks can be marked `status: deprecated` but are not deleted. A corrected re-enrichment can supersede deprecated chunks.

### Corpus Write Operations

Independent of job execution, the human or the system may write documents directly to Tier 3 as corpus enrichment. This is the mechanism for bootstrapping domain knowledge before jobs have been run.

**Sources:** approved external documents fetched by a corpus enrichment Task Package, local documents explicitly loaded by the human, output from the Gap Resolver's knowledge gap resolution process.

**All corpus writes follow the same chunking and embedding sequence as NIDABA enrichment.** Source type is recorded as `corpus_write` rather than `nidaba_enrichment`.

### Query Interface

Tier 3 is queried by the Planner during plan generation to retrieve relevant background context for a given intent. Bit may also query Tier 3 to populate conversational context.

**Semantic search request:**

```json
{
  "schema_version": "1.0",
  "query_id": "<uuid>",
  "query_text": "<natural language query derived from the current intent>",
  "top_k": 10,
  "filters": {
    "domain": "<optional domain filter>",
    "source_type": "<optional — nidaba_enrichment|corpus_write|execution_summary|job_artifact>",
    "written_after": "<ISO8601 — optional>",
    "package_id": "<optional — restrict to results from a specific Task Package>"
  },
  "min_similarity": 0.65
}
```

**Semantic search response:**

```json
{
  "schema_version": "1.0",
  "query_id": "<uuid>",
  "results": [
    {
      "chunk_id": "<uuid>",
      "similarity_score": 0.0,
      "content": "<chunk text>",
      "metadata": {}
    }
  ],
  "total_results": 0,
  "embedding_model_id": "<model used to embed the query>"
}
```

The query is embedded using the same model configured for the store. Cross-model similarity scores are meaningless — the store refuses queries if the configured embedding model doesn't match the model used to embed the stored chunks.

### Invariants

- Tier 3 writes occur only through NIDABA enrichment or explicit corpus write operations
- NIDABA enrichment is a declared package property — it is not an implicit behavior of any layer
- The embedding model is a versioned, hash-verified Tool Pool item
- Query embedding model must match the store's indexed embedding model
- Chunks are permanent — deprecated, not deleted
- Re-embedding on model update is P3 background work; old index remains queryable until replacement is complete

---

## Reference Resolution Protocol

The `context_refs` field in the Intent Artifact is the formal mechanism by which memory tier content reaches the Planner. This section defines the full resolution protocol.

### What `context_refs` Carries

`context_refs` is populated by Bit at Intent Artifact emission time. It carries:
- References to active Tier 2 facts that are relevant to the intent
- Resolved values inline (Planner does not query storage)
- Tier identifier so the Planner knows where the value originated

Tier 3 content reaches the Planner through a separate channel — not `context_refs`. Tier 3 is queried by the Planner independently during plan generation, using the intent text as the query. `context_refs` is strictly for Tier 2 (and potentially Tier 0 session state in future versions).

### Resolution Sequence

1. **Intent emission.** Bit emits an Intent Artifact with `context_refs` populated from the active Tier 2 fact set.

2. **Planner receipt.** Planner receives the Intent Artifact and validates its SHA256 hash.

3. **Tier 2 resolution.** For each entry in `context_refs`, the Planner reads `resolved_value` inline. No storage query required. The value is treated as authoritative for this plan generation cycle.

4. **Tier 3 query.** Planner derives a semantic search query from the intent text. Sends query to Tier 3. Receives top-k chunks. These are used as background context for plan generation — they inform the Planner's matching and gap resolution logic.

5. **Combined context.** Planner uses Tier 2 resolved values and Tier 3 retrieved chunks together with the ranked intents to generate the Execution Plan. Neither source overrides the intent — they inform it.

6. **Tier 1 audit.** Context references used in plan generation are logged to Tier 1 as part of the `job.plan_generated` event payload.

### Staleness Handling

`context_refs` resolved values are point-in-time. If a Tier 2 fact changes between intent emission and plan approval (rare but possible), the Planner uses the `resolved_value` from the Intent Artifact — not the current storage value.

This is intentional: the plan was generated against a specific fact set. Changing the fact set under the plan without re-generating the plan could produce plan/fact inconsistency. If the human changes a Tier 2 fact while a job is in `pending_approval`, the correct action is to request plan revision so the Planner can incorporate the updated fact.

### Invariants

- Tier 2 values in `context_refs` are resolved inline at emission — Planner does not query Tier 2 directly
- Tier 3 is queried by the Planner, not by Bit — Tier 3 content is not in `context_refs`
- Tier 0 session state reaches the Planner via Bit-provided snapshots — not via `context_refs`
- Context references used in plan generation are logged to Tier 1

---

## Memory System Invariants

These invariants are binding across all tiers and all layers. They expand the invariants stated in Technical Spec Section 9.

**Access control:**
- No layer reads from or writes to a tier not listed in the read/write table in Technical Spec Section 9
- No layer bypasses another layer to access a tier — Planner does not read Tier 0 directly; it receives a snapshot from Bit

**Tier 0:**
- Never written to disk
- Never transmitted over the network
- Cleared on session end

**Tier 1:**
- Append-only — immutable after write
- fsync required for write completion
- Integrity events retained indefinitely, unconditionally
- No compaction, summarization, or deletion permitted

**Tier 2:**
- No write without explicit human confirmation through Bit
- Superseded facts retained — never deleted
- `source: inferred_and_confirmed` requires the confirmation step to have completed
- Every write logged to Tier 1

**Tier 3:**
- Write sources: NIDABA enrichment (declared package property) or explicit corpus write operation only
- Embedding model is a versioned Tool Pool item — changes trigger background re-embedding
- Chunks are permanent — deprecated, not deleted
- Query embedding model must match indexed embedding model

**Reference resolution:**
- `context_refs` carries Tier 2 resolved values inline — Planner does not query Tier 2 directly
- Resolved values are point-in-time at Intent Artifact emission
- Tier 3 is queried independently by the Planner during plan generation
- Plan generation context logged to Tier 1

---

*Document compiled from architecture sessions and design sessions — March 2026. Companion documents: Concierge_Philosophy_v5.md · Concierge_Hardware_Appendix_v5.md · Concierge_Technical_Spec_v5.md.*
