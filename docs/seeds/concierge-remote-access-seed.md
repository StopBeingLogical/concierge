---
title: "Concierge — Remote Access Setup Seed"
document_type: seed
version: "1.0"
date: "2026-04-12"
status: reference
tags: ['tailscale', 'homarr', 'remote-access', 'infrastructure']
---

# CONCIERGE — Remote Access Setup Seed
**Version:** 1.0 — April 12, 2026
**Purpose:** Handoff seed for dedicated remote access configuration session
**Context:** Pre-Bit scaffold planning — establishing single entry point for homelab services via Tailscale VPN + Homarr dashboard

---

## Session Objective

Configure remote access infrastructure for Concierge homelab:
1. **Tailscale mesh VPN** on Atlas and Logos (and any other nodes that need remote access)
2. **Homarr dashboard** on Atlas (port 7575) as the single entry point
3. **Open WebUI** on Atlas (port 3000) as the LLM interface, pointing to remote Ollama instances
4. **Ollama** on Kratos and Ergaster (already running, localhost:11434)

**End state:** Connect to Tailscale from anywhere → browser to `atlas.100.x.x.x:7575` → dashboard with links to all services (Open WebUI, Nextcloud, Forgejo, TrueNAS, etc.)

---

## Fleet Summary

| Node | Role | Specs | Service Role |
|---|---|---|---|
| **Atlas** | Storage/Services | Ryzen 5700G, 64GB RAM, 3x12TB RaidZ1, TrueNAS SCALE | Portal host (Homarr, Open WebUI, Tailscale node) |
| **Logos** | Workstation | M1 Max (10/24), 64GB RAM | Tailscale client |
| **Kratos** | Inference | Ryzen 7600X, RX 7800 XT (16GB), 32GB RAM | Ollama (localhost:11434, ROCm) |
| **Ergaster** | Control Plane | i9-13900HX, 64GB RAM | Ollama (localhost:11434, CPU) — TBD |
| **Daemon** | Inference | i7-12700F, 32GB, 2x P100, 1x 5060 Ti | Not needed for scaffold |

---

## Current Services on Atlas

| Service | Access | Status |
|---|---|---|
| TrueNAS UI | Local only | Running |
| Nextcloud | nextcloud.damnaliens.us (Cloudflare tunnel) | Running |
| Forgejo | forgejo.damnaliens.us (Cloudflare tunnel) | Running |
| Nisaba | Docker (internal) | Running |

---

## Setup Tasks (In Order)

### Phase 1: Tailscale VPN Setup
- [ ] Install Tailscale on Atlas
- [ ] Authenticate Atlas to Tailscale account
- [ ] Get Tailscale IP for Atlas (format: 100.x.x.x)
- [ ] Install Tailscale on Logos (Mac)
- [ ] Authenticate Logos to Tailscale
- [ ] Test connectivity: ping atlas.100.x.x.x from Logos
- [ ] Verify all services accessible via Tailscale IP (TrueNAS at atlas:6000, etc.)

### Phase 2: Homarr Dashboard
- [ ] Install Homarr Docker container on Atlas (port 7575)
- [ ] Configure Homarr to display tiles/links for:
  - Open WebUI (atlas:3000)
  - Nextcloud (atlas or nextcloud.damnaliens.us)
  - Forgejo (atlas or forgejo.damnaliens.us)
  - TrueNAS UI (atlas:6000)
  - SSH access points (Kratos, Ergaster, Logos)
- [ ] Test dashboard accessibility: http://atlas.100.x.x.x:7575
- [ ] Verify all tiles/links work

### Phase 3: Open WebUI Setup
- [ ] Install Open WebUI Docker container on Atlas (port 3000)
- [ ] Configure Open WebUI to point to Kratos Ollama (http://kratos.100.x.x.x:11434 or kratos.local:11434)
- [ ] Enable Open WebUI auth (WEBUI_AUTH=True)
- [ ] Pull at least one model on Kratos (test model)
- [ ] Test Open WebUI chat interface: http://atlas.100.x.x.x:3000
- [ ] Verify model dropdown shows available models
- [ ] Test model switching (if Ergaster Ollama is also set up)

### Phase 4: Optional — Ergaster Ollama
- [ ] Install Ollama on Ergaster (if not already running)
- [ ] Configure Ergaster Ollama (localhost:11434)
- [ ] Pull at least one model on Ergaster
- [ ] In Open WebUI settings, test switching OLLAMA_BASE_URL to point to Ergaster
- [ ] Verify models from both nodes are accessible

### Phase 5: Network Hardening (Optional but Recommended)
- [ ] Ensure Atlas services only listen on Tailscale IP or localhost (not 0.0.0.0)
- [ ] Restrict Ollama on Kratos/Ergaster to local network only
- [ ] Verify no services are accidentally exposed to the internet

---

## Key Technical Details

### Tailscale IPs
- Tailscale assigns each node a unique IP in the 100.x.x.x range
- These IPs are stable (persist across reboots)
- Access by IP or hostname (e.g., `atlas.100.x.x.x` or `atlas.local` via Tailscale DNS)

### Homarr Configuration
- Port: 7575 (default)
- Volume mount for persistent config
- Supports iframe embedding of services or simple links
- No complex reverse proxy needed

### Open WebUI + Ollama
- Open WebUI needs network access to Ollama (not necessarily localhost)
- Use Tailscale hostnames or IPs to reach remote Ollama instances
- Model list fetched from OLLAMA_BASE_URL at startup
- Can switch backends via UI settings (no restart needed)

### Docker Compose (Recommended for Atlas)
All Atlas services (Homarr, Open WebUI, existing Nextcloud/Forgejo) should ideally run via docker-compose for easy management and persistence.

---

## Known Constraints

- **Ergaster Ollama:** i9-13900HX has iGPU (framebuffer only, not useful for inference). CPU inference only. Will be slower than Kratos. Useful for testing, not primary inference.
- **Kratos Network:** Must have network path to Atlas. Typically same LAN, should be fine.
- **Model Switching:** Switching between Kratos and Ergaster in Open WebUI requires changing OLLAMA_BASE_URL in settings and reloading models. Not seamless in a single chat.

---

## Not In Scope for This Session

- Bit application (pre-Bit scaffold only)
- Router/Foreman/Workbee (full stack not being built yet)
- Advanced security hardening (basic Tailscale gate is sufficient for MVP)
- Load balancing or failover between Ollama instances
- Model serving optimization (using default Ollama/llama.cpp performance)

---

## Success Criteria

When this session is complete:

1. Tailscale VPN is running on Atlas and Logos
2. You can access http://atlas.100.x.x.x:7575 from Logos browser (via Tailscale)
3. Homarr dashboard displays at that URL with working service links
4. Open WebUI is accessible at atlas:3000 with working model selection
5. You can chat with a model running on Kratos (or Ergaster, if set up)
6. Model switching between nodes works (if both Ollama instances are set up)

---

## References

- `hardware-inventory-v1.1.md` — current fleet specs
- `CONCIERGE_SESSION_SEED.md` — full project context if needed
- Tailscale docs: https://tailscale.com/kb/
- Homarr docs: https://homarr.dev/
- Open WebUI docs: https://docs.openwebui.com/

---

*Handoff seed created April 12, 2026 during pre-Bit scaffold planning session. Load this at the start of the remote access configuration session. No prior knowledge of Concierge architecture needed — this is pure infrastructure setup.*
