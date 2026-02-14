# ProtocolBox Roadmap 🗺️

This document outlines the development trajectory for ProtocolBox. We prioritize tools that provide high-leverage capabilities to AI Agents (scrapers, browsers, sandbox execution).

## 🚀 Q1 2026 Objectives (v0.2.0)

### New Tools
- [ ] **`search(query)`**: High-performance SERP API wrapper (Google/Bing) for real-time grounding.
- [ ] **`browser`**: Headless browser control for interacting with dynamic JS-heavy sites (beyond simple scraping).
- [ ] **`filesystem`**: Safe, sandboxed file I/O permissions for agents to read/write their own workspace.

### Infrastructure
- [ ] **Docker Image**: Official `protocolbox/server` image for easy deployment in containerized agent swarms.
- [ ] **Auth**: Simple Bearer token authentication for the MCP server.

## 🔮 Future Concepts (v0.3.0+)

- **Agent Sandbox**: A secure Python execution environment (REPL) for agents to run generated code safely.
- **Vector Memory**: Built-in simple RAG interface for agents to store/retrieve context across sessions.
- **Multi-Modal**: Tools for resizing/converting images and processing audio.

## 🤝 How to contribute

See a feature here you want?
1. Check [Issues](https://github.com/ianuragbhatt/protocolbox/issues) to see if it's already in progress.
2. Comment on the issue or open a new one expressing interest.
3. Submit a PR!
