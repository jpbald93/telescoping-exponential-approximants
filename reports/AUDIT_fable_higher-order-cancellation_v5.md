# Higher-Order Cancellation (V5) — second-vendor audit

**Manuscript:** `inbox/higher-order-cancellation/v5/higher_order_cancellation.tex` (V5, Sept 2026)
**Driver:** `v5/code/verify_hoc.py` (committed output `verify_output.txt`)
**Auditor:** second vendor (independent). All load-bearing claims re-derived with my own sympy/mpmath code (`reports/tmp_v5_secondvendor.py`), not the shipped driver. The shipped driver was also re-run: it reports `ALL ASSERTIONS PASS` and its committed `verify_output.txt` byte-matches a fresh run.

## Verdict

**The mathematics of V5 is essentially sound, and every V4 defect on the fix list is genuinely fixed.** The main theorem (two-branch order-3 family, limit e^c, D_n ~ −3e^c A3 n^⁻⁴, Θ(N⁻³) error), the corrected A3 constants, the corrected classical baseline, the repaired Lemma 2.3, the design-principle indexing, Table 3, the c≠0 exception, and the previously invalid citations are all now correct — each verified independently below.

**One new error was introduced in V5:** the printed general formula for **A4 (eq. (9), label `eq:A4`) has a sign error in its γ-block**. The γ-part is printed as `+γ(α1⁴/4 − α1²α2 + α2²/2)`; the correct coefficient of t⁴ in (βn+γ)log(1+α1/n+α2/n²) has γ-part `−γ(α1⁴/4 − α1²α2 + α2²/2)`. Ironically, the **branch constants** quoted downstream, A4^(I,II) = c(39∓25√3)/720, are the **correct** values (they follow from the correct A4 and are numerically confirmed to control the n⁻⁵ term) — so the paper is internally inconsistent: substituting the branch parameters into the printed eq. (9) yields c(369∓215√3)/720, which does **not** equal the quoted constants. The shipped driver asserts the printed forms of eqs (5)–(8) but computes A4 directly from the series without asserting the printed eq. (9) — which is exactly how this slipped through, and makes Appendix B's claim that the driver "confirms (5)–(9)" inaccurate for (9).

This is a contained, easily repaired defect: it does not touch Theorem 1's statement or proof (which uses only the branch A4 values, which are right). Everything else found is a nit.

