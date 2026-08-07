# Contributing to PZColab

Thanks for helping make free Project Zomboid servers on Google Colab better for everyone! 🧟

## How to contribute

1. **Open an issue first** for bugs or feature ideas — describe the problem, the Colab runtime you use, and what you saw in the console.
2. **Fork the repo** and create a branch for your change.
3. Make your changes — see [Development notes](#development-notes).
4. **Test in Google Colab** before opening the PR (the real environment can't be simulated locally).
5. Open a **Pull Request** against `main` with a clear description and any console output showing it works.

## Development notes

- The product lives in **`PZ_Colab_EN.ipynb`** (English, primary) and **`PZ_Colab_ES.ipynb`** (Spanish). The English notebook is derived from the Spanish source through a translation table — keep both in sync.
- **Keep UI messages clean:** users run these cells in Colab, so keep console output purposeful and non-noisy.
- **Do not change the pinned Playit.gg version (`v0.15.26`)** — newer agent versions don't work well as a tunnel on Colab.
- **Respect Colab limits:** ~12.7 GB RAM (keep `-Xmx` ≤ 8 GB) and free sessions up to ~12 h.
- **Never hardcode passwords** — empty admin password fields are recovered from the server `.ini` or auto-generated.
- Update the **README.md / README.es.md** documentation when you change user-facing behavior.

## Code of conduct

Be respectful and constructive. This project serves the Spanish- and English-speaking Project Zomboid community — keep discussions inclusive.
