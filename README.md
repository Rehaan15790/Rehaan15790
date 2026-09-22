<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rehaan15790/Rehaan15790/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Rehaan15790/Rehaan15790/main/assets/banner-light.svg">
  <img alt="Rehaan Taherbhoy — B.Tech Artificial Intelligence &amp; Data Science" src="https://raw.githubusercontent.com/Rehaan15790/Rehaan15790/main/assets/banner-dark.svg" width="100%">
</picture>

First-year B.Tech student in Artificial Intelligence & Data Science. I build
local-first AI systems — voice interfaces, LLM tooling, and the security around them.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rehaan_Taherbhoy-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rehaan-taherbhoy-5b59ab426/)
[![GitHub](https://img.shields.io/badge/GitHub-Rehaan15790-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Rehaan15790)

## Featured — [ultron](https://github.com/Rehaan15790/ultron)

[![tests](https://github.com/Rehaan15790/ultron/actions/workflows/tests.yml/badge.svg)](https://github.com/Rehaan15790/ultron/actions/workflows/tests.yml)
[![release](https://img.shields.io/github/v/release/Rehaan15790/ultron?color=ff2a2a&label=release)](https://github.com/Rehaan15790/ultron/releases)
[![license](https://img.shields.io/github/license/Rehaan15790/ultron?color=ffb43c)](https://github.com/Rehaan15790/ultron/blob/main/LICENSE)

A local voice-driven AI assistant with a command-center interface. Speech in,
speech out, everything on one machine — and the model sits downstream of every
security decision.

<a href="https://github.com/Rehaan15790/ultron"><img src="https://raw.githubusercontent.com/Rehaan15790/ultron/main/docs/hud-session.png" alt="Ultron HUD during a live session" width="100%"></a>

- Local `faster-whisper` transcription and `qwen2.5:14b` via Ollama — audio and prompts never leave the machine
- Sanitizer → deterministic router → tiered permission gate, with every decision written to an audit log
- 37 sandbox-escape tests; found and fixed a path traversal, a stored XSS, and a leaked credential along the way
- 111 tests, run in CI on Ubuntu and Windows

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![faster-whisper](https://img.shields.io/badge/faster--whisper-4B5563?style=for-the-badge)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-000000?style=for-the-badge&logo=elevenlabs&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

## Up next

Sentence-chunked TTS streaming for ultron — cutting time-to-first-audio from ~6s to ~2s.
