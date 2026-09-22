# Higher-Order Cancellation (V5 fixed) — second-vendor re-audit

Auditor: fable (second-vendor confirmation pass, post-fix).
Manuscript: `inbox/higher-order-cancellation/v5/higher_order_cancellation.tex` (V5, repaired)
Driver: `v5/code/verify_hoc.py` — Lean: `v5/lean/` (ExpHOC) — Auditor code: `/tmp/audit_v5b/my_verify.py` (independent; not the shipped driver).

## Verdict

**CLEAN.** All previously reported defects are repaired, all mathematical claims re-verify against my own independent symbolic (sympy) and numeric (mpmath, 60–80 dps) code, the shipped driver genuinely asserts and fails loudly (tamper-tested), and the Lean gate passes from a clean rebuild: **13 theorems, standard axioms only**. The new-error hunt found **no substantive new error** — only two cosmetic wording nits (below), neither affecting correctness.

## Fixes verified

| # | Item | Status |
|---|------|--------|
| 1 | **General A4 formula (eq. A4)** now reads γ(α₁²α₂ − α₁⁴/4 − α₂²/2) + β(α₁⁵/5 − α₁³α₂ + α₁α₂²) | **CORRECT** — matches my own sympy expansion of (β/t+γ)·log(1+α₁t+α₂t²) at t⁴ exactly. The old misprinted form is gone from the manuscript (grep confirms no `α₁⁴/4 − α₁²α₂/2`-style β-block anywhere except inside the corrected formulas). I also confirmed the old form does **not** equal the true coefficient (symbolic non-zero difference). |
| 2 | **Driver asserts the general A4 identity** | **CORRECT** — line `check(... "eq(4b) general A4 (printed form) matches the expansion")` is present. **Tamper test:** I changed `a1**5/5 → a1**5/6` in a copy; the driver printed `[FAIL]`, reported `RESULT: 1 FAILURE(S)`, and **exited 1**. Untampered driver exits 0 with `ALL ASSERTIONS PASS`. Every Table 1/2 value is asserted at 0.5% rel-tol, slopes/intercepts at 5e-4, R² thresholded, all constants and signs asserted. |
| 3a | Two previously uncited bibitems | **FIXED** — all 12 bibitems are now cited at least once (checked mechanically: brent 1, glaisher 1, adams 1, mitchell 1, flajolet 2, dlmf39 3, corless2023 2, richardson2024 1, richardson2024arxiv 1, yangtian 1, yangtianarxiv 1, balditerative 1). |
| 3b | arXiv 2401.07562 author order | **FIXED** — bibitem now lists Oates, Karvonen, Teckentrup, Strocchi, Niederer; matches arXiv `citation_author` metadata fetched today (Oates first). |
| 3c | "150-digit" vs dps mismatch | **FIXED** — text says 150-digit precision and the appendix script sets `mp.mp.dps = 150`. (The verification driver runs at dps 60, which is ample for the 3-s.f. table assertions; I reproduced all table values independently at dps 60 and 80 with identical roundings.) |
| 3d | §6.2 cost paragraph | **FIXED** — now explicitly states "We deliberately state no bit-complexity bound" and disclaims the O(log n)-operations claim; no unsupported complexity assertion remains. |
| 3e | Lemma 2.3 hypothesis | **FIXED** — now "for some integer k ≥ 0", and the k=0 case (n⁻² coefficient B + A²/2) is handled in the proof. Prop 3.1 uses it with k=0 consistently. |
| 3f | Table 3 qualified | **FIXED** — caption reads "(parameterized rows: fixed c≠0)"; §6.1 states the signed-asymptotic hypothesis holds "for every family compared below"; Remark 6.1 corrects the old middle row (limit e^{c²}, order Θ(n⁻²)). |
| 4 | **Constants & multiplier** | **RE-CONFIRMED** independently: A₃^(I) = c(2√3−3)/72, A₃^(II) = −c(3+2√3)/72 (symbolic, from my own expansion + branch substitution); multiplier −3e^c (numeric: n⁴Dₙ^(I) → −0.05256 = −3e·A₃^(I), n⁴Dₙ^(II) → +0.73214 = −3e·A₃^(II) at n=10⁶); A₄^(I,II) = c(39∓25√3)/720 (symbolic **and** numeric via n⁴(log xₙ − c − A₃/n³) → A₄, matching to 6 decimals). Constraint system re-derived: A₁=0 ⇒ γ = c(½−α₂); A₂=0 then ⇒ α₂² = 1/12 ⇒ α₂ = ±√3/6. Both displayed constraint equations match my expansion. |

