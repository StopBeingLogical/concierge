# Handoff: Update Project Files
*Session: April 21-22, 2026 — Ergaster/Atlas setup*

---

## Task

Update project files in the Claude.ai project store with tonight's work.

---

## Files to Update or Create

### 1. `Claude_Platform_FAQ.md` — Add new Q&A entries

- **Claude Code desktop app Code tab** — local filesystem access, limitations, session sharing with CLI
- **Session sharing between desktop and CLI** — not direct; handoff via Continue in / `--teleport`
- **Agent SDK vs CLI headless (`claude -p`) billing** — SDK requires API key, CLI uses subscription quota
- **Remote access options** — SSH+tmux confirmed as primary, `remote-control` is research preview with caveats
- **Default model per chat** — no native setting, last-used model persists as soft default
- **Concurrent sessions** — no restriction, shared quota pool, quota burns proportionally across all surfaces
- **Claude Design** — launched April 17, research preview, powered by Opus 4.7, creates prototypes/slides/one-pagers, exports to PDF/PPTX/Canva

### 2. `Mneme_Integration_Config.md`
Already created this session. File is in outputs — add to project store as-is.

### 3. `Tmux_Cheatsheet.md`
Already created this session. File is in outputs — add to project store as-is.

### 4. `Ergaster_Setup.md` — Create new
Document Ergaster's current state:

**Hardware:**
- i9-13900HX, 64GB RAM, iGPU only, Ubuntu 24.04 (Noble)
- Role: orchestration node, remote dev workstation, CLI AI sessions

**Tools installed:**
- Claude Code CLI (v2.1.116)
- Gemini CLI (v0.38.2)
- pi coding agent (v0.68.0)
- rclone (Nextcloud mount)
- tmux with tmux-resurrect + tmux-continuum plugins
- Node.js v22 (via fnm)
- mosh, davfs2 removed

**Nextcloud:**
- Mounted at `~/nextcloud` via rclone
- Systemd service: `rclone-nextcloud.service`
- Virtual filesystem — no local storage, files live on Atlas
- Mneme accessible at `~/nextcloud/Mneme/`

**Ollama connections:**
- Kratos: `http://192.168.3.138:11434`
- Ergaster local: `http://192.168.3.143:11434`

**tmux:**
- Session named `AI`
- Windows: home, pi, gemini, claude
- Resurrect saves to `~/.local/share/tmux/resurrect/`
- Config at `~/.tmux.conf`

**pi config:**
- Extensions: `searxng-search.ts`, `turn-stats.ts`
- Config synced from Logos via rsync
- Points to Kratos Ollama by default

**Planned resident models on Ergaster Ollama:**
- `gemma4:e4b` — lightweight background tasks, file ops, summarization

### 5. `AI_User_Cheatsheet.md` — Consider adding

- **Session handoff seeds** — deliberate pattern for surface-agnostic continuity, more robust than any native session handoff feature. Works across desktop↔CLI, different machines, context resets.
- **Model tier escalation thresholds:**
  - Haiku — rubber ducking, simple Q&A, casual conversation
  - Sonnet — code generation, multi-step tasks, analysis, anything where quality matters
  - Opus — deep architecture planning, complex debugging, sustained long-context reasoning
- **TUI prototyping direction** — Go/Charm stack (Bubbletea + Lipgloss + Bubbles) for `bit`, Concierge's TUI frontend. Shared `theme.go` package as design language across future apps.

---

## Context Notes

- All referenced output files exist in this session's outputs
- Mneme is live at `~/nextcloud/Mneme/` on Ergaster — these docs should eventually live there
- Naming convention: hardware = Greek/Latin, software = Sumerian
- `Claude_Platform_FAQ.md` and `AI_User_Cheatsheet.md` already exist in project store — append, don't replace

---
*Generated: 2026-04-22 | Source: Claude Platform Q&A + Ergaster setup session*
