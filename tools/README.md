# PZColab — Developer Tools

Tooling used to build and test the notebooks. Run everything from the repo root.

## Requirements

- Python 3.8+
- No external packages needed (standard library only)

## Build the notebooks

Regenerates **both** notebooks from the single source of truth:

```bash
python tools/build_pzcolab.py
```

- Output: `PZ_Colab.ipynb` (Spanish) and `PZ_Colab_EN.ipynb` (English) at the repo root.
- The English notebook is derived from the Spanish one by applying the translation table in `traducciones.py` — **never edit the EN notebook by hand**; edit the builder sources and the translation table instead.
- The builder validates the Python syntax of every code cell (IPython magics like `!` are filtered before compiling).

## Run the functional tests

Cell 4 (mods / collections) functional tests, run against each notebook:

```bash
python tools/test_cell4.py                    # Spanish notebook
python tools/test_cell4.py PZ_Colab_EN.ipynb  # English notebook
```

## Check for untranslated strings

Detects leftover Spanish UI strings in the English notebook (some hits are false positives — review the output):

```bash
python tools/check_en.py
```

## Golden rules

- **Playit.gg stays pinned to `v0.15.26`** — never "modernize" that download URL (newer agents don't work well as a Colab tunnel).
- **Colab RAM limit is ~12.7 GB** — never raise the `-Xms/-Xmx` patch above ~8 GB.
- **Never hardcode passwords** in the notebooks.
- Keep console output purposeful: users run these cells in Colab.
