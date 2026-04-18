---
title: "Atlas Filesystem Audit & Consolidation Plan"
document_type: reference
date: "2026-04-13"
status: reference
tags: ['atlas', 'truenas', 'filesystem', 'zfs', 'consolidation']
---

# Atlas Filesystem Audit & Consolidation Plan
**Date:** April 13, 2026  
**Status:** Planning Phase (Not Yet Executed)  
**Pool:** MemoryAlpha (3×12TB RaidZ1)

---

## Section 1: Current State Audit

### 1.1 Pool Overview
- **Pool Name:** MemoryAlpha
- **Size:** ~36TB raw (3×12TB RaidZ1)
- **Used:** 5.03T (14% utilization)
- **Available:** 16.6T
- **Secondary Pool:** boot-pool (system/OS, 427GB available, ignore for consolidation)

### 1.2 Current Dataset Hierarchy

```
MemoryAlpha/
├── .system/                          (2.07G) — TrueNAS system datasets (legacy mount)
│   ├── configs-*                     (14.3M)
│   ├── cores                         (128K)
│   ├── netdata-*                     (346M)
│   ├── nfs                           (192K)
│   ├── samba4                        (405K)
│   └── vm                            (128K)
├── Software/                         (2.05T) — Personal user data
├── Video/                            (1.03T) — Personal user data
├── bobby/                            (1.72T) — Personal user data (with ~500 auto snapshots!)
├── dez/                              (128K) — User folder (minimal)
├── forgejo/                          (21.0M) — Git server storage
│   ├── config                        (128K)
│   ├── data                          (2.81M)
│   └── postgres                      (17.9M)
├── minecraft/                        (2.56G) — Game server data
├── nasops/                           (128K) — Empty/unused
├── nextcloud/                        (650M) — NC app data
├── nextcloud-data/                   (128K) — Empty/unused
├── nextcloud-db/                     (142M) — NC database
├── nextcloud-users/                  (437K) — User file storage roots
│   ├── bobby/                        (170K)
│   └── masqued/                      (128K)
├── nisaba/                           (310M) — Custom Docker app (Concierge work)
└── ix-apps/                          (50.2G) — TrueNAS app infrastructure
    ├── app_configs/                  (24.8M)
    ├── app_mounts/                   (23.7G) — Per-app storage
    │   ├── ddns-updater/             (1.67M)
    │   ├── homarr/                   (3.71M)
    │   ├── makemkv/                  (9.57M)
    │   ├── nextcloud/                (2.80G) ← Nextcloud app code
    │   ├── nginx-proxy-manager/      (13.3M)
    │   ├── open-webui/               (20.9G) ← LLM interface + models
    │   ├── searxng/                  (298K)
    │   └── tailscale/                (288K)
    ├── docker/                       (26.0G) — Docker image/layer storage
    └── truenas_catalog/              (441M) — App catalog cache

Empty/Unused Mountpoints (check for data):
- /mnt/src_2tb/
- /mnt/src_4tb/
```

**Notable Issue:** `MemoryAlpha/bobby` has ~500 hourly auto-snapshots (bobby@auto-*) consuming metadata overhead.

### 1.3 Docker Service Mount Mapping

| Service | Source | Destination | Purpose |
|---------|--------|-------------|---------|
| **Nextcloud** (ix-nextcloud-nextcloud-1) | | | |
| | `/mnt/.ix-apps/app_mounts/nextcloud/html` | `/var/www/html` | App code |
| | `/mnt/MemoryAlpha/nextcloud` | `/var/www/html/data` | User data (root) |
| | `/mnt/MemoryAlpha/nextcloud-users/bobby` | `/var/www/html/data/bobby/files` | bobby's files |
| | `/mnt/MemoryAlpha/nextcloud-users/masqued` | `/var/www/html/data/masqued/files` | masqued's files |
| | `/mnt/MemoryAlpha/bobby` | `/mnt/MemoryAlpha/bobby` | (bind mount to local FS) |
| **Open WebUI** (ix-open-webui-open-webui-1) | | | |
| | `/mnt/.ix-apps/app_mounts/open-webui/data` | `/app/backend/data` | UI state, convo history |
| | `/mnt/.ix-apps/app_mounts/open-webui/ollama` | `/root/.ollama` | Ollama models cache |
| **Nisaba** (custom Docker app) | | | |
| | `/mnt/MemoryAlpha/nisaba/data` | `/data` | Concierge artifact store |
| **Forgejo** (ix-forgejo-forgejo-1) | | | |
| | `/mnt/MemoryAlpha/forgejo/config` | `/etc/gitea` | Git config |
| | `/mnt/MemoryAlpha/forgejo/data` | `/var/lib/gitea` | Repo data |

