---
title: "Seed — Antigravity & OpenCode Integration Options"
document_type: seed
version: "1.0"
date: "2026-04"
status: current
tags: ['antigravity', 'opencode', 'routing', 'frontier', 'local-swarm']
---

# SEED: Antigravity & OpenCode Integration Options
**Version:** 1.0 — April 2026  
**Status:** Strategic Reference for Concierge/Bit  
**Focus:** Hybrid Routing (Frontier Planning + Local Execution Swarm)

## 1. The Core Integration: "Scalpel vs. Hammer"
This configuration utilizes Antigravity as the high-level reasoning interface (the Scalpel) and OpenCode as the local task executor (the Hammer).

* **Antigravity (The Architect)**: A fork of VS Code OSS (Version 1.107.0) that provides "Mission Control" for managing autonomous agents. It handles repository indexing, visual verification via an embedded browser, and high-level strategic planning using Gemini 3.1 Pro and Claude 4.6.
* **OpenCode (The Builder)**: A terminal-based agent that runs inside the Antigravity workspace. It acts as the bridge to over 75 providers, including your local hardware nodes.

## 2. Authentication & Quota Management
To leverage your Google AI Pro (5 TB) plan without incurring per-token API costs, you can tunnel your subscription into the terminal.

* **Antigravity OAuth Plugin**: Authenticates the OpenCode CLI using your Google account.
* **Benefit**: This allows OpenCode to tap into your 5-hour rolling Antigravity quota and 1,000 monthly AI credits directly from the terminal.
* **Command**: `opencode auth login` -> Select **OAuth with Google (Antigravity)**.

## 3. Local Swarm Routing (Distributed Nodes)
Route to your 5-node swarm (Kratos, Daemon, and the 16GB independent nodes) through OpenCode.

### A. The Gateway: LiteLLM Proxy
Run LiteLLM on a central node (Logos or Atlas) as a unified OpenAI-compatible endpoint.
* **Safe Versioning**: Use version **1.82.6** or earlier to avoid known supply chain compromises.
* **Routing**: LiteLLM collects endpoints from all 5 nodes and presents them to OpenCode as a single provider.

### B. OpenCode Configuration (opencode.jsonc)
```json
{
  "provider": {
    "local-swarm": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://<PROXY-IP>:4000/v1" },
      "models": {
        "workbee-1": {},
        "workbee-2": {},
        "auditor-node": {}
      }
    }
  }
}
```

## 4. Recommended 2026 Workflow
1.  **Plan (Frontier)**: Use Claude 4.6 or Gemini 3.1 Pro in Antigravity to architect the solution and generate a TASK.md contract.
2.  **Verify (Local)**: Open the terminal and run: `open code run "Execute TASK.md using workbee-1"`.
3.  **Audit (Swarm)**: Switch to your auditor-node to perform a neutral code review of the generated work.
4.  **Final Polish**: Use Antigravity's Agent Manager to visually verify changes in the embedded browser.

---
*Created April 2026. Add to Concierge Project Store.*
