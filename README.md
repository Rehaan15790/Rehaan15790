# Hi, I'm Rehaan

First-year B.Tech student in Artificial Intelligence & Data Science. I build
local-first AI systems — voice interfaces, LLM tooling, and the security around them.

[LinkedIn](https://www.linkedin.com/in/rehaan-taherbhoy-5b59ab426/)

## Featured — [ultron](https://github.com/Rehaan15790/ultron)

[![tests](https://github.com/Rehaan15790/ultron/actions/workflows/tests.yml/badge.svg)](https://github.com/Rehaan15790/ultron/actions/workflows/tests.yml)

A local voice-driven AI assistant with a command-center interface. Speech in,
speech out, everything on one machine — and the model sits downstream of every
security decision.

<a href="https://github.com/Rehaan15790/ultron"><img src="https://raw.githubusercontent.com/Rehaan15790/ultron/main/docs/hud-session.png" alt="Ultron HUD during a live session" width="100%"></a>

- Local `faster-whisper` transcription and `qwen2.5:14b` via Ollama — audio and prompts never leave the machine
- Sanitizer → deterministic router → tiered permission gate, with every decision written to an audit log
- 37 sandbox-escape tests; found and fixed a path traversal, a stored XSS, and a leaked credential along the way
- 111 tests, run in CI on Ubuntu and Windows

## Stack

`Python` · `FastAPI` · `Ollama` · `faster-whisper` · `ElevenLabs` · `SQLite` · `pytest`

## Up next

Sentence-chunked TTS streaming for ultron — cutting time-to-first-audio from ~6s to ~2s.