### 1.4 NFS Sharing Status
- **Current:** All datasets have `sharenfs=off` — **no NFS exports active**
- Observation: NFS infrastructure is set up but not in use

### 1.5 SMB Sharing Status
- **Current:** No active SMB shares (per `smbstatus -S`)
- Observation: SMB not configured despite samba4 dataset existing

---

## Section 2: Current State Problems & Inefficiencies

### 2.1 Storage Organization Issues

1. **Mixed User & App Data**
   - User files (Software, Video, bobby) mixed with app storage (nextcloud, forgejo, nisaba, minecraft)
   - No clear separation between personal NAS shares and Concierge work data

2. **Nextcloud Configuration Scattered**
   - App code in `/mnt/.ix-apps/app_mounts/nextcloud/html`
   - User data in `/mnt/MemoryAlpha/nextcloud`
   - User-specific files in `/mnt/MemoryAlpha/nextcloud-users/{bobby,masqued}`
   - Database in `/mnt/MemoryAlpha/nextcloud-db`
   - **Result:** 4 separate datasets for one app

3. **Snapshot Explosion**
   - `bobby` dataset has ~500 auto-snapshots (hourly) → metadata bloat
   - No evidence of cleanup policy
   - Snapshots are backups; this is defensive but unmanaged

4. **Unused/Empty Datasets**
   - `/mnt/MemoryAlpha/nextcloud-data` — 128K, empty
   - `/mnt/MemoryAlpha/nasops` — 128K, empty
   - `/mnt/src_2tb/` and `/mnt/src_4tb/` — entirely empty

5. **Open WebUI Storage Bloat**
   - `ix-apps/app_mounts/open-webui/` is 20.9G
   - Unclear: is this model data, conversation history, or both?
   - Not organized for RAG or Tier 3 memory ingestion

6. **Nisaba Not Integrated**
   - 310M stored separately from other Concierge infrastructure
   - Should be part of a unified `concierge/` tree once kb/artifacts consolidate

7. **TrueNAS App Infrastructure**
   - 50.2G in `ix-apps/` is necessary system overhead
   - But not clearly partitioned from user/app data
   - Docker image layer storage (26G) commingled with app mounts

### 2.2 Future Readiness Gaps

1. **No dedicated KB/RAG storage**
   - Need: `concierge-kb/` dataset for RAG corpus, Tier 3 memory, artifact index
   - Open WebUI will need filesystem access to this for custom functions

2. **No Nextcloud "External Storage"**
   - Nextcloud can mount datasets as external storage for UI access
   - Currently all data is direct filesystem mounts, no UI window

3. **No artifact handoff path**
   - Bit on Logos will generate artifacts → where do they land?
   - Need canonical path for artifact storage that Nextcloud and Open WebUI both see

4. **Snapshot strategy unclear**
   - Bobby has 500 snapshots; are these intentional backups or automatic overflow?
   - Need explicit retention policy before any migration

---

## Section 3: Proposed Canonical Structure

### 3.1 High-Level Organization

