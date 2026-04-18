---
title: "Concierge — Filesystem Organization & Consolidation Seed"
document_type: seed
date: "2026-04-13"
status: reference
tags: ['atlas', 'nextcloud', 'filesystem', 'storage', 'concierge']
---

# CONCIERGE — Filesystem Organization & Consolidation Seed
**Date:** April 13, 2026  
**Purpose:** Handoff for dedicated TrueNAS dataset planning and consolidation session  
**Context:** Pre-RAG/Open WebUI filesystem architecture. Establish canonical storage structure before carving up for Tier 3 memory, artifacts, and KB corpus.

---

## Problem Statement

Current state: Nextcloud dataset is empty and not configured. Existing NAS shares and datasets scattered across TrueNAS. Need to consolidate and organize before:
1. Creating dedicated `concierge-kb` dataset for RAG + Tier 3 memory + artifacts
2. Configuring Open WebUI filesystem access
3. Setting up Nextcloud as a UI window to the actual data (not the primary storage)
4. Establishing canonical storage locations for Bit artifact handoff

**Goal of this session:** Audit current filesystem state, organize all datasets/shares, create a canonical structure, decide what gets consolidated where.

---

## Current Infrastructure

**TrueNAS Scale on Atlas:**
- Ryzen 5700G, 64GB RAM
- 3×12TB RaidZ1 (configured)
- Nextcloud community app running (dataset currently empty)
- Atlas also hosts: Homarr, Open WebUI, SearXNG, Forgejo, Nisaba, Tailscale, nginx-proxy-manager

**Existing Services Using Filesystem:**
- Nextcloud (empty dataset)
- Nisaba (Docker app — what dataset?)
- Forgejo (running — what dataset?)
- TrueNAS itself (/boot, /var, system)

**Current NAS Shares/Folders:**
- [TO BE INVENTORIED] — existing shared folders, datasets, mount points

---

## Tasks for This Session

### 1. Inventory Current State
```
For each dataset/share:
- Dataset name and mountpoint
- Current size and usage
- What service/data is stored there
- Important files or structure
- Whether it's in active use or deprecated
```

Run on Atlas:
```bash
# List all datasets
zfs list -o name,used,avail,mountpoint

# List all SMB shares (if any)
sudo smbstatus -S

# Check TrueNAS app storage
# (via UI or docker inspect for volumes)
```

### 2. Identify What Needs Consolidation
- What's currently scattered that should be together?
- What datasets are redundant?
- What's critical vs. deprecated?
- Space utilization — any unused datasets?

### 3. Design Canonical Structure
```
Proposed layout (to be finalized):

tank/ (or your pool name)
├── system/ (TrueNAS system datasets)
├── concierge/
│   ├── kb/ (KB corpus, Tier 3 memory, RAG input)
│   │   ├── documents/ (source docs)
│   │   ├── tier3-memory/ (vector index)
│   │   └── artifacts/ (generated files)
│   ├── infrastructure/ (configs, backups, metadata)
│   └── working/ (temp, scratch, logs)
├── nas/ (standard NAS shares)
│   ├── photos/
│   ├── media/
│   ├── documents/
│   └── [other standard folders]
└── services/ (app-specific storage)
    ├── nextcloud/ (scratch only)
    ├── forgejo/ (git data)
    └── nisaba/ (app data)
```

### 4. Create Migration Plan
- Which existing data goes where?
- Order of operations (what must be done first)?
- Downtime requirements (if any)?
- Backup/rollback strategy?

### 5. Document Final Structure
- Datasets created
- Mountpoints assigned
- Permissions set (who accesses what?)
- Nextcloud External Storage mappings planned
- Open WebUI volume mount paths defined

---

## Success Criteria

By end of session:
- [ ] Current filesystem state fully audited
- [ ] Decision made on consolidation strategy
- [ ] New dataset structure designed and documented
- [ ] Migration plan written out
- [ ] Ready to execute (but not yet executing)

---

## Handoff for Next Session (WebUI Configuration)

Once filesystem is organized, the next session will:
1. Create the `concierge-kb` dataset (or whatever you name it)
2. Mount datasets into Open WebUI container
3. Configure Nextcloud External Storage for UI access
4. Create custom functions in Open WebUI for RAG/artifact access
5. Test end-to-end: ingest → search → generate → save

---

## Tools & References

**TrueNAS CLI:**
- `zfs list` — view dataset hierarchy
- `zfs create` — create new datasets
- `zfs set` — configure datasets
- `zfs rename` — reorganize
- `zfs snapshot` — backup before migration

**TrueNAS UI:**
- Storage → Pools → manage datasets
- Sharing → Windows Shares (SMB) — configure access
- Apps → app management (for Nextcloud, Nisaba configs)

---

*Handoff seed created April 13, 2026. Use this to organize and consolidate Atlas filesystem before configuring RAG/Open WebUI access. Return to main Concierge chat once filesystem structure is finalized.*
