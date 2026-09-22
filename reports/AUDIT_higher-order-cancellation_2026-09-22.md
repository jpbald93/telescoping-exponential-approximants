# Audit — *Higher-Order Cancellation in Exponential Approximants: An Explicit O(n⁻⁴) Telescoping Family* (V4)

**Author:** Josh Bald (Independent Researcher) · **Date:** December 2025 · **Length:** 17 pp
**Artifact:** `paper.pdf` sha256 `572cf3f5dc7f4b11431c835f4bb94fde43ddd07bd6f10914f047aca195e017db`
**Audit date:** 2026-09-22 · **Method:** line-by-line reading + independent symbolic (sympy) and high-precision (mpmath, 90 dps) verification (`audit/verify_hoc.py`, output `audit/verify_output.txt`) + separate-vendor adversarial re-audit (see `AUDIT_astra_higher-order-cancellation.md`).

---

## Verdict: **MAJOR REVISION**

The paper's **structural results are correct** — the two-branch family does converge to `e^c`, the difference does decay like `Θ(n⁻⁴)`, and the error decays like `Θ(N⁻³)` — and **every number in its tables is right**. But the paper's headline contribution (§1.6/1.7: *explicit closed-form leading constants*) is **wrong**: the `A₃` coefficient formula (eq. 4), the stated constants `A₃ = c(9∓5√3)/36`, and the finite-difference factor `−4e^c` are all incorrect. The classical baseline in §1.5 / Prop 3.1 is also wrong. Notably, the paper's **own tables contradict its own stated formulas** and agree with the corrected ones.

The good news: the correct constants are clean and the fix is small (see below).

---

## 1. The `A₃` coefficient formula (eq. 4) is wrong

Expanding `log x_n = (βn+γ)·log(1 + α₁/n + α₂/n²)` in powers of `1/n` (sympy, exact):

| eq. | paper | correct | match |
|---|---|---|---|
| (1) | `c₀ = α₁β` | `α₁β` | ✅ |
| (2) | `A₁ = α₁γ + βα₂ − α₁²β/2` | same | ✅ |
| (3) | `A₂ = γα₂ − α₁²γ/2 + α₁³β/3 − α₁α₂β` | same | ✅ |
| (4) | `A₃ = γ(α₁³/3 − α₁α₂) + β(α₁⁴/4 − α₁²α₂/2)` | `A₃ = γ(α₁³/3 − α₁α₂) + β(α₁²α₂ − α₁⁴/4 − α₂²/2)` | ❌ |

