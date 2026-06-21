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
- **Push brain to CT 206**: `cd /home/fcunha/portugalfuturista/replica && ./.aurelio/sync.py --push`

When working here, refer to `replica/AGENTS.md` for the agent bootstrapping protocol and
`nervura-electrica/AGENTS.md` for live infrastructure state.