## Claim-by-claim

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Eqs (5)–(8): c0, A1, A2, A3 formulas | **CORRECT** — my independent sympy expansion of (β/t+γ)log(1+α1t+α2t²) matches all four exactly. |
| 1b | Eq (9): A4 formula | **WRONG** — γ-block sign flipped (see below). β-block (α1⁵/5 − α1³α2 + α1α2²) is correct. |
| 2 | Branches: A1=A2=0; A3^(I)=c(2√3−3)/72; A3^(II)=−c(3+2√3)/72; A4^(I,II)=c(39∓25√3)/720; A3≠0 with opposite signs for c≠0 | **CORRECT** — all confirmed symbolically. Constraint system re-solved independently: with α1=1, β=c, sympy solve gives exactly α2=±√3/6, γ=c(1/2∓√3/6). α2²=1/12 checked by hand. 2√3−3≈0.464>0, 3+2√3≈6.464>0, so A3^(I)>0>A3^(II) for c>0. |
| 3 | Theorem (thm:main): lim x_n=e^c; D_n ~ −3e^c A3 n⁻⁴ (multiplier −3e^c, not −4e^c) | **CORRECT** — high-precision check at n=10⁶ for c∈{1, 2, −1, 0.5}, both branches: n⁴D_n/(−3e^c A3) − 1 ≈ 3×10⁻⁶, and the ratio converges monotonically toward 1 as n runs 10⁴→10⁷ (e.g. branch I, c=1: n⁴D_n = −0.05254795, −0.05256326, −0.05256479, −0.05256494 vs predicted −0.052564958). Also n³(x_n−e^c) → e^c·A3 with the correct sign on every branch/c tested; branch I approaches from above, branch II from below, for c>0, exactly as Remark on branch labeling states. |
| 4 | Lemma 2.3 (log-expansion ⇒ difference asymptotic) with new regularity hypothesis | **CORRECT** (sufficient); one redundancy noted below. |
| 5 | Proposition (prop:order1) / eq (1): D_n = e^{ab}a²b/(2n²)+O(n⁻³); O(n⁻³) iff a=0 or b=0 | **CORRECT** — symbolic expansion gives log x_n = ab − a²b/(2n) + a³b/(3n²) + O(n⁻³); numeric n²D_n/e^{ab} → a²b/2 verified for (a,b) = (1,1),(2,3),(−1,2),(3,−1),(0.5,0.5). Euler a=b=1 gives 0.4999986 → 1/2, i.e. Θ(n⁻²), confirming the V4 "cancellation at a=b" claim was false and V5's replacement is right. The iff is trivially correct (a²b=0 ⟺ a=0 or b=0 ⟺ x_n≡1). |
| 6 | Table 3 middle row: (1+c/n)^{cn} → e^{c²}, Θ(n⁻²)/Θ(N⁻¹) | **CORRECT** — verified lim = e^{c²} and n²D_n/e^{c²} → c³/2 ≠ 0 for c=1, 2, 0.5. At c=1 it coincides with Euler's row. |
| 7 | Tables 1–2 values and rounding; Remark 1.3 signed-asymptotics example | **CORRECT** — every one of the 16 Table 1 entries and 12 Table 2 entries reproduced exactly at 3 s.f. from my own code at 170 dps, including the repaired 8.40×10⁻¹⁷. The 1+(−1)ⁿn⁻⁴ example checks out: \|D_n\|·n⁴ → 2 (Θ(n⁻⁴)) while \|x_n−1\| = n⁻⁴ exactly. |
| 8 | Abstract c≠0 exception | **CORRECT** — present ("for any real c ≠ 0", plus the explicit "(At c=0 both sequences are identically 1…)" sentence). At c=0 both exponents vanish, x_n≡1, D_n≡0; driver checks this too. |
| 9 | Design principle indexing | **CORRECT** — "enforce c0=c and A_1=…=A_{k−1}=0, leaving A_k≠0" with Lemma applied at relabeled index k−1 gives D_n = −k e^c A_k n^{−(k+1)} = Θ(n^{−(k+1)}), i.e. order k per Definition (order k ⟺ D_n=Θ(n^{−(k+1)})). Instantiated at k=3: A1=A2=0, A3≠0, D_n~−3e^cA3n⁻⁴. Consistent everywhere (Theorem, §3.3, Remark on order). Off-by-one from V4 is gone. |
| 10 | References | Both flagged entries now **valid** (details below). Two bib entries are present but never cited (nit). |
| 11 | Regression numbers (§5) | **CORRECT** — my independent fit over n=100..10000 step 25: branch I slope −3.997288, intercept −2.9696306, R²=0.9999997246; branch II slope −3.9969039, intercept −0.33910374, R²=0.9999996418. All match the printed −3.9973/−2.9696/0.9999997 and −3.9969/−0.3391/0.9999996 at the stated precision. |
| 12 | Lemma 2.2 (tail rate) | **CORRECT** — indexing L−x_N = Σ_{n≥N}D_n is right; Σ_{n≥N}n^{−(k+1)} = N^{−k}/k + O(N^{−(k+1)}) is standard; numerically e−x_N vs (K/3)N⁻³ agree to ratio 0.99999 at N=10⁵. Consistent with §1.1's R_N = Σ_{n>N}D_n = L−x_{N+1}. |
| 13 | Positivity lemma (lem:pos) | **CORRECT** — 1−√3/6 = (6−√3)/6 ≈ 0.711 > 0. |