```
MemoryAlpha/
├── system/                    [TrueNAS system, read-only]
├── concierge/                 [NEW] Concierge AI infrastructure
│   ├── kb/                    [NEW] Knowledge base, RAG corpus, Tier 3 memory
│   │   ├── documents/         Documents for RAG ingestion
│   │   ├── vectors/           Vector embeddings / FAISS index (from Open WebUI vector_db)
│   │   ├── artifacts/         Generated artifacts (from Bit, etc.)
│   │   └── index/             Metadata index for fast lookup
│   ├── models/                [NEW] Local model weights, cache
│   │   ├── ollama/            Ollama model cache (from Open WebUI)
│   │   └── weights/           Other local model checkpoints (FernflowerAI, etc.)
│   └── working/               [NEW] Logs, temp, session data
│       ├── logs/              Application logs (Langfuse, OTel spans)
│       ├── temp/              Ephemeral working directory
│       └── sessions/          Session state, conversation history
├── services/                  [NEW] App-specific storage
│   ├── nextcloud/             Nextcloud consolidated
│   │   ├── html/              App code (from ix-apps, copy or bind)
│   │   ├── config/            Nextcloud config
│   │   ├── database/          PostgreSQL data
│   │   └── data/              User file storage
│   │       ├── bobby/
│   │       └── masqued/
│   ├── forgejo/               Forgejo consolidated
│   │   ├── config/
│   │   ├── repos/
│   │   └── database/
│   ├── open-webui/            Open WebUI consolidated
│   │   ├── data/              Conversation history (webui.db only; 65K)
│   │   └── models/            Symlink to concierge/models for model cache
│   ├── nisaba/                Game tracker app
│   │   └── data/              Game inventory, wishlist data
│   └── minecraft/             Game server
│       └── data/              Server state and player data
├── nas/                       [MOVED] User/personal NAS shares
│   ├── Software/              [FROM MemoryAlpha/Software]
│   ├── Video/                 [FROM MemoryAlpha/Video]
│   ├── documents/             General documents
│   └── bobby/                 [FROM MemoryAlpha/bobby] User home dir
├── backups/                   [NEW] Snapshot/backup staging
│   └── [snapshots stored here if needed]
└── [DEPRECATED - to remove]
    ├── dez/
    ├── nasops/
    ├── nextcloud/             [MOVE TO services/nextcloud/data]
    ├── nextcloud-data/        [TO DELETE - empty]
    ├── nextcloud-db/          [MOVE TO services/nextcloud/database]
    ├── nextcloud-users/       [MOVE TO services/nextcloud/data]
    ├── nisaba/                [MOVE TO services/nisaba/data]
    ├── minecraft/             [MOVE TO services/minecraft/data]
    └── ix-apps/               [Keep minimal; separate below]

MemoryAlpha/ix-apps/          [TrueNAS infrastructure - KEEP MINIMAL]
├── app_mounts/                [Gradually migrate app data out]
│   ├── nextcloud/             [→ services/nextcloud/html]
│   ├── open-webui/            [→ services/open-webui + concierge/models]
│   ├── forgejo/               [→ services/forgejo]
│   ├── nisaba/                [→ services/nisaba]
│   ├── minecraft/             [→ services/minecraft]
│   └── [other ix-apps tools]
├── docker/                    [Docker image storage, system]
└── truenas_catalog/           [TrueNAS system]
```

### 3.2 Rationale for New Structure

