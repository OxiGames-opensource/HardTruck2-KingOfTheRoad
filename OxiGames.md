# OxiGames
This document defines the common principles shared by all OxiGames repositories.

## Mission

OxiGames is an open-source initiative dedicated to preserving the playability and improving the compatibility of classic and modern PC games on current operating systems and hardware.

The project develops legal compatibility patches, documentation and research intended to keep original games playable for years to come.

---

## Core Principles

### Legal First

OxiGames supports **only legally obtained copies** of games acquired through official distribution platforms such as Steam, GOG, Epic Games Store and other authorized stores.

The project does **not** distribute or support:

- cracks
- key generators
- DRM bypasses
- pirated copies
- copyrighted game assets

Every patch requires the user to own the original game.

---

### Compatibility

The purpose of every project is to improve compatibility with modern environments, including:

- Windows
- Linux
- Proton
- Wine
- Steam Deck
- modern CPUs
- modern GPUs
- modern display resolutions

OxiGames does not change gameplay unless required to restore the original behaviour.

---

### Preservation

The project exists to preserve games, not to redesign them.

Compatibility fixes should restore functionality while keeping the original experience intact whenever possible.

---

### Automation

Every compatibility fix should be reproducible.

Whenever practical, projects should provide automated tools that:

- verify supported executable versions
- detect supported game versions
- create backups
- apply binary patches safely
- allow rollback

---

### Documentation

Every compatibility issue should be documented.

Every discovered solution should be reproducible.

Every technical decision should be documented whenever possible.

Research, documentation and reproducibility are considered as valuable as source code.

---

## Reverse Engineering

Reverse engineering is used exclusively for:

- compatibility research
- understanding legacy software behaviour
- documenting technical limitations
- developing legal compatibility patches

Reverse engineering is used to understand software behaviour, not to replace original software.

The project does not attempt to recreate or redistribute the original game.

---

## Repository Philosophy

Each repository should remain self-contained.

Every repository should be understandable without requiring information from other OxiGames repositories.

Each repository should include:

- documentation
- research
- tooling
- patch sources
- Docker environment (when appropriate)

A repository should **not** include:

- original executables
- original DLLs
- copyrighted assets
- installers
- Steam libraries
- Wine prefixes

---

## Contributions

Contributions are welcome.

Every proposed change should include:

- problem description
- technical explanation
- supported game version(s)
- reproducible validation
- rollback information (when applicable)

---

## Long-Term Vision

OxiGames aims to build an open knowledge base for game compatibility and preservation.

The project values:

- technical accuracy
- reproducibility
- documentation
- long-term maintainability

More than simply fixing individual games, OxiGames aims to preserve the knowledge required to keep them playable on future systems.

---

## Philosophy

OxiGames does not rewrite game history.

It helps game history continue.