## The A3 constants and eq (4)

(V4's "eq (4)" is V5's eq (8), label `eq:A3`.)

- **Eq (8) as printed is correct.** My independent series expansion gives the t³ coefficient
  γ(α1³/3 − α1α2) + β(α1²α2 − α1⁴/4 − α2²/2), identical to the printed form. The V4 form β(α1⁴/4 − α1²α2/2) is indeed wrong, and Remark `rem:eq4`'s cross-check (wrong form ⇒ c(9−4√3)/18) is accurate — I confirmed that substitution too.
- **Branch constants correct.** A3^(I)=c(2√3−3)/72 ≈ 0.0064459c, A3^(II)=−c(3+2√3)/72 ≈ −0.0897792c; both nonzero for c≠0, opposite signs. The V4 values c(9∓5√3)/36 and the −4e^c multiplier are gone; the −3e^c multiplier is what Lemma 2.3 (k=2) demands and what the numerics show.
- **NEW ERROR — eq (9) (`eq:A4`).** The printed γ-block has the wrong overall sign:
  - Printed: A4 = **+γ(α1⁴/4 − α1²α2 + α2²/2)** + β(α1⁵/5 − α1³α2 + α1α2²)
  - Correct: A4 = **−γ(α1⁴/4 − α1²α2 + α2²/2)** + β(α1⁵/5 − α1³α2 + α1α2²)
  (The t⁴ coefficient of log(1+u) is −α1⁴/4 + α1²α2 − α2²/2; the printed version negates it.)
  Substituting the branch parameters into the *printed* formula yields c(369∓215√3)/720 (≈ −0.00471c and +1.0297c), which contradicts the quoted A4^(I,II)=c(39∓25√3)/720 (≈ −0.005974c and +0.114307c). The quoted branch values are the true ones: I verified numerically that n⁵(D_n − (−3e^cA3/n⁴)) → e^c(6A3 − 4A4) using the quoted A4 (branch I: 0.17008 vs predicted 0.170086; branch II: −2.70707 vs −2.70715 at n=10⁵). So §3.3's constants, the Theorem proof, and Open Problem 1 are unaffected — only the displayed general formula (9) is wrong.
  **Root cause visible in the driver:** `verify_hoc.py` asserts the printed closed forms for c0, A1, A2, A3 but takes A4 straight from the sympy series (`logx.coeff(t,4)`) without asserting the manuscript's eq (9). Hence "ALL ASSERTIONS PASS" while (9) is misprinted, and Appendix B's sentence "Symbolically it confirms (5)–(9)" overstates what the driver checks.

## The classical baseline

Fully fixed. Proposition `prop:order1` now states D_n = e^{ab}a²b/(2n²) + O(n⁻³) with the iff (a=0 or b=0) characterization; my symbolic and numeric checks confirm it (see row 5 above). Remark `rem:correction` candidly documents the V4 error (ab(a−b)/2, sham cancellation at a=b) and correctly notes n²D_n/e → 1/2 for Euler. Eq (1) in §1.5 matches the proposition. The proof's expansion log x_n = ab − a²b/(2n) + a³b/(3n²) + O(n⁻³) is exactly what sympy gives. The invocation of Lemma 2.3 "with k=0 … or by direct differencing" is slightly outside the lemma's stated k≥1 range, but the hedge ("or by direct differencing") is legitimate and the k=0 case in fact goes through by the same argument — not an error.

## Lemma 2.3

The V5 hypothesis — a genuine two-term expansion log x_n = c + A/n^{k+1} + B/n^{k+2} + O(n^{−(k+3)}) — **is sufficient, and the proof is correct.** I attempted to break it and could not:

- The exponentiated remainder is R_n = B n^{−(k+2)} + A²/2·n^{−(2k+2)} + (log-remainder) + higher cross terms. Its forward difference: Δ(Bn^{−(k+2)}) = O(n^{−(k+3)}); Δ(n^{−(2k+2)}) = O(n^{−(2k+3)}) ⊆ O(n^{−(k+3)}) for k≥0; and any sequence that is O(n^{−(k+3)}) automatically has forward difference O(n^{−(k+3)}) (triangle inequality). So ΔR_n = O(n^{−(k+3)}) holds and the conclusion D_n = −(k+1)e^cA n^{−(k+2)} + O(n^{−(k+3)}) follows. Adversarial choices of a wildly oscillating O(n^{−(k+3)}) log-remainder do not hurt: the target error is the same order as the remainder itself.
- **Stylistic note (not an error):** the extra clause "where the remainder is such that its forward difference is O(n^{−(k+3)})" is actually *vacuous* — every O(n^{−(k+3)}) sequence satisfies it trivially. The real fix relative to V4 is the inclusion of the explicit B/n^{k+2} term (whose difference is genuinely O(n^{−(k+3)}), unlike a bare O(n^{−(k+2)}) remainder). The pre-lemma motivating sentence explains this correctly. The redundant clause is harmless and could be dropped or reworded.
- The MVT step (n+1)^{−(k+1)} − n^{−(k+1)} = −(k+1)n^{−(k+2)} + O(n^{−(k+3)}) is fine.
- Application in the Theorem proof (k=2, A=A3, B=A4) satisfies the hypothesis since the branch sequences have full integer-power expansions of log x_n.

## Tables

