# 🧟‍♂️ PZColab — Free Project Zomboid Dedicated Server on Google Colab

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Open In Colab](https://img.shields.io/badge/Open%20In-Colab-orange.svg?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/Andresdotdev/PZColab/blob/main/PZ_Colab_EN.ipynb)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg?logo=python&logoColor=white)]()
[![Project Zomboid](https://img.shields.io/badge/Project%20Zomboid-b41%20%26%20b42-red.svg)]()
![GitHub stars](https://img.shields.io/github/stars/Andresdotdev/PZColab?style=social)

**Read this in: [Español 🇪🇸](README.es.md)**

Run your own **free Project Zomboid dedicated server** in the cloud using **Google Colab** — no VPS, no port forwarding, no credit card. Works with **Build 42 (stable)** and **Build 41 (legacy)**, installs everything automatically with **SteamCMD**, persists your world on **Google Drive**, and exposes the server to your friends through a **Playit.gg tunnel**.

> This is an open-source tool for the community: spin up multiplayer Project Zomboid servers in minutes, free of charge, and stress-test mods, maps and configurations with zero infrastructure cost.

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🎮 Supported Game Versions](#-supported-game-versions)
- [📦 Installing Mods (Easy Mode)](#-installing-mods-easy-mode)
- [🛠️ Server Operations](#️-server-operations)
- [🧠 Log Diagnostics](#-log-diagnostics)
- [❓ FAQ](#-faq)
- [⚠️ Important Notes](#️-important-notes)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

* **One-click deployment:** automatically installs system dependencies, SteamCMD and the Project Zomboid dedicated server.
* **Version selector:** **b42 stable** (recommended), **b41 legacy** and **b42 unstable** — one synchronized choice shared across all cells via a state file on Drive.
* **No port forwarding:** built-in [Playit.gg](https://playit.gg/) tunnel gives your server a public address anyone can join.
* **Cloud persistence:** saves, configs and player profiles live on your Google Drive (`/MyDrive/ZomboidSaves`) — nothing is lost when the Colab session ends.
* **Automatic memory tuning:** patches `-Xms/-Xmx` to 6 GB in `start-server.sh`, matching Colab's ~12.7 GB RAM limit.
* **Easy Workshop mods + collections:** paste a Workshop URL or numeric ID (one per line) — or a whole Steam **collection** — and the notebook downloads each item via SteamCMD, **auto-detects the real Mod ID** from its `mod.info`, classifies them (Libraries / UI / Vehicles / QoL) and writes them to the server `.ini` without duplicates.
* **Crash watchdog:** the server auto-restarts on failure (configurable retry count).
* **Clean shutdown:** sends `save` then `quit` so the world is saved safely.
* **Live console:** a `tail` cell shows the server console in real time.
* **Saves backup:** one-click `.tar.gz` backups on Drive with configurable retention.
* **Advanced log diagnostics:** scans log files and groups Lua errors / Steam Workshop failures per mod, naming the actual culprit.
* **Anti-idle script:** a browser console script that prevents Google Colab from disconnecting your session.

## 🚀 Quick Start

1. Open **`PZ_Colab_EN.ipynb`** in Google Colab (use the badge above or *File → Open notebook → GitHub*).
2. Run **Cell 1** — pick the game version and install the server (mounts Google Drive automatically).
3. Run **Cell 2** — claim your persistent Playit.gg tunnel (first time only).
4. Run **Cell 3** — the server starts in the background. Share the IP/port that Playit assigns!

> 💡 Spanish speakers: use the Spanish version **`PZ_Colab.ipynb`** — [Español 🇪🇸](README.es.md).

## 🎮 Supported Game Versions

| Option | SteamCMD branch | Description |
|---|---|---|
| `b42 stable` | Default (no beta) | Current stable build of Project Zomboid. **Recommended.** |
| `b41 legacy` | `-beta legacy41` | Legacy 41.x build, for servers with older mods. |
| `b42 unstable` | `-beta unstable` | Unstable Build 42 branch, for testing new features. |

The selected version is stored in `MyDrive/ZomboidSaves/.pzcolab_state.json` and reused by every other cell. Re-running **Cell 1** is fast: if the server is already installed with the same version it skips the download; if you switched versions it stops the running server and reinstalls automatically.

## 📦 Installing Mods (Easy Mode)

In **Cell 4**, paste one mod per line — the **Workshop URL** or just the **numeric ID**:

```
https://steamcommunity.com/sharedfiles/filedetails/?id=2902678
2861456062
https://steamcommunity.com/sharedfiles/filedetails/?id=2750177123
```

You can also paste **Steam collection URLs** — they expand automatically. The cell downloads each item with SteamCMD, reads the **real Mod ID** from its `mod.info` (so you never need to know it), classifies them (Libraries → UI → Vehicles → QoL load order) and updates the `.ini` without duplicates, keeping your previous mods. The final report shows the mods' **real names**.

If automatic detection fails for a mod, use the advanced format `URL|ModIDManual` on that line.

## 🛠️ Server Operations

* **Cell 3.1 — Live console:** watch the server output in real time (stop with the ⏹ button).
* **Cell 3.2 — Clean shutdown:** saves the world and shuts the server down safely.
* **Cell 5 — Backup:** creates a `.tar.gz` of your saves in `MyDrive/ZomboidSaves_backups` with retention of the last N copies.
* **Anti-idle (end of notebook):** paste the browser script into the Colab page console (F12) to keep the session alive.

## 🧠 Log Diagnostics

If the server fails to boot or mods misbehave, run **Cell 4.1 — Server Inspector & Advanced Diagnostics**. It analyzes your Drive logs and prints:
- Exact number of critical Lua errors.
- The mod/script responsible for the failure.
- Steam Workshop connection alerts.

## ❓ FAQ

**Is it really free?** Yes — Google Colab's free tier runs the server at no cost (session-limited to ~12 hours). A VPS or dedicated host is not required.

**Does it work with Steam Workshop mods?** Yes. Cell 4 downloads mods via SteamCMD and writes them to the server configuration automatically, including Steam collections.

**Do I need to open ports on my router?** No. Playit.gg creates a public tunnel without port forwarding.

**How much RAM does the server use?** The notebook sets the server to 6 GB, safely below Colab's ~12.7 GB limit.

**Will my world be lost when Colab disconnects?** No. The world and configs are stored on your Google Drive and reloaded on the next session.

**Can I play with friends on b41 and b42?** Yes — pick the version in Cell 1; the notebook installs the matching dedicated server branch (legacy 41 or stable 42).

## ⚠️ Important Notes

* **Playit.gg is pinned to `v0.15.26`** on purpose (Colab console compatibility). Do not upgrade.
* **Colab limits:** free sessions last up to 12 hours with an inactivity timeout (~90 min). Use the notebook's anti-idle script and restart the server after reconnecting.
* **Port changes:** if you change the UDP port in Cell 3, update the matching tunnel in your [Playit.gg](https://playit.gg/account) dashboard.

## 🤝 Contributing

Pull requests are welcome! This project aims to be a solid base for the community to stress-test mods, maps and configurations in multiplayer environments without local infrastructure costs. Found a bug or have ideas to reduce RAM/CPU usage on Colab? Open an [Issue](https://github.com/Andresdotdev/PZColab/issues).

## 📄 License

This project is licensed under the [MIT License](LICENSE). Free to use, modify and distribute for your own testing.
