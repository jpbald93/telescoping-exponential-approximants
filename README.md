# Higher-Order Cancellation in Exponential Approximants — reproduction package

Source and verification package for the note

> **Higher-Order Cancellation in Exponential Approximants: An Explicit `O(n⁻⁴)` Telescoping Family** — Josh Bald, **V5**, September 2026.

The note builds an explicit two-branch family of elementary sequences converging to `e^c` whose successive differences `Dₙ = x_{n+1} − xₙ` decay at order `n⁻⁴` (telescoping order 3), obtained by enforcing coefficient-cancellation constraints inside the quadratic-base / affine-exponent class
`xₙ = (1 + a₁/n + a₂/n²)^{cn+γ}`.

Main result (`c ≠ 0`):

```
xₙ^(I)  = (1 + 1/n + √3/(6n²))^{cn + c(1/2 − √3/6)}
xₙ^(II) = (1 + 1/n − √3/(6n²))^{cn + c(1/2 + √3/6)}

Dₙ^(·) ~ −3 e^c A₃^(·) n⁻⁴ ,   A₃^(I) = c(2√3−3)/72 ,   A₃^(II) = −c(3+2√3)/72
⇒  |x_N − e^c| = Θ(N⁻³)
```

## Layout

```
paper/higher_order_cancellation.tex            manuscript (LaTeX)
paper/higher_order_cancellation.pdf            compiled manuscript
code/verify_hoc.py                             verification driver (sympy + mpmath)
code/verify_output.txt                         saved driver output
lean/ExpHOC.lean                               Lean 4 project root
lean/ExpHOC/Basic.lean                         exact algebraic core (theorems)
lean/ExpHOC/Check.lean                         #print axioms audit
lean/gate.sh                                   verification gate
lean/lakefile.toml, lake-manifest.json, lean-toolchain
reports/                                       independent audit reports
```

## What is verified, and how

**Lean 4 — exact algebraic core (`[Lean]`).** `lean/ExpHOC/Basic.lean` formalises the
log-expansion coefficients of equations (1)–(4) as polynomials in `(a₁,a₂,β,γ)` and proves,
over `ℝ` with `√3`:

- `branch_I_A1`, `branch_II_A1`, `branch_I_A2`, `branch_II_A2` — `A₁ = A₂ = 0` on both branches;
- `branch_I_A3 = c(2√3−3)/72`, `branch_II_A3 = −c(3+2√3)/72`;
- `branch_I_A4 = c(39−25√3)/720`, `branch_II_A4 = c(39+25√3)/720`;
- `branch_I_A3_ne_zero`, `branch_II_A3_ne_zero` (for `c ≠ 0`), `branch_signs` (opposite signs for `c > 0`).

Gate: `PASS (13 theorems, standard axioms only)` — every theorem depends only on
`propext`, `Classical.choice`, `Quot.sound`.

**Driver — every numeral (`[sym]`/`[num]`).** `code/verify_hoc.py` regenerates every number in the
paper and **asserts every claimed sign and constant**, exiting nonzero on any failed assertion. It
checks symbolically the identities (1)–(4) (including the general `A₄`), the branch cancellations and
constants, and numerically the limit `e^c`, the multipliers `n⁴Dₙ → −3e^c A₃` and
`n³(xₙ−e^c) → e^c A₃` (with signs), all tabulated values, the regression slopes/`R²`, and the
corrected classical baseline `Dₙ ~ e^{ab}a²b/(2n²)`.

**Not formalised:** the Taylor-series derivation of (1)–(4) and all asymptotic (`limit` / `Θ`) content.

## Reproduce

```bash
# driver (sympy + mpmath; asserts every sign)
cd code && python3 verify_hoc.py         # -> RESULT: ALL ASSERTIONS PASS

# manuscript
cd paper && pdflatex higher_order_cancellation.tex   # run 3×

# Lean gate (source-only repo: link a Mathlib build first)
cd lean
mkdir -p .lake && ln -sfn /path/to/mathlib-checkout/.lake/packages .lake/packages
export PATH="$HOME/.elan/bin:$PATH"
./gate.sh                                # -> PASS (13 theorems, standard axioms only)
```

## Revision history

This is **V5**. Earlier versions circulated with the following defects, all repaired here (and
flagged independently by two adversarial referees):

| defect | V5 correction |
|---|---|
| the `A₃` coefficient formula (eq. 4) had wrong signs and a missing term | corrected in eq. (4) |
| stated constants `A₃ = c(9∓5√3)/36` | corrected to `c(2√3−3)/72`, `−c(3+2√3)/72` |
| finite-difference multiplier `−4e^c` | corrected to `−3e^c` |
| classical baseline `Dₙ = e^{ab}ab(a−b)/(2n²)` (false) | corrected to `e^{ab}a²b/(2n²)`; `O(n⁻³) ⟺ a=0` or `b=0` |
| under-specified Lemma 2.3 | regularity hypothesis added; stated for `k ≥ 0` |
| off-by-one design principle | corrected to `A₁…A_{k−1}=0, A_k≠0` |
| Table 3 middle row | corrected to `(1+c/n)^{cn} → e^{c²}`, `Θ(n⁻²)/Θ(N⁻¹)` |
| two invalid citations | removed/repaired |

Reports from both independent audits (separate vendors, separate implementations) are in `reports/`.
