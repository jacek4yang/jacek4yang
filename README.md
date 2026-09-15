<div align="center">

<img src="assets/hero.svg" alt="Jacek Yang — Systems / Network / Security / AI. Building fast systems and tools close to the metal." width="100%">

<br>

**Systems · Networking · Security · AI Tooling**

Building fast systems, network software, reverse-engineering infrastructure,
cryptographic experiments and developer agents — mostly in Rust.

<br>

**[▸ ENTER INTERACTIVE PROFILE](https://jacek4yang.github.io)** — a live network-topology visualization of my work, with a system map, project telemetry and an interactive terminal.

<br>

</div>

```text
$ whoami
systems developer — Rust-first, everything below is production-shaped work
with benchmarks, fuzz targets and CI behind it, not tutorials.
```

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
<sub>reverse-mcp · rust-reality · egressdns · fastcrypto-rs · cline-proxy · rnc</sub>
</div>
