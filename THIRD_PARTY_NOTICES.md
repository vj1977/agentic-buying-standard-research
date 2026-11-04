# Third-party notices

## Code, data and attack implementations

None are vendored. Everything in `acs/`, `tests/`, `data/`, `rulebook/`, `expert/` and
`results/` was written for this project, in Python 3.14 using only the standard library:
- the harness, metrics and analysis;
- the scenario and catalogue data;
- the rulebook;
- the expert kit.

Attack payloads came from two places:
- hand-written scenario text (static and hard sets);
- the attacker model's own output during the red-team run (`results/runs/redteam.jsonl`).

No public benchmark task (for example AgentDojo or WASP), dataset or published attack
implementation was copied.

`standard/` belongs to another project lane; its notices are kept there.

| Item | Licence | Source | How used |
|---|---|---|---|
| Python 3.14 standard library | PSF License | https://www.python.org/ | runtime |
| Claude Code CLI (`claude`) | Anthropic terms | https://claude.com/claude-code | invoked as a subprocess; not distributed |
| Grok CLI (`grok`) | xAI terms | https://x.ai/ | invoked as a subprocess; not distributed |
| Codex CLI (`codex`) | OpenAI terms | https://github.com/openai/codex | backend implemented; not usable in this session; not distributed |
| Gemini CLI (`gemini`) | Apache-2.0 | https://github.com/google-gemini/gemini-cli | backend implemented; account rejected; not distributed |

## Methods adopted (re-implemented from the papers; cited)

- Wilson score interval: E. B. Wilson (1927), "Probable inference, the law of succession, and
  statistical inference", JASA 22(158).
- Exact McNemar test: Q. McNemar (1947), "Note on the sampling error of the difference between
  correlated proportions or percentages", Psychometrika 12(2).
- Cohen's kappa: J. Cohen (1960), "A coefficient of agreement for nominal scales", Educational
  and Psychological Measurement 20(1).
- Percentile bootstrap: B. Efron (1979), "Bootstrap methods: another look at the jackknife",
  Annals of Statistics 7(1).
- Trusted monitoring, the AI-control framing for the C3 monitor: R. Greenblatt, B. Shlegeris et
  al. (2023), "AI Control: Improving Safety Despite Intentional Subversion", arXiv:2312.06942.
- Indirect prompt injection, the threat model for the injection traps: K. Greshake et al.
  (2023), "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications
  with Indirect Prompt Injection", arXiv:2302.12173.
- Agent injection benchmarks (related work; nothing reused): E. Debenedetti et al. (2024),
  "AgentDojo", arXiv:2406.13352.
- Motivation, an LLM running a shop: Anthropic (2025), "Project Vend".
- Canonical JSON for hashing, referenced only: RFC 8785, JSON Canonicalization Scheme. The
  harness uses its own sorted-key JSON serialisation, not an RFC 8785 implementation.
- Optimised attack on an LLM judge, the model for the Phase 3 adaptive evidence attack
  (`acs/attack.py`): J. Shi, Z. Yuan, Y. Liu, Y. Huang, P. Zhou, L. Sun, N. Z. Gong (2024),
  "Optimization-based Prompt Injection Attack to LLM-as-a-Judge", ACM CCS 2024, arXiv:2403.17710.
  Re-implemented from the paper's description as a black-box feedback loop with an attacker model
  in place of gradient optimisation; the JudgeDeceiver repository carries no licence and none of
  its code or data was copied.
- Intermediate vs end-to-end attack success, the two metric names used in the Phase 3 tables:
  I. Evtimov, A. Zharmagambetov, A. Grattafiori, C. Guo, K. Chaudhuri (2025), "WASP: Benchmarking
  Web Agent Security Against Prompt Injection Attacks", NeurIPS 2025 Datasets and Benchmarks,
  arXiv:2504.18575. Definitions adopted; no code (CC BY-NC 4.0) or data reused.
- Safety-usefulness curve across abstention thresholds, the framing of the H6 re-analysis
  (`acs/analyze_phase3.py`): Greenblatt, Shlegeris, Sachan, Roger (2023), already cited above.
  Computed with this project's own code; nothing from `control-evaluations` (MIT) was copied.

## Standards referenced, never copied

ISO 20022, ISO 17442 (LEI), ISO 18245 (MCC), ISO 3166 and ISO 4217 are named only in
`standard/`. Card-scheme rules are described in general terms with no rule numbers. The EU
Consumer Rights Directive withdrawal right is described in general terms.