## Lean

Ran the gate myself (not trusting a stale cache): symlinked `.lake/packages → /home/work/Projects/artin-lean/artin/.lake/packages` (already in place), **deleted `.lake/build` to force a full clean rebuild**, exported `~/.elan/bin` on PATH, ran `./gate.sh`:

```
PASS (13 theorems, standard axioms only)
```

- All 13 `#print axioms` outputs verified individually: every theorem depends only on `[propext, Classical.choice, Quot.sound]`.
- No `sorry`/`admit`/`axiom`/`native_decide` in the sources (gate greps; I read both files in full).
- **Lean ↔ paper cross-check:** `A3`/`A4` definitions in `Basic.lean` are token-for-token the paper's eq. (A3)/(A4), including the corrected β-block `a1^2*a2 − a1^4/4 − a2^2/2` and the A4 γ/β blocks. Branch theorems prove: A₁=0, A₂=0 (both branches), A₃^(I) = c(2√3−3)/72, A₃^(II) = −c(3+2√3)/72, A₄^(I) = c(39−25√3)/720, A₄^(II) = c(39+25√3)/720, nonvanishing of A₃ for c≠0, and the opposite-sign statement for c>0 (`branch_signs`) — all exactly matching the paper's constants and Remark 1.4.
- Scope note (properly disclosed in the file header): Lean covers the exact algebraic core only; the analytic content (limit, −3e^c multiplier, Θ-rates) is driver/auditor-verified, as the paper states.

## New-error hunt

Everything below was checked with my own code or by hand; none of it turned up a substantive error.

- **Log-expansion coefficients c₀–A₄ (general):** all five printed formulas match my sympy expansion exactly.
- **Theorem 1.5 / abstract asymptotics:** Dₙ ~ −3e^c A₃ n⁻⁴ confirmed numerically for both branches at n = 10⁶ (c=1), and n³(xₙ−e^c) → e^c A₃ with correct signs. Remark 1.4's sign/magnitude claims (branch I smaller |Dₙ|, from above for c>0; II from below) match: 0 < 2√3−3 < 3+2√3, and the numeric signs agree.
- **Lemma 1.1 (positivity):** 1 − √3/6 = (6−√3)/6 > 0 — trivially correct.
- **Lemma 1.2 (tail):** L − xₙ = Σ_{n≥N} Dₙ indexing is right; p-series tail Σ_{n≥N} n⁻⁴ = N⁻³/3 + O(N⁻⁴) confirmed numerically; the signed conclusion L − x_N → −e^c A₃ N⁻³ confirmed for both branches at N = 10⁵ (consistency of Lemmas 1.2 + 2.3 + Theorem).
- **Remark 1.3 counterexample** (xₙ = 1 + (−1)ⁿn⁻⁴): |Dₙ| ~ 2n⁻⁴ = Θ(n⁻⁴) while |xₙ−1| = n⁻⁴ — correct.
- **Prop 3.1 (classical baseline):** Dₙ ~ e^{ab}a²b/(2n²) confirmed numerically for (a,b) ∈ {(1,1),(2,2),(1,2),(2,3),(−1,2)} at n = 10⁶; a=b does **not** cancel (Euler ratio → 1/2). Remark 3.2's correction statement is accurate.
- **Design principle re-indexing:** first nonzero A_k gives Dₙ = −k e^c A_k n^{−(k+1)} — consistent with Lemma 2.3 relabeled; verified in the theorem's k=3 instance.
- **Tables 1 & 2:** all 22 tabulated values reproduced independently and every 3-s.f. rounding matches, including the previously mis-rounded 8.40×10⁻¹⁷ (my dps-80 value: 8.404953×10⁻¹⁷).
- **Regression:** my own least-squares on the stated grid (n = 100, 125, …, 10000): slopes −3.99729/−3.99690, intercepts −2.96963/−0.33910, R² = 0.999999725/0.999999642 — all four quoted coefficients match to every printed digit, and both R² values round to exactly the printed 0.9999997/0.9999996.
- **Remark 4.1 cross-check value:** substituting branch I parameters into the old misprinted form indeed gives c(9−4√3)/18 (my symbolic check), which differs from both the correct value and the V4 constant — the remark's claim is true. (See nit below on branch labeling.)
- **c=0 exception:** both sequences identically 1 — confirmed.
- **Appendix script:** read in full; formulas, grid, and leading-constant check are correct and match the paper.
- **Gate script:** logic is sound (fails on sorry/admit/axiom/native_decide, on build failure, on <12 audited theorems, on any nonstandard axiom); rebuilt from scratch so the count of 13 comes from real compilation, not cache.

