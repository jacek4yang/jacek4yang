# <img src="assets/mono.svg" alt="j4y" width="28" align="top">&nbsp; jacek4yang

Systems developer. Rust-first — everything below is production-shaped work
with benchmarks, fuzz targets, and CI behind it, not tutorials.

<br>

## Selected work

<table>
<tr>
<td width="50%" valign="top">

### [reverse-mcp](https://github.com/jacek4yang/reverse-mcp)
MCP server exposing IDA Pro's headless `idalib` for AI-driven binary
analysis — stdio and HTTP transports. The flagship: actively developed,
built for real reversing workflows.
<br><br>
`Rust` · `IDA 9.2` · `MCP`

</td>
<td width="50%" valign="top">

### [rust-reality](https://github.com/jacek4yang/rust-reality)
From-scratch implementation of VLESS and REALITY. ~5.9 MB of Rust plus a
hand-written assembly layer for session-establishment crypto on 1-vCPU hosts.
<br><br>
`Rust` · `Assembly` · `TLS 1.3`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [egressdns](https://github.com/jacek4yang/egressdns)
Egress-aware DNS resolver: Cloudflare anycast optimization, DNSSEC
validation, hot reload. Packaging, fuzzing, and benches included.
<br><br>
`Rust` · `DNSSEC` · `Networking`

</td>
<td width="50%" valign="top">

### [fastcrypto-rs](https://github.com/jacek4yang/fastcrypto-rs)
Cryptographic R&amp;D staging for rust-reality: benchmarks X25519, AES-GCM,
SHA-2, and ML-KEM-768 against their production incumbents on real workload
shapes — keeps what wins, delegates what doesn't.
<br><br>
`Assembly` · `Rust` · `Cryptography`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [grok-build](https://github.com/jacek4yang/grok-build)
Fork of xai-org's model-agnostic coding-agent harness — native
multi-provider protocols, semantic tool execution, cross-platform runtime.
Used and extended as a daily driver.
<br><br>
`Rust` · `Agents` · `Tooling`

</td>
<td width="50%" valign="top">

### [rnc](https://github.com/jacek4yang/rnc)
Binary-safe netcat in Rust with native Windows Unicode and full
UTF-8 / GBK / GB18030 support over TCP and UDP. Built for CTF and
CJK-heavy terminal work that GNU netcat mangles.
<br><br>
`Rust` · `Windows` · `Sockets`

</td>
</tr>
</table>

<br>

## Also in the orbit

- **[agent-pulse](https://github.com/jacek4yang/agent-pulse)** — Windows scheduler for resuming terminal AI coding agents
- **[cline-proxy](https://github.com/jacek4yang/cline-proxy)** — Rust gateway aggregating Cline API keys, Claude Code / OpenAI compatible
- **[rime-xhup-flow](https://github.com/jacek4yang/rime-xhup-flow)** — 小鹤音形 Rime scheme with a graphical training platform

<br>

## Focus

`reverse engineering` · `network protocols` · `applied cryptography` · `agent infrastructure` · `Windows internals`
