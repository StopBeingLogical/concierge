---
title: "Homelab Hardware Inventory"
document_type: reference
version: "1.1"
date: "2026-04-12"
status: current
tags: ['hardware', 'fleet', 'inventory', 'homelab']
---

# Homelab Hardware Inventory — v1.1
**Status:** Canonical Hardware State
**Updated:** April 12, 2026

---

## 1. Active Fleet

| Name | Role | Specs | Notes |
| :--- | :--- | :--- | :--- |
| **Logos** | Primary Workstation | MacBook Pro M1 Max (10-core CPU / 24-core GPU), 64GB RAM | Human interaction layer, MVP validation target |
| **Atlas** | Storage/Services | Ryzen 5700G, 64GB RAM, 3x12TB RaidZ1, TrueNAS SCALE | Runs Nextcloud, Nisaba, Forgejo; Cloudflare tunnel endpoints |
| **Daemon** | Headless CUDA Inference | i7-12700F, 32GB RAM, 2x Tesla P100, 1x RTX 5060 Ti | Three heterogeneous GPU islands; burst mode capable |
| **Ergaster** | Control Plane (Router/Foreman) | Acemagic M1 (i9-13900HX), 64GB RAM | 24 cores / 32 threads; iGPU framebuffer only |
| **Kratos** | Mid-Tier Inference | Ryzen 7600X, RX 7800 XT (16GB), 32GB DDR5 6000 RAM | ROCm backend; quorum voice for 7B-13B inference |

---

## 2. Candidate / On-Bench

| Name | Status | Specs | Notes |
| :--- | :--- | :--- | :--- |
| **Noesis** | Active (Dev Laptop) | Dell Latitude 7420 (i7-1185G7, 32GB LPDDR4x, Xe iGPU) | Promoted from bench to development use |
| **Ephemera** | Bench | MacBook Air M2 (8GB unified memory) | Sitting under desk; available for deployment |
| **Praxis** | Gaming-Only | Steam Deck | Out of scope for Concierge |
| **Gramma** | Out of Scope | iPad Air (M3) | Note-taking device |

---

## 3. Fleet Topology Summary

**Compute Tiers:**
- **Tier 1 (Inference):** Daemon (dGPU verifier + burst capacity), Kratos (iGPU quorum), Ergaster iGPU (when idle)
- **Tier 2 (Background):** Noesis (Pathfinder-class via Xe + OpenVINO), Ephemera (ANE-based when deployed)
- **Tier 3 (Control Plane):** Ergaster (primary Router/Foreman host)
- **Tier 4 (Storage/Portal):** Atlas (TrueNAS + Docker services)
- **Tier 5 (Human Surface):** Logos (Bit application, disconnected-mode fallback)

**Active Quorum (Inference Ensemble):**
- Daemon Island 1 (5060 Ti): ~1 voice
- Daemon Island 2 (P100 #1): ~1 voice
- Daemon Island 3 (P100 #2): ~1 voice
- Kratos (RX 7800 XT): ~1 voice
- **Total: 4 quorum voices at baseline; burst mode can shard across all three Daemon islands**

**Network Topology:**
- All nodes on local network; Atlas is canonical storage/NAS
- Cloudflare tunnel for external access (nextcloud.damnaliens.us, forgejo.damnaliens.us)
- Tailscale mesh VPN (planned) for homelab-wide remote access

---

## 4. Service Inventory (Current)

| Service | Host | Access | Status |
| :--- | :--- | :--- | :--- |
| TrueNAS UI | Atlas | Local / Tailscale | Running |
| Nextcloud | Atlas | nextcloud.damnaliens.us (Cloudflare tunnel) | Running |
| Forgejo | Atlas | forgejo.damnaliens.us (Cloudflare tunnel) | Running |
| Nisaba | Atlas | Docker (internal) | Running |
| Ollama | Kratos | localhost:11434 | Planned for scaffold |
| Ollama | Ergaster | localhost:11434 | Planned for scaffold |
| Open WebUI | Atlas | TBD (Tailscale, Homarr dashboard) | Planned |
| Homarr (Portal) | Atlas | TBD (Tailscale entry point) | Planned |

---

## 5. Changelog

| Date | Version | Changes |
| :--- | :--- | :--- |
| 2026-04-12 | v1.1 | Logos: clarified 24-core GPU (not 32); Noesis: promoted to active dev laptop; added service inventory; added planned scaffold services; added topology summary |
| 2026-02-15 | v1.0 | Inception. Renamed old Praxis to Kratos and updated specs. |

---

## 6. Acquisition Pipeline

**No pending acquisitions.** Current fleet baseline supports Concierge MVP. Future expansion will follow telemetry signals from Router (queue depth, P1 latency, bottleneck identification) rather than speculative hardware purchases.

**Research notes (deferred):**
- Intel Arc Pro B70 (dGPU verifier candidate)
- AMD Radeon AI PRO R9700 (dGPU verifier candidate)
- RDNA2 GPU (secondary card for Ryzen 2600 worker node, opportunistic)

---

*Canonical inventory. Load alongside CONCIERGE_SESSION_SEED.md and Concierge_Hardware_Appendix_v5.md for complete hardware context.*