**Two cosmetic nits (not errors):**

1. **Remark 4.1 wording:** "substituting the branch parameters into the incorrect form gives c(9−4√3)/18" — this is the branch-I value only; branch II under the incorrect form gives c(9+4√3)/18. Saying "the branch-I parameters" would be precise. The mathematical claim as applied to branch I is correct.
2. **Lemma 2.3 proof, one clause:** "we therefore have Rₙ = O(n^{−(k+2)}), whence ΔRₙ = O(n^{−(k+3)}) by the triangle inequality" compresses two steps: the size bound alone does not give the improved difference bound; one needs Rₙ = B n^{−(k+2)} + O(n^{−(k+3)}) (which the previous line established), difference the explicit B-term smoothly, and apply the triangle inequality to the O(n^{−(k+3)}) tail only. The lemma and conclusion are **true** and the full argument is present in substance (the B-term is retained in the displayed expansion); this is a one-clause exposition compression, consistent with what the other vendor's V5 audit classified as a clarity point, not an error. A one-line rewrite would close it.

## What is sound

- The complete mathematical chain: general expansion coefficients c₀–A₄ → constraint system → two branches (α₂ = ±√3/6, γ = c(½∓√3/6)) → A₃, A₄ closed forms → −3e^c multiplier → Θ(n⁻⁴) differences → Θ(N⁻³) error. Every link independently re-verified.
- All numerics in the paper (Tables 1–2, both regressions, both R² values) reproduce exactly at the printed precision.
- The shipped driver is a genuine gate: comprehensive assertions, correct exit-code behavior, tamper-test confirmed.
- The Lean development compiles cleanly, proves exactly what it claims (13 theorems matching the paper's constants), uses only the three standard axioms, and honestly documents its scope.
- Framing, novelty claims, corrections of the earlier draft, and bibliography are accurate and appropriately conservative.

## Remaining items

Optional polish only; nothing blocks acceptance:

1. Remark 4.1: say "the branch-I parameters" (nit #1 above).
2. Lemma 2.3 proof: expand the "whence ΔRₙ = …" clause into the two-step argument (nit #2 above).
3. (Very minor) The driver asserts R² > 0.999999 as a threshold rather than the printed 7-digit values; my independent code confirms the printed values exactly, so this is a driver-hygiene note, not a manuscript issue.

**Bottom line: the revision is clean. All previously reported errors are fixed, all repairs verify independently, and no new substantive error was found.**
