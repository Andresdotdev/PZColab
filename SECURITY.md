# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| `main` | ✅ |

## Reporting a vulnerability

If you discover a security issue in PZColab (e.g., credential handling, the Colab notebook code, or anything that could compromise a user's Google Drive or GitHub account):

1. **Do not open a public issue** with the details.
2. Email the maintainer at **kristianurrea@hotmail.com** or open a [private advisory](https://github.com/Andresdotdev/PZColab/security/advisories/new).
3. Include the affected file/cell, a description of the flaw, and (if possible) a minimal reproduction.

We aim to respond within a few days and will coordinate a fix before any public disclosure.

## Security notes for users

- Never commit real passwords: an empty admin password field makes the notebook recover the existing `.ini` password or generate a new random one.
- The notebook stores only a small state file (`ZomboidSaves/.pzcolab_state.json`) in your own Google Drive — it contains no credentials.
- Review the notebook code before running it if you are unsure — it executes shell commands (apt, SteamCMD, Playit) inside your Colab session.
