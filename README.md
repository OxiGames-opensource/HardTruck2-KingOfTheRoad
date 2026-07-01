# Hard Truck 2: King of the Road Community Compatibility Patch

Open-source compatibility patch and reverse engineering research project for **Hard Truck 2: King of the Road**.

This repository is part of the **OxiGames** ecosystem — an open initiative dedicated to preserving and improving the compatibility of classic and modern PC games on current operating systems and hardware.

For the complete project philosophy and design principles, see **[OxiGames.md](OxiGames.md)**.

---

## Goals

- Improve compatibility with modern Windows and Linux systems
- Fix startup and hardware detection issues
- Preserve original gameplay
- Document compatibility problems and their solutions
- Provide reproducible research and tooling
- Distribute compatibility patches, **not** copyrighted game files

---

## Current Focus

- Modern GPU compatibility
- Texture memory fixes
- Linux / Proton compatibility
- AVI subsystem investigation
- Safe binary patching tools
- Reverse engineering documentation

---

## Legal Notice

This repository **does not contain** any copyrighted assets from the original game.

The following files are **not** distributed:

- game executables
- game DLLs
- movies
- textures
- music
- original archives
- any other copyrighted game resources

A legally obtained copy of **Hard Truck 2: King of the Road** is required.

---

## Development Environment

This repository follows the **OxiFabrics workspace layout**.

The repository root contains the development environment, while the actual project files are stored inside the `app/` directory.

```
app/
docker/
.env.example
.gitignore
OxiGames.md
README.md
```

Each Docker service is stored in its own directory.

Example:

```
docker/
    ghidra/
        Dockerfile
        helper/
```

---

## Ghidra

Ghidra is **not** stored in this repository.

During Docker image build, the required version of Ghidra is downloaded directly from the official NSA GitHub release.

No Ghidra binaries are distributed with this project.

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/OxiGames-opensource/HardTruck2-KingOfTheRoad.git
cd HardTruck2-KingOfTheRoad
```

Create the local environment file:

```bash
cp .env.example .env
```

Build the Ghidra container:

```bash
docker compose build ghidra
```

Start the development environment:

```bash
docker compose run --rm ghidra
```

Inside the container the repository is mounted as:

```
/workspace
```

The project files are located at:

```
/workspace/app
```

---

## Repository Structure

```
app/
    docs/
    ghidra/
        scripts/
    patches/
    research/
    tools/

docker/
    ghidra/
        Dockerfile
        helper/

README.md
OxiGames.md
.env.example
.gitignore
```

---

## Project Status

🚧 **Work in Progress**

Planned public release:

- Windows compatibility patch
- Linux / Proton compatibility guide
- Technical documentation
- Safe binary patcher
- Reverse engineering notes
- Research documentation

---

## Contributing

Bug reports, research notes and pull requests are welcome.

Please ensure that every proposed change is:

- technically documented
- reproducible
- tested
- compatible with legally obtained copies of the game

---

## License

This project is licensed under the **MIT License**.