# Agent Notes — O Livro do Desassossego

## What is this repo?

This is a public literary / experimental repository under the `portugalfuturista` GitHub
organization. It holds fragments, media assets, and structural notes related to *O Livro
do Desassossego*.

## Infrastructure context

For all Portugal Futurista infrastructure, Proxmox maps, and active cleanup priorities,
see the canonical source of truth:

```
nervura-electrica/AGENTS.md
```

Located at: `/home/fcunha/portugalfuturista/nervura-electrica/AGENTS.md`

## Brain / memory sync

This workspace participates in the **Réplica Omnisciente** brain network:

- **Central brain repo**: `portugalfuturista/replica` (`/home/fcunha/portugalfuturista/replica`)
- **Aurélio brain path**: `replica/.aurelio/brain`
- **Kimi sessions** are imported via `replica/scripts/sync-kimi-to-brain.py`
- **z-ai GLM / Claude Code** are wired into Aurelio's model router and local MCP config (`olivrododesassossego/.aurelio/mcp_config.json`)
- **Push brain to CT 208**: `cd /home/fcunha/portugalfuturista/replica && ./.aurelio/sync.py --push`

## z-ai GLM / Claude Code integration

This repo's local MCP config (`olivrododesassossego/.aurelio/mcp_config.json`) registers the four z-ai MCP servers (`zai-vision`, `zai-web-search`, `zai-web-reader`, `zai-zread`) so Aurelio clients running from this workspace can use them.

API keys are referenced via `${Z_AI_API_KEY}`; set the key in `.env` or export it in your shell before running Aurelio clients.

For the full integration guide — including backend routing, Hermes mode, React / VS Code: / Svelte UIs, deployment, and security notes — see:

```
nervura-electrica/docs/AURELIO_GLM_CLAUDE.md
```

> **Security note**: the literal API key was removed from the git-tracked MCP config. Rotate the key if this repository was ever public.

When working here, refer to `replica/AGENTS.md` for the agent bootstrapping protocol and
`nervura-electrica/AGENTS.md` for live infrastructure state.