The `γ`-part of eq. (4) is right; the **`β`-part is wrong** — the signs on `α₁⁴` and `α₁²α₂` are wrong/garbled and the `−α₂²/2` term (from `−u²/2`, `u = α₁t+α₂t²`) is missing entirely. (Check: eq. (4) as printed gives, for the two branches, `c(9−4√3)/18` and `c(4√3+9)/18` — **not** the `c(9∓5√3)/36` the paper states. So eq. (4) and the stated constants don't even agree with each other.)

## 2. The stated `A₃` constants are wrong

Substituting `α₁=1, β=c, α₂=±√3/6, γ=c(1/2∓√3/6)`:

| branch | paper states | **correct** | numeric (implied) |
|---|---|---|---|
| I | `c(9−5√3)/36 ≈ 0.0094374c` | `c(2√3−3)/72 ≈ 0.0064459c` | `0.0064454c` ✅ |
| II | `c(9+5√3)/36 ≈ 0.4905626c` | `−c(3+2√3)/72 ≈ −0.0897792c` | `0.0897726c` ✅ |

The numeric values `n⁴|Dₙ| /(3e^c)` converge to the **correct** constants (Family I: `0.006245→0.006445` as n: 10³→5·10⁴; Family II: `0.089448→0.089773`), matching `c(2√3−3)/72` and `c(3+2√3)/72` — **not** the stated ones (which are off by ×1.46 and ×5.46 respectively, with a wrong sign for II).

## 3. The finite-difference factor is `−3e^c`, not `−4e^c`

`log x_n = c + A₃/n³ + O(n⁻⁴)` ⇒ `x_n = e^c(1 + A₃n⁻³ + …)` ⇒
`Dₙ = e^c A₃[(n+1)⁻³ − n⁻³] + … = −3e^c A₃ n⁻⁴ + …`.

So Theorem 1.4's `Dₙ ∼ −4e^c A₃/n⁴` should read **`Dₙ ∼ −3e^c A₃/n⁴`**. This also **contradicts the paper's own Lemma 2.3**, which correctly gives `−(k+1)e^c A n^{−(k+2)}` = `−3e^c A₃` for `k=2`. Numeric confirmation: `3·e·A₃(correct) = 0.0525650` vs measured `n⁴|D_I| = 0.0525641` (n=2·10⁵) ✅; `4·e·A₃(paper) = 0.10261` ✗.

## 4. The classical baseline (§1.5, Prop 3.1) is wrong

Prop 3.1 claims `Dₙ = e^{ab}·ab(a−b)/(2n²) + O(n⁻³)` for `xₙ = (1+a/n)^{bn}`, hence `Dₙ = O(n⁻³)` iff `a=b`. **Both are false.** Direct expansion gives `Dₙ ∼ e^{ab}·a²b/(2n²)`. Numeric `n²Dₙ/e^{ab}`:

| (a,b) | measured | `a²b/2` (correct) | `ab(a−b)/2` (paper) |
|---|---|---|---|
| (1,1) | 0.49999 | 0.5 | 0.0 |
| (1,2) | 0.99997 | 1.0 | −1.0 |
| (2,3) | 5.99942 | 6.0 | −3.0 |
| (3,5) | 22.4938 | 22.5 | −15.0 |

At `a=b=1` (Euler's sequence) the paper predicts `O(n⁻³)`, but the true rate is `Θ(n⁻²)` (`n²Dₙ/e → 1/2`). So the "order-1 cancellation at `a=b`" story — and the whole "design principle" framing built on it — is wrong. (The cited Newman–Sofer 1990 result concerns precisely `(1+1/n)ⁿ` and gives `e/(2n²)`, i.e. it supports the corrected formula, not the paper's.)

## 5. Design-principle indexing is off by one (§2.3)

The design principle reads "to achieve telescoping order `k`, enforce `A₁=…=A_k=0`, leaving `A_{k+1}≠0`." With Lemma 2.3 that yields `Dₙ = Θ(n^{−(k+2)})`, i.e. **order `k+1`**, not order `k`. The consistent statement (used, correctly, in §4.2) is: order `k` ⟺ `A₁=…=A_{k−1}=0`, `A_k≠0`.

## 6. Text vs. tables: the tables are right

Reproducing Table 1 (c=1) at 90 dps:

| n | `|D_I|` (measured) | paper | `|D_II|` (measured) | paper |
|---|---|---|---|---|
| 100 | 5.0902e-10 | 5.09e-10 ✅ | 7.0579e-9 | 7.06e-9 ✅ |
| 500 | 8.3562e-13 | 8.36e-13 ✅ | 1.1628e-11 | 1.16e-11 ✅ |
| 1000 | 5.2395e-14 | 5.24e-14 ✅ | 7.2944e-13 | 7.29e-13 ✅ |
| 5000 | 8.4050e-17 | 8.41e-17 ✅ | 1.1705e-15 | 1.17e-15 ✅ |

and `|xₙ−e|` likewise (1000: `1.7505e-11` vs `1.75e-11`; `2.4374e-10` vs `2.44e-10`). These values match the **corrected** constants (`−3e^c A₃`, `A₃ = c(2√3−3)/72`) to the displayed digits, and are **inconsistent** with the paper's stated formulas (which would give `1.03e-13` and `1.02e-12` at n=1000). Table 2 (c=2, c=−1) is likewise correct and consistent with the corrected constants. The regression slopes `−3.995/−3.994` correctly confirm `Θ(n⁻⁴)`.

**So the paper's numerics validate the true result — its stated analytic constants are the error.**

## What is sound

- `lim_{n→∞} xₙ^{(·)} = e^c` — ✅ (verified to 18 digits).
- `|Dₙ| = Θ(n⁻⁴)` and `|x_N − e^c| = Θ(N⁻³)` — ✅ (rates correct; `n⁴|Dₙ|` and `n³|xₙ−e^c|` converge).
- `A₃ ≠ 0` for `c≠0` — ✅ (though the paper's justification uses the wrong constants).
- Lemma 1.1 (positivity), Lemma 1.2 (tail rate), Lemma 2.3 (log→difference, factor `−(k+1)`) — ✅ correct.
- Eqs. (1), (2), (3) — ✅ correct.
- Remark 1.5 (branch labeling: `I` has smaller `|Dₙ|`) — ✅ correct.
- The `A₁=A₂=0` solve (`α₂² = 1/12`) — ✅ correct.
- All tabulated numbers (Tables 1–2) and regression slopes — ✅ correct.
- Reproducibility script (Appendix A) — plausible and self-contained (uses the correct sequence, hence reproduces the *correct* numbers).

## Recommended repairs

1. **Fix eq. (4):** the `β`-group is `β(α₁²α₂ − α₁⁴/4 − α₂²/2)`.
2. **Fix the constants:** `A₃^{(I)} = c(2√3−3)/72`, `A₃^{(II)} = −c(3+2√3)/72`.
3. **Fix the factor:** `Dₙ ∼ −3e^c A₃ n⁻⁴` (consistent with the paper's own Lemma 2.3).
4. **Fix §1.5 / Prop 3.1:** `Dₙ ∼ e^{ab}a²b/(2n²)`; the `a=b` case does **not** cancel (it is `Θ(n⁻²)`), so either correct the classical baseline or replace it.
5. **Fix the design-principle indexing** (order `k` ⟺ `A₁…A_{k−1}=0`, `A_k≠0`).
6. Add a driver assertion tying the stated constants to the measured `n⁴|Dₙ|`, so text and table can never diverge again.

## Bottom line

The **construction, the rate, the limit, and all numerics are correct and reproducible**; the **explicit constants — the paper's stated novelty — are wrong**, as is the classical order-1 baseline. This is a genuine MAJOR REVISION, but a surgically small one: five corrections, all local, none touching the structural result. The corrected constants (`c(2√3−3)/72`, `−c(3+2√3)/72`) are clean and are already what the paper's own tables compute.
