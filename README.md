<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/banner-dark-tall.svg">
  <source media="(max-width: 600px)" srcset="assets/banner-light-tall.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Dan Lichtenberger, New York. I build systems that make a measurable claim, and then I try to break the claim. Six projects deployed, 1,827 tests in CI, three negative results reported." src="assets/banner-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://danny-397.github.io"><b>Portfolio</b></a> &nbsp;·&nbsp;
  <a href="https://danny-397.github.io/reports.html"><b>Technical reports</b></a> &nbsp;·&nbsp;
  <a href="https://danny-397.github.io/reports/verification-ledger.html"><b>Verification ledger</b></a>
</p>

Six projects, built May to November 2026, each deployed to a URL you can open right now. Each one makes a claim with a number attached, and each has a test whose job is to break that claim. Three of them didn't beat their baseline, and they say so, with confidence intervals. Every figure below links back to how it was measured.

<br>

<a href="https://rl-for-crypto-and-stocks.vercel.app"><picture><source media="(max-width: 600px)" srcset="assets/01-rl-trader-tall.svg"><img src="assets/01-rl-trader.svg" width="100%" alt="How RL Agents Fool You: PPO from scratch tested across thirty seeds. A +275% single run was luck: 2 of 30 crypto seeds and 0 of 300 stock runs beat buy-and-hold."></picture></a>

**[Live lab](https://rl-for-crypto-and-stocks.vercel.app)** · [Source](https://github.com/Danny-397/RL-for-Crypto-and-stocks-) · [Paper](https://danny-397.github.io/reports/rl-trader-paper.html) · [DOI 10.5281/zenodo.23843503](https://doi.org/10.5281/zenodo.23843503) &nbsp;—&nbsp; PyTorch, Gymnasium; predictions pre-registered before the runs, 505 tests

<br>

<a href="https://quantumsafescan.com"><picture><source media="(max-width: 600px)" srcset="assets/02-quantumsafe-tall.svg"><img src="assets/02-quantumsafe.svg" width="100%" alt="QuantumSafe Scan: finds quantum-vulnerable cryptography in 11 languages. 95% precision on randomly sampled real-world findings, 88% recall on held-out real code, 584 tests."></picture></a>

**[Scan your code](https://quantumsafescan.com)** · [Source](https://github.com/Danny-397/Quantum-Safe-Scan) · [PyPI](https://pypi.org/project/quantumsafe-scan/) · [GitHub Action](https://github.com/marketplace/actions/quantumsafe-scanner) · [Report](https://danny-397.github.io/reports/quantumsafe-technical-report.html) · [DOI](https://doi.org/10.5281/zenodo.23843488) &nbsp;—&nbsp; exports SARIF and CycloneDX CBOM; Shor's algorithm demonstrated in Qiskit

<br>

<a href="https://alphaglyph.org"><picture><source media="(max-width: 600px)" srcset="assets/03-alphaglyph-tall.svg"><img src="assets/03-alphaglyph.svg" width="100%" alt="AlphaGlyph: a backtesting lab that attacks its own results. 72% probability that its best backtest is overfit; its forecaster scores an AUC of 0.51, a coin flip, and says so. 367 tests."></picture></a>

**[Run a backtest](https://alphaglyph.org)** · [Source](https://github.com/Danny-397/Alphaglyph) · [Report](https://danny-397.github.io/reports/alphaglyph-technical-report.html) &nbsp;—&nbsp; Deflated Sharpe, CPCV, Fama-French; a 106k-parameter transformer served as ONNX in 512 MB

<br>

<a href="https://rlchess.xyz"><picture><source media="(max-width: 600px)" srcset="assets/04-chess-tall.svg"><img src="assets/04-chess.svg" width="100%" alt="AlphaZero-style chess engine written from scratch: network, tree search and self-play. 1,000 self-play games; its self-play collapses into threefold repetition, and across three seeds training leaves it 93 Elo worse than its random start."></picture></a>

**[Play the engine](https://rlchess.xyz/#play)** · [Source](https://github.com/Danny-397/RL-Chess-Engine) · [Report](https://danny-397.github.io/reports/rl-chess-technical-report.html) · [Experiments](https://danny-397.github.io/reports/rl-chess-experiment-results.html) &nbsp;—&nbsp; PUCT search, ResNet policy/value net, runs client-side in ONNX Runtime Web

<br>

<a href="https://www.tradeski.dev"><picture><source media="(max-width: 600px)" srcset="assets/05-tradeski-tall.svg"><img src="assets/05-tradeski.svg" width="100%" alt="Tradeski: a real-time market dashboard with an assistant grounded in your holdings. 79% on held-out assistant eval questions, every indicator hand-coded on NumPy, 321 tests."></picture></a>

**[Open the dashboard](https://www.tradeski.dev)** · [Source](https://github.com/Danny-397/Tradeski) · [Assistant eval](https://github.com/Danny-397/Tradeski/blob/main/docs/ski-eval/README.md) · [Report](https://danny-397.github.io/reports/tradeski-technical-report.html) &nbsp;—&nbsp; WebSockets, FRED macro data, Claude Haiku with nine tools and a check on every figure it quotes

<br>

<a href="https://danny-397.github.io/neural-canvas/"><picture><source media="(max-width: 600px)" srcset="assets/06-neural-canvas-tall.svg"><img src="assets/06-neural-canvas.svg" width="100%" alt="Neural Canvas, built for Hack the Arts 2026: paint glowing light in mid-air with your hands. 21 hand landmarks tracked about 60 times a second, on-device, in one HTML file."></picture></a>

**[Paint with your hands](https://danny-397.github.io/neural-canvas/)** · [Source](https://github.com/Danny-397/neural-canvas) · [Report](https://danny-397.github.io/reports/neural-canvas-technical-report.html) &nbsp;—&nbsp; MediaPipe, one-euro filtering, six-fold symmetry, no build step

<br>

### How I work

- **Ship it.** A repository nobody can run isn't evidence of anything, so every project has a live URL.
- **Try to break the result before trusting it.** Held-out test sets are written before the fixes. Predictions are committed before the runs. AlphaGlyph exists mostly to attack my own backtests.
- **Report what the data said.** When a headline number doesn't survive more seeds or a fairer comparison, I withdraw it in public and keep the correction on the page.

### Outside my own repos

**[Farama-Foundation/Gymnasium#1657](https://github.com/Farama-Foundation/Gymnasium/pull/1657)**: I traced an `AsyncVectorEnv` crash on autoreset to scalar substitution in the worker, then wrote a fix and a regression test (+85/−3). I argued from `SyncVectorEnv`'s behaviour that it was a library bug. A maintainer closed it as an environment bug instead. I still think the two vector envs should behave the same, but it was their call, and learning that codebase well enough to make the case was worth it.

<br>

<p align="center">
  <code>Python</code> · <code>PyTorch</code> · <code>NumPy</code> · <code>Flask</code> · <code>FastAPI</code> · <code>JavaScript</code> · <code>ONNX</code> · <code>Qiskit</code> · <code>Postgres</code> · <code>Docker</code> · <code>GitHub Actions</code>
</p>

<sub>Cards are generated by <a href="tools/build_cards.py"><code>tools/build_cards.py</code></a> from the figures in each project's own docs and CI.</sub>
