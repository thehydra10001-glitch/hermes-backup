---
name: codebase-memory-mcp
description: The fastest code intelligence engine for AI coding agents — full-indexes repos in milliseconds, answers structural queries in under 1ms. Ships as a single static binary with 15 MCP tools for codebase understanding.
metadata:
  source: https://github.com/DeusData/codebase-memory-mcp
  version: 1.0
---

# Codebase Memory MCP — Code Intelligence Engine

The fastest code intelligence engine for AI coding agents. Full-indexes an average repository in milliseconds, the Linux kernel (28M LOC, 75K files) in 3 minutes. Answers structural queries in under 1ms.

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

Then restart your coding agent and say **"Index this project"**.

## 15 MCP Tools
- Architecture overview, call graph tracing, impact analysis
- Semantic search (vector + BM25 + structural)
- Dead code detection, ADR management
- Cross-service linking (HTTP, gRPC, GraphQL, tRPC)
- Cypher-like queries on the knowledge graph
- 3D graph visualization UI at localhost:9749

## Key Features
- 158 languages via tree-sitter AST parsing
- Hybrid LSP for semantic type resolution (Python, TS/JS, Go, Rust, Java, C++, etc.)
- 120x fewer tokens vs file-by-file search
- Zero dependencies — single static binary
- All processing 100% local
