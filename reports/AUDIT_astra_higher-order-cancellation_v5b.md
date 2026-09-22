# Higher-Order Cancellation (V5 fixed) — re-audit

## Verdict

**The repaired general A4 formula is CORRECT, the branch constants and main asymptotic theorem are CORRECT, and the Lean algebraic development passes.** Independent SymPy/mpmath calculations reproduce every numerical table entry and both regressions, including the printed R² values.

**The revision is mathematically sound in its principal results, but not completely clean as written.** There remains a small, readily repaired justification gap in the proof of Lemma 2.3: the triangle inequality does not improve the order of an arbitrary remainder's difference. The stronger expansion already present in that proof supplies the missing justification, so this is not a counterexample to the lemma or main theorem. Also, the driver's R² assertion checks a threshold, not agreement with the specific printed R² values; its table tolerances do not certify exact three-significant-figure rounding. These are limitations of the claimed verification coverage, not incorrect numerical results.

No new incorrect coefficient, branch constant, table entry, regression value, or Lean theorem was found.

## Fixes verified

1. **General A4 — CORRECT.** At `higher_order_cancellation.tex`, equation `eq:A4`, the coefficient is now
   \[
   A_4=\gamma\left(a_1^2a_2-\frac{a_1^4}{4}-\frac{a_2^2}{2}\right)
   +\beta\left(\frac{a_1^5}{5}-a_1^3a_2+a_1a_2^2\right).
   \]
   I independently expanded the logarithmic derivative \(Q'/Q\), integrated coefficientwise, and multiplied by \(\beta/t+\gamma\), with \(Q=1+a_1t+a_2t^2\). The result agrees identically, as do c0 and A1–A3. The former sign-flipped gamma block is absent from the active manuscript formula, Lean definition, and driver assertion. The retained historical correction remarks concern older A3 errors, not an active recurrence of the A4 error.

2. **Driver general identity and failure behavior — CORRECT.** `code/verify_hoc.py:46–47` explicitly tests the general A4 identity rather than only branch substitutions. `check` records failed conditions and the final block calls `sys.exit(1)` if any failed. Running the unmodified driver returned exit code 0 and `RESULT: ALL ASSERTIONS PASS`; the entire output matches the shipped `code/verify_output.txt` byte for byte. An additional in-memory fault-injection run forced just the general-A4 check to fail, without changing the shipped source: it reported that failure and exited with code 1.

3. **Driver tables and R² — qualified confirmation.** All 16 numerical cells in Table 1 and all 12 in Table 2 are individually checked (`EXP1`, `EXP2`, lines 123–134). However, the relative tolerance is 0.5%, which is weaker than correct three-significant-figure rounding. For R², line 156 asserts only `float(r2) > 0.999999`; there is no assertion against `0.9999997` and `0.9999996`. Thus the driver does assert a property of R², but not the manuscript's particular rounded values. My independent checks certify all 28 cells at their actual printed rounding precision and both printed R² values at seven decimal places.

4. **Lemma 2.3 — statement CORRECT; proof needs a local repair.** It now allows integer \(k\ge0\), has the extra coefficient required for differencing, and correctly handles the \(B+A^2/2\) coefficient when \(k=0\). The remaining issue is the justification at lines 295–297; see the next section on the new-error hunt.

5. **Proposition 3.1 — corrected index and formula CORRECT.** The proof now invokes the lemma at \(k=0\), and \(D_n=e^{ab}a^2b/(2n^2)+O(n^{-3})\) is correct. Strictly, that invocation applies when \(a,b\ne0\), because the lemma assumes \(A\ne0\). The zero cases are already identified as the constant sequence in the proposition; explicitly disposing of them before the invocation would remove this minor implicit case split.

6. **Section 6.1 tail qualification — CORRECT.** The Θ-tail implication is now conditioned on the signed asymptotic \(D_n=Kn^{-(k+1)}+O(n^{-(k+2)})\), \(K\ne0\), rather than an absolute Θ-bound alone.

7. **Table 3 qualification — CORRECT.** Its caption explicitly restricts parameterized rows to fixed \(c\ne0\), and the surrounding text correctly identifies the classical target as \(e^{c^2}\).

8. **Computational-cost correction — CORRECT in the requested respect.** The unsupported operation-count claim has been removed; the paragraph explicitly disclaims a competitive complexity or bit-complexity bound and explains that one need only evaluate \(x_N\), not sum N differences. The stated index-versus-error scaling is the exact-arithmetic truncation rate; fixed working precision should not be understood as guaranteeing arbitrarily small errors below its numerical accuracy.

9. **Bibliographic repairs — CORRECT.** The arXiv Richardson entry is Oates-first, followed by Karvonen, Teckentrup, Strocchi, Niederer; I checked the arXiv page's citation-author metadata. The Princeton reference now names Sedgewick and Flajolet, *An Introduction to the Analysis of Algorithms*, Chapter 4, matching the linked booksite. Both Yang–Tian entries are cited in Open Problem 3. A source-level citation-key check finds 12 bibliography entries, all cited, with no undefined citation keys.

10. **Branch constants and multiplier — CORRECT, symbolically and numerically.** Independent substitution gives
    \[
    A_3^{\mathrm I}=\frac{c(2\sqrt3-3)}{72},\qquad
    A_3^{\mathrm {II}}=-\frac{c(3+2\sqrt3)}{72},
    \]
    \[
    A_4^{\mathrm I}=\frac{c(39-25\sqrt3)}{720},\qquad
    A_4^{\mathrm {II}}=\frac{c(39+25\sqrt3)}{720}.
    \]
    Independently shifting the formal variable \(t\mapsto t/(1+t)\) yields the stronger check
    \[
    D_n=e^c\left[-3A_3n^{-4}+(6A_3-4A_4)n^{-5}+O(n^{-6})\right].
    \]
    In particular, the multiplier is **−3eᶜ**, not −4eᶜ.

## Lean

The required symlink was already correctly configured:

```text
lean/.lake/packages -> /home/work/Projects/artin-lean/artin/.lake/packages
```

I preserved it, exported `PATH="$HOME/.elan/bin:$PATH"`, and independently ran `./gate.sh`:

```text
PASS (13 theorems, standard axioms only)
```

Exit status was 0. I additionally ran `lake env lean ExpHOC/Basic.lean` to elaborate the actual proof source and `lake env lean ExpHOC/Check.lean` for a direct axiom audit. All 13 audited theorems report exactly:

```text
[propext, Classical.choice, Quot.sound]
```

Reading `Basic.lean` confirms that:

- A1–A4 definitions match the manuscript, including the repaired A4 gamma block.
- Both branch parameter substitutions match the paper.
- Four branch-cancellation theorems prove A1=A2=0.
- Four coefficient theorems prove exactly the stated A3 and A4 constants.
- Two nonvanishing theorems use the required hypothesis c≠0, and `branch_signs` uses c>0.
- The remaining two audited theorems establish the needed facts about √3.
- There are no placeholder proofs or additional declared axioms in these sources.

The scope is accurately described as **the exact algebraic core**. It does not formalize the Taylor-series derivation, asymptotic remainder arguments, exponential limits, or finite-difference multiplier. The gate's numerical minimum is 12, but the actual current audit contains and checks 13; this does not invalidate the reported current result.

## New-error hunt

### 1. Remaining proof justification gap: Lemma 2.3, lines 295–297

The proof says

> R_n = O(n^{−(k+2)}), whence ΔR_n = O(n^{−(k+3)}) by the triangle inequality.

That inference is false from the displayed bound alone: the triangle inequality gives only \(O(n^{-(k+2)})\). For example, \(R_n=(-1)^n n^{-(k+2)}\) has a difference of that same order.

**Crucially, this counterexample does not satisfy the stronger remainder structure already available in this proof.** The statement of the lemma is true. To repair the proof, explicitly retain that structure. Put

\[
C=\begin{cases}B+A^2/2,&k=0,\\B,&k\ge1,\end{cases}
\qquad
R_n=Cn^{-(k+2)}+E_n,\quad E_n=O(n^{-(k+3)}).
\]

Then

\[
\Delta R_n=C\big((n+1)^{-(k+2)}-n^{-(k+2)}\big)+\Delta E_n
=O(n^{-(k+3)}),
\]

using the power-term estimate and the triangle inequality **on E_n**, not on the coarser bound for R_n. This is a local proof correction, not a change to any theorem or asymptotic coefficient.

### 2. Verification coverage is weaker than the strongest prose claim

The driver checks every table cell but with a loose tolerance, and checks an R² lower bound rather than the two quoted rounded values. Accordingly, the Verification Summary's assertion that the driver confirms every numeral should not be read as an exact printed-rounding certificate. Add branch-specific R² expectations with a half-unit rounding tolerance and tighten the table checks to the precision printed in each cell.

A separate minor reproducibility detail: the shipped full driver sets `mp.mp.dps = 60` at line 74, although the manuscript describes its numerical validation and Table 1 as 150-digit calculations. The appendix's short script does set 150 digits. My own complete table/regression rerun used 150 digits and reproduced the values, so this is a documentation/driver alignment issue, not evidence of inaccurate tables.

### Whole-manuscript result

I checked the base positivity argument, telescoping indices, signed tail summation, the corrected classical family, cancellation constraints, branch signs and nonvanishing, all c=0 exclusions, the main theorem's use of the stronger logarithmic expansion, the comparison table, regression grid, historical coefficient checks, appendix formulas, bibliography coverage, and the Lean definitions/theorems. **No additional substantive mathematical error was found.**

## What is sound

The independent checker does not import the supplied driver. It derives logarithmic coefficients through Q′/Q, performs exact symbolic branch substitutions and the discrete shift, and uses 150-digit `log1p`/`expm1` evaluations for numerical differences and errors. Numerical asymptotic checks include c=−7, −1, −0.01, 0, 0.01, 1, 2, 7; both branches; and the subleading A4 contribution.

For c=1:

| Quantity | Branch I | Branch II |
|---|---:|---:|
| A3 | 0.0064458557658021470424 | −0.089779189099135480376 |
| A4 | −0.0059739863739193504697 | 0.11430731970725268380 |
| Limit of n⁴Dₙ | −0.052564957791143818578 | 0.73213541490590512742 |
| Regression slope | −3.997288000927257301903 | −3.996903943945855834062 |
| Regression intercept | −2.969630554215946622948 | −0.3391037398617156947405 |
| R² | 0.9999997246485026867618 | 0.9999996417766585529202 |

Every quoted table cell and regression value rounds correctly. The two branches have the stated opposite signed errors, the claimed n⁻⁴ difference order, and the claimed N⁻³ approximation-error order for fixed nonzero c. The zero parameter gives identically 1 as stated.

Reproducibility artifacts saved alongside this report:

- `v5b_independent_check.py`
- `v5b_independent_check_output.txt`
- `v5b_shipped_driver_rerun.txt`
- `v5b_driver_failure_test.txt`
- `v5b_lean_gate.txt`
- `v5b_lean_basic.txt`
- `v5b_lean_axioms.txt`

## Remaining items

1. Replace the false standalone triangle-inequality inference in Lemma 2.3 with the explicit remainder decomposition above.
2. For literal verification of the printed numerals, assert each quoted R² and tighten rounding tolerances; align the full driver's working precision with the manuscript's 150-digit description.
3. Optionally make the already-understood zero-parameter case split explicit before Proposition 3.1 invokes the lemma.

**Bottom line:** the A4 repair is successful, all principal results and numerical values independently check out, and Lean passes with the claimed 13 standard-axiom theorems. A short proof-wording fix and small verification-description/checking adjustments remain before calling the revision completely clean.