- **Table 1 (c=1):** all 16 entries reproduced exactly at 3 s.f. by independent code at 170 dps, including the V4-mis-rounded cell now correctly 8.40×10⁻¹⁷ (true value 8.3997…×10⁻¹⁷).
- **Table 2 (c=2, −1):** all 12 entries reproduced exactly.
- **Table 3:** all three rows now correct. Euler: Θ(n⁻²)/Θ(N⁻¹) ✓. Classical (1+c/n)^{cn}: limit e^{c²} (not e^c), Θ(n⁻²)/Θ(N⁻¹) ✓ (V4's Θ(n⁻³)/Θ(N⁻²) row is gone and Remark `rem:table3` documents the fix accurately). Order-3: Θ(n⁻⁴)/Θ(N⁻³) ✓. Implicitly assumes c≠0 in the middle row (constant sequence at c=0) — covered by Prop 3.1's statement; acceptable.
- **§5 regression numbers:** match to all printed digits (see row 11). Committed `verify_output.txt` matches a fresh driver run bit-for-bit.

## References

- **Oates–Karvonen–Teckentrup–Strocchi–Niederer, "Probabilistic Richardson extrapolation", JRSS-B 87(2) (2025) 457–479, DOI 10.1093/jrsssb/qkae098** — **valid**. Confirmed via multiple independent index records (Helsinki research portal; bibliography aggregators listing JRSS-B 87, 2025) and the matching arXiv:2401.07562 (fetched: title and all five authors match).
- **Yang–Tian, "An accurate approximation formula for gamma function", J. Inequal. Appl. 2018, Article 56, DOI 10.1186/s13660-018-1646-6** — **valid**. Confirmed via Springer (volume 2018, article number 56, published 6 March 2018) and PMC; arXiv:1712.08051 fetched and matches.
- Spot-checks of the rest: Brent JACM 23(2) 1976 ✓; Glaisher, Messenger of Math 1 (1872) ✓; Adams, Proc. Roy. Soc. 27 (1878) ✓; Mitchell–Strain, Osiris 1 (1936) 476–496 ✓; DLMF §3.9 ✓; Corless, Maple Trans. 3(1) 2023, DOI 10.5206/mt.v3i1.14777 ✓ (title, venue, DOI all confirmed); Zenodo self-citation 10.5281/zenodo.17605158 resolves to "Telescoping Representations of Classical Iterative Methods and Constants", Bald ✓. **No fabricated or invalid entry remains.**
- **Nits:** (i) `yangtian` and `yangtianarxiv` are in the bibliography but **never cited in the body** (grep confirms zero \cite occurrences) — leftover from V4; either cite or drop. (ii) The `richardson2024arxiv` bibitem lists authors as "T. Karvonen, C. J. Oates, et al." but the arXiv author order is **Oates first** (C. J. Oates, T. Karvonen, …) — should match the primary entry.

## What is sound

- The complete chain: coefficient formulas (5)–(8) → constraint system → two branches (α2=±√3/6, γ=c(1/2∓√3/6)) → A3 branch constants → Lemma 2.3 (k=2) → D_n ~ −3e^cA3n⁻⁴ → Lemma 2.2 → Θ(N⁻³) error. Every link independently re-derived and numerically confirmed at up to 170 digits, for c ∈ {1, 2, −1, 0.5} and n up to 10⁷.
- The corrected classical baseline and its iff statement; the Euler check.
- Lemma 2.2 indexing and tail constant (numerically confirmed to 5+ digits).
- Remark 1.3's counterexample; branch-sign remark; positivity lemma; c=0 exception; design-principle indexing.
- Both quoted A4 *branch constants* (verified symbolically and via the n⁻⁵ residual e^c(6A3−4A4)).
- Tables 1, 2, 3; regression slopes/intercepts/R²; driver output reproducibility (committed output = fresh run).
- Both previously-invalid citations now resolve; honest correction remarks (rem:correction, rem:eq4, rem:const, rem:table3) accurately describe the V4 defects.

## Recommended repairs

1. **(Required) Fix eq. (9) (`eq:A4`):** change the γ-block sign to
   `A4 = γ(−α1⁴/4 + α1²α2 − α2²/2) + β(α1⁵/5 − α1³α2 + α1α2²)`.
   The downstream branch constants c(39∓25√3)/720 are already correct and need no change.
2. **(Required) Make the driver assert the printed A4 formula** (add a `check(sp.simplify(A4 - (printed form)) == 0, "eq A4")` mirroring the A3 check), so Appendix B's "confirms (5)–(9)" becomes true. Regenerate `verify_output.txt`.
3. (Minor) Either cite or remove the two uncited Yang–Tian bibliography entries; fix the author order in `richardson2024arxiv` (Oates first).
4. (Minor) Drop or reword the redundant clause in Lemma 2.3's hypothesis ("remainder's forward difference is O(n^{−(k+3)})" is automatic for an O(n^{−(k+3)}) remainder); the two-term expansion is what does the work.
5. (Nit) §6.2's cost bound O(ε^{−1/3} log(ε^{−1})·M(p)) contradicts the very next sentence ("this counts evaluations of one endpoint"): a single evaluation of x_N costs O(log N · M(p)) = O(log(ε^{−1})·M(p)); the ε^{−1/3} factor belongs only to the naive term-by-term summation the text says is unnecessary. State one or the other consistently.
6. (Nit) §5 and the Table 1 caption say "150-digit precision" while the appendix script sets `mp.mp.dps = 170` (and the driver uses 60/170 in different parts). Results are unaffected at 3 s.f.; align the stated precision with the code.
7. (Nit) In Theorem `thm:main`, "K^(·) = 3e^c|A3^(·)|" uses K for the magnitude, whereas Lemma 2.2's K is signed (for branch I, c>0, the signed constant is negative). A clarifying word ("with K the constant for |D_n|") would remove the ambiguity.

---
*Audit evidence: independent verification script at `reports/tmp_v5_secondvendor.py` (sympy symbolic expansion done from scratch; mpmath numerics at 60–170 dps; n up to 10⁷; c ∈ {1,2,−1,0.5}). Shipped driver re-run: ALL ASSERTIONS PASS; committed verify_output.txt identical to fresh run. References checked against arXiv, Springer, PMC, Maple Transactions, Zenodo API, and JRSS-B index records.*
