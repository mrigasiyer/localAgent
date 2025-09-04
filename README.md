# LocalAgent – Autonomous LLM Tool Runtime

**LocalAgent** is a Python-based autonomous agent runtime that runs on your local machine, integrates with local LLMs via [Ollama](https://ollama.com/), and intelligently decides when to use tools like a shell or calculator to answer user prompts — inspired by agentic frameworks like AutoGPT, OpenDevin, and Devika.

This project is the foundation for a larger open-source platform for LLM prompt evaluation, runtime orchestration, and agentic behavior testing.

---

## ✅ Features (So Far)

- **Multi-step agent reasoning loop** — rethinks after every tool use
- **Modular Tool Interface** — easy to add tools like shell commands, calculator, etc.
- **Local LLM inference** via Mistral running on [Ollama](https://ollama.com/)
- **Secure evaluation sandbox** for math expressions (`eval` w/ safelist)
- Learns from prior tool results using an internal `history` memory
- Handles malformed LLM output (extra lines, hallucinated answers, etc.)

---

## Current Stack



## Example Usage

```bash
$ python agent_brain.py

Enter Prompt: what is 52 * 12  
[LLM OUTPUT]
TOOL: calc  
INPUT: 52 * 12

Jarvis: Result: 624

---

Enter Prompt: create folder test123 and list it  
[LLM OUTPUT]
TOOL: shell  
INPUT: mkdir test123 && ls test123

Jarvis: a.txt  
b.txt  
c.txt ...