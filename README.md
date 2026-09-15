<div align="center">

<!-- dark/light adaptive hero: GitHub picks the variant matching the theme -->
<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/profile/hero-light.svg">
  <img src="assets/profile/hero-dark.svg" alt="Jacek Yang — systems developer. 2186 contributions in the last year, best streak 29 days." width="100%">
</picture>

<!-- typewriter subtitle: self-hosted SMIL animation, cycles through focus areas -->
<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/profile/typing-light.svg">
  <img src="assets/profile/typing-dark.svg" alt="Rotating summary: building high-performance network software in Rust; from-scratch VLESS + REALITY; DNS resolvers; AI agents driving IDA Pro; cryptographic primitives; protocol gateways." width="700">
</picture>

**Systems · Networking · Security · AI Tooling** — building fast systems, network
software, reverse-engineering infrastructure and developer agents, mostly in Rust.

**[▸ ENTER INTERACTIVE PROFILE](https://jacek4yang.github.io)** — live network-topology visualization, system map, project telemetry and an interactive terminal.

</div>

## Selected work

<table>
<tr>
<td width="50%" valign="top">

### [rust-reality](https://github.com/jacek4yang/rust-reality) — `NETWORK` `CRYPTO`
From-scratch VLESS + REALITY + Vision proxy server. Xray-compatible data path, kernel `splice` relays, zero-copy record batching.
<br><br>
**~5.9 MB Rust + hand-written assembly** for session-establishment crypto, tuned for 1-vCPU hosts. Handoff topology sheds ~82% line-download CPU/GiB.

</td>
<td width="50%" valign="top">

### [egressdns](https://github.com/jacek4yang/egressdns) — `NETWORK` `DNS`
Egress-aware adaptive DNS caching forwarder for enterprise LANs. DoT/DoH2/DoH3/DoQ upstreams with DNSSEC validation.
<br><br>
**Measures, never guesses**: transport, HTTP version and hedging decisions come from live network evidence; degrades to a correct plain caching forwarder.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [reverse-mcp](https://github.com/jacek4yang/reverse-mcp) — `REVERSE` `AGENTS`
MCP server giving AI agents headless, programmatic control of IDA Pro 9.2 via native `idalib` — 17 tools, stdio/HTTP, no Python bridge.
<br><br>
**Optimistic concurrency & honest capabilities**: `expected_revision` on every mutation; unimplemented ops fail loudly instead of faking success.

</td>
<td width="50%" valign="top">

### [fastcrypto-rs](https://github.com/jacek4yang/fastcrypto-rs) — `CRYPTO` `PERF`
Cryptographic R&D staging for rust-reality: benchmarks X25519, AES-GCM, SHA-2 and ML-KEM-768 against production incumbents.
<br><br>
**Keeps only what wins on real workload shapes** — measured ~12.3% server CPU/session win for owned X25519 — everything else stays delegated.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [cline-proxy](https://github.com/jacek4yang/cline-proxy) — `AGENTS` `PROTOCOL`
Rust gateway exposing OpenAI + Anthropic APIs over a pool of Cline keys, built to run Claude Code against Cline.
<br><br>
**Strict 429-only key rotation invariant** with Healthy→Cooling→HalfOpen state machine; streams translated statefully between SSE dialects.

</td>
<td width="50%" valign="top">

### [rnc](https://github.com/jacek4yang/rnc) — `TOOLS` `WINDOWS`
Binary-safe netcat in Rust for TCP/UDP pipelines and CTF terminals. Static native `nc.exe`, no runtime dependencies.
<br><br>
**Full UTF-8 / GBK / GB18030 console conversion** — native Windows Unicode where GNU netcat mangles CJK byte streams.

</td>
</tr>
</table>

<details>
<summary><strong>Also in the orbit</strong></summary>

<br>

- **[agent-pulse](https://github.com/jacek4yang/agent-pulse)** — Windows scheduler that resumes terminal AI coding agents (waits out quota resets, refocuses, types `continue`)
- **[codebuddy-proxy](https://github.com/jacek4yang/codebuddy-proxy)** — Anthropic Messages API proxy for CodeBuddy, tuned for Claude Code
- **[rust-xhttp](https://github.com/jacek4yang/rust-xhttp)** — pure-Rust XHTTP/VLESS server compatible with official Xray-core clients
- **[veilweave](https://github.com/jacek4yang/veilweave)** — post-quantum, forward-secret VLESS over WebSocket, end-to-end through Cloudflare Workers
- **[rime-xhup-flow](https://github.com/jacek4yang/rime-xhup-flow)** — 小鹤音形 Rime input scheme with graphical trainer and cross-platform tooling

</details>

<br>

## Technical focus

```text
SYSTEMS    Rust · async runtimes · zero-copy · kernel splice · assembly hot paths
NETWORK    TCP/IP · DNS/DoH/DoQ · proxy protocols (VLESS/REALITY/XHTTP) · QUIC
SECURITY   reverse engineering · binary analysis (IDA/idalib) · applied cryptography · DNSSEC
AGENTS     coding agents · MCP servers · protocol gateways · developer infrastructure
```

The full interactive map — every project as a node in one system graph — lives at
**[jacek4yang.github.io](https://jacek4yang.github.io)**.

<div align="center">
<br>
<a href="https://jacek4yang.github.io"><strong>ENTER INTERACTIVE PROFILE →</strong></a>
<br><br>
<sub>profile assets are regenerated daily from live GitHub data — no external metrics services</sub>
</div>
