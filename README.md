# Dan Lichtenberger

**New York** · Building systems that make a measurable claim — then trying to break the claim.

Six projects, written May–August 2026, every one deployed to a live URL you can open right now.
Three of them report a **null or negative result**, because that's what the data said.

📊 **[danny-397.github.io](https://danny-397.github.io)** — all six projects, with the method behind each one
📄 **[Technical reports](https://danny-397.github.io/reports.html)** — one per project

---

### Selected work

| Project | What it is | Result |
|---|---|---|
| **[QuantumSafe Scan](https://github.com/Danny-397/Quantum-Safe-Scan)** · [live](https://quantumsafescan.com) | Finds cryptography quantum computers will break, across 11 languages, and maps each finding to its NIST FIPS 203/204/205 replacement | **100% precision** vs. a 49.1% naive-regex baseline on a labeled benchmark; on [PyPI](https://pypi.org/project/quantumsafe-scan/), exports SARIF + CycloneDX CBOM |
| **[RL Chess Engine](https://github.com/Danny-397/RL-Chess-Engine)** · [live](https://rlchess.xyz) | AlphaZero-style engine given only the rules, learning from self-play. Play the trained net in your browser | 10× more self-play bought **14 Elo**. Diagnosed as a *signal* problem, not compute: reweighting self-play moved Elo-vs-random **−21 → +28** at the same compute |
| **[RL-Trader](https://github.com/Danny-397/RL-for-Crypto-and-stocks-)** · [live](https://rl-for-crypto-and-stocks.vercel.app) | PPO written from the algorithm up, framed as a study of how deep-RL overfits and how you measure it honestly | A single seed showed **+275%**. Across 5 seeds it was **−2.7% [−31%, +27%]** — the edge was the seed. Domain randomization is what actually fixed it |
| **[AlphaGlyph](https://github.com/Danny-397/Alphaglyph)** · [live](https://alphaglyph.org) | Backtesting lab that runs its own results through Monte Carlo, Deflated Sharpe, and Fama-French | Built the instrument that indicts its own output: reports a **72% probability of backtest overfitting** on its own strategy grid |
| **[Tradeski](https://github.com/Danny-397/Tradeski)** · [live](https://tradeski.dev) | Full-stack analytics: WebSocket streaming, indicator engine, LLM analyst grounded in your actual holdings + Fed macro data | Real-time system with Postgres persistence and a live news-sentiment pipeline |
| **[Neural Canvas](https://github.com/Danny-397/neural-canvas)** · [live](https://danny-397.github.io/neural-canvas/) | Paint glowing light in mid-air with your hands — MediaPipe hand tracking, 100% in-browser | Built for **Hack the Arts 2026** |

---

### How I work

- **Every project ships to a real URL.** A repository nobody can run isn't evidence of anything.
- **I write the falsification test before I trust the result.** AlphaGlyph exists mostly to attack my own backtests.
- **Negative results get reported.** Three of the six above didn't beat their baseline, and they say so, with confidence intervals.

`Python` · `PyTorch` · `Flask` · `JavaScript` · `Postgres` · `Docker` · `GitHub Actions`