| Zone | Purpose | Examples |
|------|---------|----------|
| **concierge/** | Concierge-exclusive infrastructure | RAG, Tier 3 memory, artifacts, models, working state |
| **services/** | Self-contained app storage | Each app in its own subtree with all dependencies |
| **nas/** | Traditional NAS shares | User files, documents, media (standard share structure) |
| **system/** | TrueNAS system (read-only) | Keep as-is |
| **ix-apps/** | TrueNAS app infrastructure | Minimize; gradually migrate app data to services/ |

### 3.3 Key Design Decisions

**Decision 1: Consolidate Nextcloud**
- Rationale: 4 scattered datasets → 1 services/nextcloud tree
- Benefit: Unified backup, clearer app boundary, easier migration
- Implementation: Create services/nextcloud/data subtree with bobby/ and masqued/ child datasets (for per-user quotas)

**Decision 2: Move Open WebUI to services/**
- Current: Spread across ix-apps/app_mounts/open-webui and ix-apps/app_mounts/open-webui/ollama
- New: services/open-webui/{data, models} with symlink to concierge/models/ollama for shared cache
- Benefit: Clear separation; future custom functions can access concierge/kb directly

**Decision 3: Separate concierge/kb from Open WebUI**
- RAG corpus, Tier 3 memory index, and artifacts are **Concierge-exclusive** infrastructure
- Open WebUI is a **tool** that can query concierge/kb but doesn't own it
- Benefit: RAG/memory remain stable even if Open WebUI is rebuilt or replaced

**Decision 4: Keep ix-apps minimal**
- Don't delete ix-apps; TrueNAS needs it for app management
- Gradually move app **data** to services/; leave app **code** if necessary for TrueNAS to manage
- Alternative: Full app uninstall → reinstall after migration (higher risk)

**Decision 5: Create nas/ for traditional shares**
- Separates personal/user files from infrastructure
- Future NFS/SMB shares can be carved from nas/
- Nextcloud External Storage mounts can target nas/ for collaborative folders

**Decision 6: Snapshot strategy**
- Delete old snapshots on bobby (cull back to last 30 days as cleanup)
- Define retention policy for new datasets (e.g., keep 7 daily + 4 weekly for critical data)
- Snapshots stay on source dataset; don't create separate backup dataset yet

---

## Section 4: Migration Plan

### 4.1 Phase 0: Pre-Migration (Preparation)

**Goal:** Snapshot current state and prepare tools.

**Tasks:**
1. Create snapshots of critical datasets (bobby, Software, Video, forgejo, nisaba)
   ```bash
   zfs snapshot -r MemoryAlpha/bobby@pre-consolidation-2026-04-13
   zfs snapshot MemoryAlpha/Software@pre-consolidation-2026-04-13
   zfs snapshot MemoryAlpha/Video@pre-consolidation-2026-04-13
   zfs snapshot MemoryAlpha/forgejo@pre-consolidation-2026-04-13
   zfs snapshot MemoryAlpha/nisaba@pre-consolidation-2026-04-13
   ```

2. Audit bobby snapshots — delete old ones to reduce metadata overhead
   ```bash
   # List snapshots; decide retention (keep last 30 days?)
   zfs list -r -t snapshot MemoryAlpha/bobby | tail -20
   # Then delete old ones manually or via script
   ```

3. Verify all app containers are healthy
   ```bash
   sudo docker ps --filter "status=running"
   ```

4. Review Nextcloud data usage
   ```bash
   du -sh /mnt/MemoryAlpha/nextcloud*
   du -sh /mnt/MemoryAlpha/nextcloud-users/*
   du -sh /mnt/.ix-apps/app_mounts/nextcloud/
   ```

5. Confirm Open WebUI size and composition
   ```bash
   du -sh /mnt/.ix-apps/app_mounts/open-webui/*
   # Is it models, conversation history, or both?
   ```

**Duration:** ~30 min  
**Downtime:** None (read-only audit)

---

### 4.2 Phase 1: Create New Dataset Structure

**Goal:** Create all new datasets without moving data yet.

**Tasks:**
1. Create concierge/ tree
   ```bash
   zfs create MemoryAlpha/concierge
   zfs create MemoryAlpha/concierge/kb
   zfs create MemoryAlpha/concierge/kb/documents
   zfs create MemoryAlpha/concierge/kb/vectors
   zfs create MemoryAlpha/concierge/kb/artifacts
   zfs create MemoryAlpha/concierge/kb/index
   zfs create MemoryAlpha/concierge/models
   zfs create MemoryAlpha/concierge/models/ollama
   zfs create MemoryAlpha/concierge/working
   zfs create MemoryAlpha/concierge/working/logs
   zfs create MemoryAlpha/concierge/working/temp
   zfs create MemoryAlpha/concierge/working/sessions
   ```

2. Create services/ tree
   ```bash
   zfs create MemoryAlpha/services
   zfs create MemoryAlpha/services/nextcloud
   zfs create MemoryAlpha/services/nextcloud/html
   zfs create MemoryAlpha/services/nextcloud/config
   zfs create MemoryAlpha/services/nextcloud/database
   zfs create MemoryAlpha/services/nextcloud/data
   zfs create MemoryAlpha/services/nextcloud/data/bobby    # for quota isolation
   zfs create MemoryAlpha/services/nextcloud/data/masqued
   zfs create MemoryAlpha/services/forgejo
   zfs create MemoryAlpha/services/forgejo/config
   zfs create MemoryAlpha/services/forgejo/repos
   zfs create MemoryAlpha/services/forgejo/database
   zfs create MemoryAlpha/services/open-webui
   zfs create MemoryAlpha/services/open-webui/data
   zfs create MemoryAlpha/services/open-webui/models
   zfs create MemoryAlpha/services/nisaba
   zfs create MemoryAlpha/services/nisaba/data
   zfs create MemoryAlpha/services/minecraft
   zfs create MemoryAlpha/services/minecraft/data
   ```

3. Create nas/ tree
   ```bash
   zfs create MemoryAlpha/nas
   zfs create MemoryAlpha/nas/Software
   zfs create MemoryAlpha/nas/Video
   zfs create MemoryAlpha/nas/documents
   zfs create MemoryAlpha/nas/bobby
   ```

4. Create backups/ tree (for future use)
   ```bash
   zfs create MemoryAlpha/backups
   ```

**Duration:** ~5 min  
**Downtime:** None (no data moved)

---

### 4.3 Phase 2: Data Migration (Per-App, Stop App Briefly)

**Goal:** Migrate app data while maintaining integrity. Each app stops → data moves → app restarts.

#### 4.3.1 Nextcloud Migration

**Downtime:** ~10–15 min per component

**Process:**
1. Stop Nextcloud app (TrueNAS UI or docker stop)
2. Copy app code
   ```bash
   cp -r /mnt/.ix-apps/app_mounts/nextcloud/html/* /mnt/MemoryAlpha/services/nextcloud/html/
   ```
3. Copy config (if any exists in app mounts; else skip)
   ```bash
   cp -r /mnt/.ix-apps/app_mounts/nextcloud/config/* /mnt/MemoryAlpha/services/nextcloud/config/ 2>/dev/null || echo "No config to copy"
   ```
4. Copy/move user data
   ```bash
   # Move (don't copy) to avoid double-storage
   zfs send MemoryAlpha/nextcloud@pre-consolidation-2026-04-13 | zfs recv MemoryAlpha/services/nextcloud/data/archive-old-nc
   # Then copy actively-used data
   rsync -av /mnt/MemoryAlpha/nextcloud/ /mnt/MemoryAlpha/services/nextcloud/data/
   ```
5. Move database (if using separate DB dataset)
   ```bash
   zfs send MemoryAlpha/nextcloud-db@pre-consolidation-2026-04-13 | zfs recv MemoryAlpha/services/nextcloud/database/old
   rsync -av /mnt/MemoryAlpha/nextcloud-db/ /mnt/MemoryAlpha/services/nextcloud/database/
   ```
6. Move user-specific data
   ```bash
   zfs send MemoryAlpha/nextcloud-users/bobby@pre-consolidation-2026-04-13 | zfs recv MemoryAlpha/services/nextcloud/data/bobby/archive-old
   rsync -av /mnt/MemoryAlpha/nextcloud-users/bobby/ /mnt/MemoryAlpha/services/nextcloud/data/bobby/
   # Repeat for masqued
   ```
7. Update Nextcloud app mount points in TrueNAS to point to new locations
8. Restart Nextcloud
9. Verify app is healthy and data is accessible
10. Once verified, remove old datasets (keep snapshots):
    ```bash
    zfs destroy MemoryAlpha/nextcloud
    zfs destroy MemoryAlpha/nextcloud-db
    zfs destroy MemoryAlpha/nextcloud-users
    # (snapshots are retained until explicitly deleted)
    ```

#### 4.3.2 Forgejo Migration

**Downtime:** ~5 min

**Process:**
1. Stop Forgejo
2. Move config, repos, database to services/forgejo/* (same pattern as Nextcloud)
3. Update mount points in TrueNAS
4. Restart Forgejo
5. Verify; clean up old datasets

#### 4.3.3 Open WebUI Migration

**Downtime:** ~5 min

**Process:**
1. Stop Open WebUI
2. Separate data by type:
   - Move **model file** (FernflowerAI-35B) from `ix-apps/app_mounts/open-webui/data/uploads/` → `concierge/models/weights/`
   - Move **model cache** from `ix-apps/app_mounts/open-webui/data/cache/` → `concierge/models/cache/`
   - Move **vector_db** from `ix-apps/app_mounts/open-webui/data/vector_db/` → `concierge/kb/vectors/`
   - Move **conversation history** (webui.db) from `ix-apps/app_mounts/open-webui/data/` → `services/open-webui/data/`
3. Create symlink for backward compatibility:
   ```bash
   ln -s /mnt/MemoryAlpha/concierge/models /mnt/MemoryAlpha/services/open-webui/models
   ```
4. Update mount points in TrueNAS to point to new locations
5. Restart Open WebUI
6. Verify app is healthy, models load, conversation history accessible
7. Clean up old datasets once verified

#### 4.3.4 Nisaba Migration

**Downtime:** ~2 min

**Process:**
1. Stop Nisaba container
2. Snapshot current state
   ```bash
   zfs snapshot MemoryAlpha/nisaba@pre-consolidation-2026-04-13
   ```
3. Move data to services/nisaba/data
   ```bash
   rsync -av /mnt/MemoryAlpha/nisaba/data/ /mnt/MemoryAlpha/services/nisaba/data/
   ```
4. Update Nisaba Docker mount point
5. Restart Nisaba
6. Verify game tracker data accessible
7. Destroy old dataset once verified

#### 4.3.5 Minecraft Migration

**Downtime:** ~2 min

**Process:**
1. Stop Minecraft server
2. Snapshot current state
   ```bash
   zfs snapshot MemoryAlpha/minecraft@pre-consolidation-2026-04-13
   ```
3. Move data to services/minecraft/data
   ```bash
   rsync -av /mnt/MemoryAlpha/minecraft/data/ /mnt/MemoryAlpha/services/minecraft/data/
   ```
4. Update Minecraft app mount point in TrueNAS
5. Restart Minecraft
6. Verify server is healthy and world data intact
7. Destroy old dataset once verified

#### 4.3.6 User Data Migration (Software, Video, bobby)

**Downtime:** None (data can be rsync'd while apps running)

**Process:**
1. Snapshot current state
2. Rsync to nas/ tree:
   ```bash
   rsync -av /mnt/MemoryAlpha/Software/ /mnt/MemoryAlpha/nas/Software/
   rsync -av /mnt/MemoryAlpha/Video/ /mnt/MemoryAlpha/nas/Video/
   rsync -av /mnt/MemoryAlpha/bobby/ /mnt/MemoryAlpha/nas/bobby/
   ```
3. Verify data integrity (checksums or spot-checks)
4. Once verified, optionally keep old datasets as read-only or archive (via snapshot)
5. Update any paths in Nextcloud that reference old mounts

#### 4.3.7 Bobby Dataset Snapshot Cleanup

**Downtime:** None

**Process:**
1. Review current snapshots
   ```bash
   zfs list -r -t snapshot MemoryAlpha/bobby | wc -l
   ```
2. Delete snapshots older than 7 days
   ```bash
   # Manual approach: identify oldest to keep, delete rest
   zfs destroy -r MemoryAlpha/bobby@auto-2026-04-06_00-00  # example
   # Or use a script to automate
   ```
3. Monitor metadata reduction
   ```bash
   zfs list MemoryAlpha/bobby
   ```

---

### 4.4 Phase 3: Validation & Cleanup

**Goal:** Confirm all apps work and clean up deprecated datasets.

**Tasks:**
1. Test all apps end-to-end
   - Nextcloud: upload/download files, verify user shares visible
   - Forgejo: clone a repo, create issue, verify access
   - Open WebUI: run a query, verify models load, check conversation history
   - Nisaba: verify game tracker data loads, add/modify inventory
   - Minecraft: verify server starts, world data intact, players can log in

2. Verify NAS shares accessible
   - Check Nextcloud External Storage can mount nas/documents, nas/Software
   - Test SMB/NFS if enabling (future)

3. Verify model/vector storage
   - Confirm Open WebUI can access `concierge/models/weights/` for model file
   - Confirm RAG vector_db in `concierge/kb/vectors/` is readable

4. Backup verification
   - Confirm snapshots are present and valid
   - Test a snapshot restore on a non-critical dataset

5. Clean up old datasets
   ```bash
   zfs destroy MemoryAlpha/nextcloud
   zfs destroy MemoryAlpha/nextcloud-users
   zfs destroy MemoryAlpha/nextcloud-db
   zfs destroy MemoryAlpha/nisaba
   zfs destroy MemoryAlpha/minecraft
   zfs destroy MemoryAlpha/dez         # (if unused)
   zfs destroy MemoryAlpha/nasops      # (if unused)
   zfs destroy MemoryAlpha/nextcloud-data  # (if empty)
   ```

6. Monitor space reclaimed
   ```bash
   zfs list -o name,used,avail
   ```

**Duration:** ~30 min  
**Downtime:** Minimal; spot checks during app restarts only

---

### 4.5 Phase 4: Future Handoff to Open WebUI/Nextcloud Setup

**Goal:** Prepare filesystem for RAG/Tier 3 memory integration.

**Tasks (Do Not Execute Now):**
1. Mount concierge/kb datasets to Open WebUI container
2. Configure Nextcloud External Storage mappings
3. Create custom Open WebUI functions for RAG/artifact access
4. Test end-to-end: ingest → search → generate → save

**Timing:** Next session, once filesystem is stable.

---

## Section 5: Estimated Timeline & Downtime

| Phase | Task | Duration | Downtime |
|-------|------|----------|----------|
| 0 | Pre-migration prep | 30 min | None |
| 1 | Create new datasets | 5 min | None |
| 2a | Nextcloud migration | 15 min | 10–15 min |
| 2b | Forgejo migration | 5 min | 5 min |
| 2c | Open WebUI migration (split: models → concierge, history → services) | 10 min | 5 min |
| 2d | Nisaba migration | 5 min | 2 min |
| 2e | Minecraft migration | 5 min | 2 min |
| 2f | User data migration | 60–120 min | None |
| 2g | Bobby dataset snapshot cleanup | 10 min | None |
| 3 | Validation & cleanup | 30 min | Minimal |
| **Total** | | **2.5–3.5 hours** | **~30 min aggregate** |

**Note:** Phases can run in parallel where possible (e.g., user data migration doesn't block app migrations).

---

## Section 6: Rollback Strategy

**If something breaks:**

1. **Before data deletion:** Snapshots are saved as `@pre-consolidation-2026-04-13`
   ```bash
   zfs rollback MemoryAlpha/bobby@pre-consolidation-2026-04-13
   zfs rollback MemoryAlpha/nextcloud@pre-consolidation-2026-04-13
   # etc.
   ```

2. **App-level recovery:** If app data is corrupted after migration, restore from snapshot
   ```bash
   # Option A: rollback the new dataset
   zfs rollback MemoryAlpha/services/nextcloud/data@snapshot-during-migration
   
   # Option B: restore from old dataset if kept
   rsync -av /mnt/MemoryAlpha/nextcloud-archive/ /mnt/MemoryAlpha/services/nextcloud/data/
   ```

3. **Full rollback:** If consolidated structure isn't working, keep old datasets mounted alongside and revert app configs

**Risk Mitigation:**
- Keep pre-consolidation snapshots for 30 days minimum
- Run validation tests before deleting old datasets
- Document exact mount point changes before executing

---

## Section 7: Decisions Needed Before Execution

| Decision | Options | Recommendation | **Bobby's Decision** |
|----------|---------|-----------------|------------------|
| **Keep old datasets as archives?** | A) Delete immediately after migration | B) Keep for 30 days as backup | C) Keep indefinitely | B | **✅ B** |
| **Bobby snapshot cleanup** | A) Keep all 500+ snapshots | B) Cull to last 7 days | C) Cull to last 30 days | C | **✅ B** (cull to 7 days) |
| **Nisaba integration** | A) Keep as separate dataset | B) Move to concierge/ | C) Move to services/ | TBD | **✅ C** (Move to services/) |
| **Minecraft dataset** | A) Move to services/ | B) Leave in place | C) Delete | A | **✅ A** (Move to services/minecraft) |
| **NAS shares (SMB/NFS)** | A) Enable now for nas/ datasets | B) Enable after consolidation | C) Not yet (plan for later) | C | **✅ C** (Decide later) |
| **Nextcloud data per-user quotas** | A) Use dataset quotas on bobby/masqued child datasets | B) Use Nextcloud app quotas | C) No quotas yet | A | **✅ Are quotas needed for personal files?** (Deferred) |
| **Execution timing** | A) Execute immediately | B) Plan for specific date/time | C) Wait for other decisions | B | **✅ B** (Schedule when time available) |

---

## Section 8: Success Criteria

By end of migration session, all of these should be **✅ Yes**:

- [ ] All new datasets created and mounted
- [ ] Nextcloud app runs from services/nextcloud with all user data accessible
- [ ] Forgejo app runs from services/forgejo with all repos accessible
- [ ] Open WebUI runs from services/open-webui with models loading
- [ ] User data (Software, Video, bobby) accessible in nas/ tree
- [ ] All app containers healthy and passing health checks
- [ ] Space calculation: total used < 6TB (consolidated layout is efficient)
- [ ] Pre-consolidation snapshots retained (rollback available)
- [ ] Old datasets destroyed (MemoryAlpha utilization cleaner)
- [ ] Documentation updated with new mount paths
- [ ] Ready for next session: Open WebUI + Nextcloud integration for RAG/artifacts

---

## Section 9: Notes & Contingencies

### 9.1 Open WebUI Model Storage
**Q:** Is the 20.9G in open-webui/ actual model weights, or conversation history + cached embeddings?

**A:** ✅ **Confirmed breakdown:**
- **21G:** `uploads/FernflowerAI-35B-A3B-KL-ReLU.Q4_K_L.gguf` — **model weight file**
- **890M:** `cache/` — model inference cache
- **28K:** `vector_db/` — vector embeddings for RAG
- **65K:** `webui.db` — SQLite conversation history

**Decision:** Move model file (21G) + cache (890M) to `concierge/models/` (shared across tools). Keep conversation history (webui.db) in `services/open-webui/data/`. Vector DB goes to `concierge/kb/vectors/` for RAG integration.

### 9.2 Nisaba Data Ownership
**Q:** Is Nisaba data (310M) ephemeral working state, or critical infrastructure?

**A:** ✅ **Confirmed:** Nisaba is a **digital video game tracker** (inventory, wishlist system) — custom Docker app built with Claude Code. Data is persistent user content, not ephemeral.

**Decision:** Move to `services/nisaba/` alongside other apps. Not Concierge-specific infrastructure; it's a standalone service app.

### 9.3 Minecraft Dataset
Currently at 2.56G in `/mnt/MemoryAlpha/minecraft/data`. 

**Decision:** Move to `services/minecraft/data` alongside other apps.

### 9.4 Nextcloud External Storage Setup
Once consolidation is done, Nextcloud can be configured to mount:
- `nas/Software/` as "Cloud Storage"
- `nas/documents/` as "Shared Docs"
- `nas/bobby/` as "Home"

This is a **post-consolidation task** (next session).

---

## Appendix A: Quick Reference — New Mount Points

After consolidation, app mount points will be:

```
Nextcloud:
  ├── App code:      /mnt/MemoryAlpha/services/nextcloud/html
  ├── Config:        /mnt/MemoryAlpha/services/nextcloud/config
  ├── DB:            /mnt/MemoryAlpha/services/nextcloud/database
  ├── User data:     /mnt/MemoryAlpha/services/nextcloud/data/
  │   ├── bobby:     /mnt/MemoryAlpha/services/nextcloud/data/bobby/
  │   └── masqued:   /mnt/MemoryAlpha/services/nextcloud/data/masqued/

Forgejo:
  ├── Config:        /mnt/MemoryAlpha/services/forgejo/config
  ├── Repos:         /mnt/MemoryAlpha/services/forgejo/repos
  └── DB:            /mnt/MemoryAlpha/services/forgejo/database

Open WebUI:
  ├── Conversation history: /mnt/MemoryAlpha/services/open-webui/data/webui.db
  ├── Models (symlink):     /mnt/MemoryAlpha/services/open-webui/models → concierge/models
  └── Vector DB:            /mnt/MemoryAlpha/concierge/kb/vectors/

Nisaba (Game Tracker):
  └── Data:          /mnt/MemoryAlpha/services/nisaba/data

Minecraft:
  └── Data:          /mnt/MemoryAlpha/services/minecraft/data

Concierge:
  ├── KB corpus:     /mnt/MemoryAlpha/concierge/kb/documents/
  ├── Vectors:       /mnt/MemoryAlpha/concierge/kb/vectors/
  ├── Artifacts:     /mnt/MemoryAlpha/concierge/kb/artifacts/
  ├── Model weights: /mnt/MemoryAlpha/concierge/models/weights/
  ├── Model cache:   /mnt/MemoryAlpha/concierge/models/cache/
  ├── Ollama cache:  /mnt/MemoryAlpha/concierge/models/ollama/
  └── Logs:          /mnt/MemoryAlpha/concierge/working/logs/

User NAS:
  ├── Software:      /mnt/MemoryAlpha/nas/Software/
  ├── Video:         /mnt/MemoryAlpha/nas/Video/
  ├── Documents:     /mnt/MemoryAlpha/nas/documents/
  └── Bobby:         /mnt/MemoryAlpha/nas/bobby/
```

---

## Appendix B: Commands Cheat Sheet

**Snapshot all datasets:**
```bash
zfs snapshot -r MemoryAlpha@pre-consolidation-2026-04-13
```

**List datasets with usage:**
```bash
zfs list -o name,used,avail,mountpoint MemoryAlpha
```

**Create a dataset:**
```bash
zfs create MemoryAlpha/concierge/kb/documents
```

**Destroy a dataset:**
```bash
zfs destroy MemoryAlpha/nextcloud
```

**Rsync directory (preserve permissions):**
```bash
rsync -av /source/ /dest/
```

**Check app health:**
```bash
sudo docker ps
```

**Stop/start app:**
```bash
sudo docker stop ix-nextcloud-nextcloud-1
sudo docker start ix-nextcloud-nextcloud-1
```

---

**Status:** ✏️ Ready for Bobby's review and decision on Section 7 items.  
**Next Step:** Confirm decisions in Section 7, then execute Phase 0 & 1 (non-breaking setup).
