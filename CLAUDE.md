# Concierge — Session Seed & Instructions

**Project:** Concierge v5.0 — Personal Cognitive Infrastructure  
**Lead:** Bobby (senrew@gmail.com)  
**Status:** Specification Phase (locked), Implementation beginning (Bit layer)

---

## Session Start Checklist

When you start a session on Concierge, do this in order:

1. **Load project context** (5 min)
   - Read `README.md` (quick orientation)
   - Load `docs/seeds/concierge-session-seed.md` (compressed context)

2. **Check for changelog updates** (2 min)
   - Ask: "Should I consolidate pending changelog entries from `.changelog/UNRELEASED.md` into the appropriate CHANGELOG.md files?"
   - If yes: move one-liners to their destination files and reset UNRELEASED.md
   - If no: continue

3. **Navigate by task** — Use the README's "Quick Start: By Role" section

---

## Changelog Maintenance

**Location:** `.changelog/UNRELEASED.md` (working file), `**/CHANGELOG.md` (committed files)

**When making changes:**
- Add one-liners to `.changelog/UNRELEASED.md` under the relevant section
- At session start, I'll ask if you want to consolidate entries
- Before committing, I'll move entries to the appropriate CHANGELOG.md files

**Philosophy:** Top-level changelog records major changes only. Subdirectory changelogs capture details. See each CHANGELOG.md for format.

---

## Key Constraints (First-Class)

### Specs Are Locked
- `docs/specs/` contains locked specifications (v5.0)
- Do not suggest changes to specs without reading `docs/specs/concierge-philosophy.md` first
- Design is open; specs are closed

### Hardware Constraints
- **Logos:** 64GB shared macOS memory (Bit uses local models; scales to distributed)
- **Daemon:** 16GB VRAM per GPU (single-digit daily jobs)
- **Ergaster:** CPU-optimized (planning, not inference)

### Model Roles (Not Specific Models)
- Bit layer: 30B conversational + 4-7B deterministic
- Workbee ensemble: 4× 7B specialists + 1× 32B verifier
- Model selection research: `docs/research/bit-model-selection/`

---

## Related Projects

- **Enki** (`../enki/`) — Model evaluation framework (v1.0 production-ready, v2.0 architected)
  - Used to validate Bit layer model candidates
  - Changelog structure: `.changelog/UNRELEASED.md` + `**/CHANGELOG.md`

---

## Quick Links

| I want to... | Go to... |
|---|---|
| Understand core vision | `docs/specs/concierge-philosophy.md` |
| Get context fast (resuming) | `docs/seeds/concierge-session-seed.md` |
| Implement Bit | `docs/design/concierge-bit-application-design-notes.md` |
| Review model research | `docs/research/bit-model-selection/` |
| Update documentation | See "Changelog Maintenance" above |

---

## Communication

**Email:** senrew@gmail.com  
**Repository:** Forgejo instance + GitHub mirror (StopBeingLogical/concierge)  
**Last updated:** April 22, 2026
