# Higher-Order Cancellation (V4) — adversarial audit

## Verdict (ACCEPT / MINOR / MAJOR REVISION / REJECT)

**MAJOR REVISION.** The two displayed families genuinely converge to \(e^c\), with difference order \(n^{-4}\) and error order \(n^{-3}\) for \(c\ne0\). However, the paper's central explicit constants are wrong, its finite-difference multiplier is wrong, its classical comparison is false, and its general log-expansion lemma lacks a necessary remainder hypothesis. These are substantive mathematical errors, not cosmetic corrections. The numerical tables largely support the **corrected mathematics**, not the printed theorem.

Additional independently substantiated findings: the design principle has an indexing error; the stated regressions are not reproduced by the appendix's grid; one Table 1 entry is incorrectly rounded; the abstract omits the necessary exception \(c=0\); and references [2] and [16] have demonstrably invalid bibliographic details.

**Method and scope.** Read the entire supplied `paper.txt`, including the appendix and references; whitespace was also flattened before checking whether conditions or qualifications were supplied. All line references below use `nl -ba paper.txt` (760 newline-numbered lines; form-feed page separators do not create extra line numbers). I independently wrote and ran SymPy/mpmath checks, rather than accepting the paper's reported calculations. Numerical calculations used 150 decimal digits and `log1p` to avoid cancellation in the base logarithm. This report was created provisionally early in the audit, updated as checks completed, and finalized here.

Reproducibility files alongside this report:

- `AUDIT_astra_higher-order-cancellation_checks.py` — independent symbolic and numerical checks.
- `AUDIT_astra_higher-order-cancellation_checks.txt` — complete execution output.
- `AUDIT_astra_higher-order-cancellation_reference_checks.json` — retrieved Crossref metadata supporting the bibliography findings.

## Claim-by-claim (each with your own computation + line numbers)

### 1. Equations (1)–(4): three correct, one incorrect

**Lines 297–310.** Set \(t=1/n\). My SymPy expansion of
\[
(\beta/t+\gamma)\log(1+a_1t+a_2t^2)
\]
gives
\[
\begin{aligned}
c_0&=a_1\beta,\\
A_1&=a_1\gamma+\beta(a_2-a_1^2/2),\\
A_2&=\gamma(a_2-a_1^2/2)+\beta(a_1^3/3-a_1a_2),\\
A_3&=\gamma(a_1^3/3-a_1a_2)
 +\beta(-a_1^4/4+a_1^2a_2-a_2^2/2).
\end{aligned}
\]
Thus **(1), (2), and (3) are correct; (4) is incorrect.** The printed beta contribution has a wrong fourth-power sign, a wrong mixed-term coefficient/sign, and omits the \(-a_2^2/2\) term. Detailed comparison is below.

### 2. Cancellation system and branches: correct, but not their claimed A3

**Lines 315–339.** With \(a_1=1,\beta=c\), equation \(A_1=0\) gives \(\gamma=c(1/2-a_2)\). My substitution into \(A_2\) simplifies exactly to
\[
A_2=c(1/12-a_2^2).
\]
For \(c\ne0\), the two solutions are indeed \(a_2=\pm\sqrt3/6\), with precisely the exponents displayed in the paper. Direct symbolic substitution gives \(A_1=A_2=0\) on both branches. The correct constants are
\[
\boxed{A_3^{(I)}=\frac{c(2\sqrt3-3)}{72},\qquad
A_3^{(II)}=-\frac{c(3+2\sqrt3)}{72}.}
\]
Both are nonzero for \(c\ne0\). In particular, for positive \(c\) the branches have **opposite** leading-error signs, contrary to the printed pair.

### 3. Finite-difference factor: 3, not 4

**Lines 203–213, 349–353, 355–365; compare Lemma 2.3, lines 252–275.** My series calculation gives
\[
(n+1)^{-3}-n^{-3}=-3n^{-4}+6n^{-5}+O(n^{-6}).
\]
For these analytic families this implies
\[
\boxed{D_n=-3e^c A_3n^{-4}+O(n^{-5}).}
\]
Even the paper's own displayed multiplier \(-(k+1)\) becomes \(-3\), not \(-4\), upon its stated substitution \(k=2\) at line 349.

Independent high-precision signed tests at \(c=1\):

| n | \(n^4D_n^{(I)}\) | \(n^4D_n^{(II)}\) |
|---:|---:|---:|
| 100 | −0.0509023915699938 | +0.705787501431455 |
| 1,000 | −0.0523952617719882 | +0.729435660779543 |
| 10,000 | −0.0525479531132691 | +0.731864774128990 |
| 1,000,000 | −0.0525647877057044 | +0.732132707764448 |
| correct limit | **−0.0525649577911438** | **+0.732135414905905** |

These also verify the sign reversal for branch II. The positive magnitude constants are \(K^{(j)}=3e^c|A_3^{(j)}|\).

### 4. Classical baseline: false as printed

**Lines 133–146 and Proposition 3.1, lines 280–288.** Independent symbolic expansion and numerical tests establish
\[
\boxed{D_n=\frac{e^{ab}a^2b}{2n^2}+O(n^{-3}),}
\]
not \(e^{ab}ab(a-b)/(2n^2)\). Equality \(a=b\) does not cancel the leading term. The detailed tests and corrected iff statement appear in the dedicated baseline section below.

### 5. Numerical tables: substantially correct, unlike the explicit theorem

**Table 1, lines 389–399; Table 2, lines 402–420.** Direct evaluations reproduce all Table 1 entries to their displayed three significant figures **except** \(|D_{5000}^{(I)}|\), which is \(8.4049529988\ldots\times10^{-17}\) and should be printed \(8.40\times10^{-17}\), not \(8.41\times10^{-17}\). All four rows of Table 2 round correctly. Full reproduced values and the text/table contradiction are below.

### 6. Lemmas 1.1, 1.2, 2.3: two sound; one false as stated

**Lemma 1.1, lines 66–83 — CORRECT.** For \(n\ge1\), the plus base exceeds 1; the minus base is at least \(1-\sqrt3/6\). Independent evaluation gives \(1-\sqrt3/6=0.711324865405187\ldots>0\). Both real powers are well-defined for every integer \(n\ge1\) and every real \(c\).

**Lemma 1.2, lines 91–112 — CORRECT.** Under its actual signed-asymptotic hypothesis,
\[
\sum_{n\ge N}Kn^{-(k+1)}=(K/k)N^{-k}+O(N^{-k-1}),
\]
and the summed remainder is \(O(N^{-k-1})\). The integral bounds for the decreasing p-series establish the stated leading coefficient, including its sign. As an independent computational check, for \(K=2,k=3\), \(N^3\,2\zeta(4,N)\) equals 0.676733330000444, 0.667667333333, and 0.666766673333333 at \(N=100,1000,10000\), converging to \(2/3\). The indexing \(L-x_N=\sum_{n\ge N}D_n\) is correct. The alternate \(R_N=\sum_{n>N}D_n=L-x_{N+1}\) at lines 60–63 is also correct.

**Lemma 2.3, lines 252–275 — FALSE under its printed hypotheses.** Its exponentiation step is valid, and \(-(k+1)\) is the right multiplier when a suitably regular expansion exists. The problem is line 273: a general \(O(n^{-(k+2)})\) remainder cannot be differenced into \(O(n^{-(k+3)})\).

A concrete counterexample satisfying every displayed hypothesis with \(c=0,A=1,k=2\) is
\[
 x_n=\exp\!\left(n^{-3}+2(-1)^n n^{-4}\right).
\]
Then
\[
 n^4D_n=-3-4(-1)^n+O(n^{-1}),
\]
so the even and odd limits are \(-7\) and \(+1\), not \(-3\). My 150-digit code gives −6.999986000030 at \(n=1,000,000\) and +0.999998000012 at \(n=1,000,001\).

A sufficient repair is to assume
\[
\log x_n=c+A n^{-(k+1)}+B n^{-(k+2)}+O(n^{-(k+3)}),
\]
or explicitly impose the needed difference bound on the remainder. The present power-form families possess analytic expansions in \(t=1/n\), so this repair **does apply to them**. The proof gap does not invalidate their corrected asymptotics.

### 7. Design principle: off by one

**Definition 2.1, lines 228–232; principle, lines 276–277; application, lines 315–317.** If the first nonzero log coefficient is \(A_m\), an analytic expansion gives \(|D_n|=\Theta(n^{-m-1})\), hence telescoping order \(m\). Therefore order \(k\) requires
\[
c_0=c,\quad A_1=\cdots=A_{k-1}=0,\quad A_k\ne0.
\]
The printed principle cancels through \(A_k\) and leaves \(A_{k+1}\), thus producing **order \(k+1\)**. Section 4.2 correctly cancels only \(A_1,A_2\) to obtain order 3. My extracted branch coefficients \((c,0,0,A_3)\) provide a direct computational check of which indexing the construction uses.

### 8. Structural main claims: correct with c != 0

**Theorem 1.4, lines 186–213; proof, lines 355–365.** Despite the wrong constants, the following statements are **CORRECT**:
\[
x_n\longrightarrow e^c,\qquad |D_n|=\Theta(n^{-4}),\qquad
|x_N-e^c|=\Theta(N^{-3})\quad(c\ne0).
\]
Indeed, the verified coefficients and analyticity give
\[
x_n=e^c\{1+A_3n^{-3}+A_4n^{-4}+O(n^{-5})\},
\]
so \(x_n-e^c\sim e^c A_3n^{-3}\), and the difference formula follows without relying on the defective general lemma. My computations additionally give
\[
A_4^{(I)}=\frac{c(39-25\sqrt3)}{720},\qquad
A_4^{(II)}=\frac{c(39+25\sqrt3)}{720}.
\]
The normalized error \(n^3(x_n-e)\) tends to +0.0175216525970479 on branch I and −0.244045138301968 on branch II, matching \(eA_3\).

**Abstract exception:** lines 31–46 claim the nonzero-order conclusions “for any real c.” At \(c=0\), both sequences are identically 1 and every difference/error is zero, so neither Theta statement nor an asymptotic equivalence with nonzero leading constant holds. The theorem correctly excludes zero at line 188; the abstract must do the same.

### 9. Bibliographic spot-checks: real sources mixed with invalid metadata

These checks used source URLs and primary Crossref metadata, not memory or search absence alone.

- **[2], lines 554–555, cited as the proof of Proposition 3.1 at line 288: invalid as cited.** Crossref's records for *College Mathematics Journal* **21(4), 1990** identify pp.302–304 as “Fallacies, Flaws, and Flimflam,” DOI [10.1080/07468342.1990.11973323](https://doi.org/10.1080/07468342.1990.11973323), and pp.305–307 as Roger H. Marty's “The Number of Paths in a Rooted Binary Tree of Infinite Height,” DOI [10.1080/07468342.1990.11973324](https://doi.org/10.1080/07468342.1990.11973324). The claimed Newman–Sofer article cannot occupy pp.303–305. Targeted searches also did not locate the claimed work, but that alone would not prove nonexistence. **The supplied bibliographic record is demonstrably wrong and raises a fabrication concern; I do not claim to have proved that no differently cited Newman–Sofer work exists.** It cannot remain as the sole support for a false proposition.
- **[13–14], lines 598–604: real, relevant work.** [arXiv:2401.07562](https://arxiv.org/abs/2401.07562) is *Probabilistic Richardson Extrapolation*. Crossref for [10.1093/jrsssb/qkae098](https://api.crossref.org/works/10.1093/jrsssb/qkae098) confirms volume 87(2), pp.457–479. Correct author order: **Chris J. Oates, Toni Karvonen, Aretha L. Teckentrup, Marina Strocchi, Steven A. Niederer**. It was published online 26 December 2024; the journal issue is dated 11 April 2025. Cite 2025 for the issue or explicitly label the 2024 online-first date. This is a metadata correction, **not fabrication**.
- **[12], lines 593–596: verified.** Crossref confirms Robert Corless, *Devilish Tricks for Sequence Acceleration*, *Maple Transactions* 3(1), 2023, DOI [10.5206/mt.v3i1.14777](https://api.crossref.org/works/10.5206/mt.v3i1.14777).
- **[16], lines 610–614: real paper, substantially wrong citation.** Its supplied DOI [10.1186/s13660-018-1646-6](https://api.crossref.org/works/10.1186/s13660-018-1646-6) identifies **Zhen-Hang Yang and Jing-Feng Tian**, *An accurate approximation formula for gamma function*, **Journal of Inequalities and Applications (2018), article 56**, not Yang–Tian–Chen, *Advances in Difference Equations*, article 29. The associated [arXiv:1712.08051](https://arxiv.org/abs/1712.08051) exists and has the quoted title.

These are spot-checks, not a claim that every remaining reference has been authenticated.

### 10. Additional-error hunt

**A. A Theta difference bound alone does not give a Theta tail.** Lines 425–426 invoke Lemma 1.2 to claim that difference order determines the same exact tail order, although the definition uses \(|D_n|\) and supplies no sign control. The lemma's signed asymptotic is stronger. For an explicit computed counterexample, take
\[
x_n=1+(-1)^n n^{-4}.
\]
Then \(|D_n|=n^{-4}+(n+1)^{-4}=\Theta(n^{-4})\), but \(|x_n-1|=n^{-4}\), not \(\Theta(n^{-3})\). At \(n=1000\), \(n^4|D_n|=1.996009980034944\) and \(n^3|x_n-1|=0.001\); at \(n=10^6\), these are 1.99999600001 and \(10^{-6}\). An eventual fixed sign together with two-sided bounds, or Lemma 1.2's actual signed expansion, repairs the Theta conclusion. The weaker **O** tail bound stated at lines 104–105 and 230–232 remains valid under absolute difference bounds; I do **not** flag that weaker statement.

**B. Regressions are not reproducible as printed.** Lines 373–388 and Appendix A, lines 693–705, 753–755. For the appendix's exact grid \(n=100,125,\ldots,10000\), \(c=1\), natural logarithms, and independently implemented least squares, I obtain:

| Branch | slope | intercept | R² |
|---|---:|---:|---:|
| I | −3.9972880009272573 | −2.96963055421594662 | 0.999999724648502687 |
| II | −3.99690394394585583 | −0.339103739861715695 | 0.999999641776658553 |

These are not the printed slopes −3.995/−3.994 and intercepts −2.991/−0.363. Different sampling could produce different fits, so this finding is specifically that **the supplied reproducibility grid does not produce the reported fit**. The actual fitted slopes still substantiate fourth-order difference decay. The branch functions in Appendix A (lines 649–659) implement the displayed sequences correctly.

**C. Computational-cost discussion needs a stated model.** Lines 438–444 assign \(O(\log n)\) arithmetic operations to a general real exponentiation and multiply by \(N\) terms. The usual repeated-squaring argument does not directly justify that cost for a real exponent; a precision and log/exp evaluation model is needed. More fundamentally, the paper's own telescoping identity gives the exact finite identity \(x_1+\sum_{n=1}^{N-1}D_n=x_N\): approximating by the endpoint does not require evaluating \(N\) differences. This does not show that the displayed bound is impossible for an explicitly chosen naive summation algorithm; it shows that it is **not an intrinsic computational-cost requirement of this construction**. Separate index size from number of evaluations and arithmetic/bit complexity.

No extraction-induced indentation or line-wrapping defects in the PDF's code listing have been treated as mathematical errors.

## The A3 constants and eq (4)

The coefficient of \(t^4\) in the base logarithm is independently obtained from
\[
\log(1+a_1t+a_2t^2)
=a_1t+(a_2-a_1^2/2)t^2+(a_1^3/3-a_1a_2)t^3
+(-a_2^2/2+a_1^2a_2-a_1^4/4)t^4+O(t^5).
\]
Multiplication by \(\beta/t+\gamma\) gives the corrected \(A_3\) above.

There are **three distinct algebraic quantities**, not two:

| Quantity | Branch I | Branch II |
|---|---|---|
| Actual coefficient from the logarithm | \(c(2\sqrt3-3)/72\) | \(-c(3+2\sqrt3)/72\) |
| Substitution into the paper's printed (4) | \(c(9-4\sqrt3)/18\) | \(c(9+4\sqrt3)/18\) |
| Paper's claimed result, lines 344–346 | \(c(9-5\sqrt3)/36\) | \(c(9+5\sqrt3)/36\) |

Consequently, fixing only equation (4) or only its subsequent simplification is insufficient: **both are wrong independently**. The factor 4 is a third separate error.

For \(c>0\), branch I is eventually above \(e^c\) and decreasing, while branch II is eventually below \(e^c\) and increasing. The signs reverse for \(c<0\). The branch-I smaller-magnitude labeling at lines 214–218 is asymptotically **correct**, since
\[
0<2\sqrt3-3<3+2\sqrt3.
\]
Both branches have the same order; “faster” here means the smaller leading constant, not a higher power of \(n^{-1}\).

## The classical baseline (Prop 3.1)

From the independently computed expansion
\[
\log x_n=ab-\frac{a^2b}{2n}+\frac{a^3b}{3n^2}+O(n^{-3}),
\]
we obtain
\[
x_n=e^{ab}\left(1-\frac{a^2b}{2n}+O(n^{-2})\right),
\quad D_n=\frac{e^{ab}a^2b}{2n^2}+O(n^{-3}),
\]
where the difference estimate is justified by the analytic expansion to further orders.

Independent numerical tests:

| (a,b) | \(n^2D_n\), n=1,000,000 | correct limit | paper's limit |
|---|---:|---:|---:|
| (1,1) | 1.35913706333893 | 1.35914091422952 | 0 |
| (2,2) | 218.390925798263 | 218.392600132577 | 0 |
| (1,2) | 7.38903146880646 | 7.38905609893065 | −7.38905609893065 |
| (2,1) | 14.7780284555802 | 14.7781121978613 | 7.38905609893065 |
| (−1,2) | 0.135335193013158 | 0.135335283236613 | 0.406005849709838 |
| (0,2) | 0 | 0 | 0 |
| (2,0) | 0 | 0 | 0 |

Thus Euler's sequence \(a=b=1\) decisively falsifies the proposed cancellation. For fixed real parameters, using the eventually positive base,
\[
\boxed{D_n=O(n^{-3})\ \Longleftrightarrow\ a=0\ \text{or}\ b=0.}
\]
Those cases are constant sequences. If both parameters are nonzero, the difference order is exactly \(n^{-2}\).

The limit \(x_n\to e^{ab}\) in Proposition 3.1 is **correct**. Its unrestricted real-parameter formulation should mean sufficiently large \(n\), since an arbitrary negative \(a\) does not give positive bases for all initial indices.

**Consequence for Table 3, lines 428–433:** for \((1+c/n)^{cn}\), the limit is \(e^{c^2}\), not generally \(e^c\), and for \(c\ne0\) the difference/error orders are \(\Theta(n^{-2})\)/\(\Theta(N^{-1})\), not \(\Theta(n^{-3})\)/\(\Theta(N^{-2})\). The required index scales as \(\varepsilon^{-1}\), not \(\varepsilon^{-1/2}\), for fixed nonzero \(c\). At \(c=1\), its alleged distinct second row is literally the first row's Euler sequence. The Euler and corrected order-3 rows themselves have the correct exponents.

## Tables vs stated formulas

Independent Table 1 reproduction at \(c=1\), 150-digit working precision (values rounded here to 12 significant figures):

| n | \(|x_n^{(I)}-e|\) | \(|D_n^{(I)}|\) | \(|x_n^{(II)}-e|\) | \(|D_n^{(II)}|\) |
|---:|---:|---:|---:|---:|
| 100 | 1.73603167491e−8 | 5.09023915700e−10 | 2.40974810718e−7 | 7.05787501431e−9 |
| 500 | 1.39913735849e−10 | 8.35621476272e−13 | 1.94740150320e−9 | 1.16280099868e−11 |
| 1,000 | 1.75054242095e−11 | 5.23952617720e−14 | 2.43734791386e−10 | 7.29435660780e−13 |
| 5,000 | 1.40147241801e−13 | 8.40495299880e−17 | 1.95186407454e−12 | 1.17055085040e−15 |

The paper's formulas would instead predict these leading magnitudes:

| Leading magnitude, c=1 | Correct | Printed A3 plus printed factor |
|---|---:|---:|
| \(n^3|x_n^{(I)}-e|\) | 0.0175216525970479 | 0.0256534798672205 |
| \(n^3|x_n^{(II)}-e|\) | 0.244045138301968 | 1.33348743436230 |
| \(n^4|D_n^{(I)}|\) | 0.0525649577911438 | 0.102613919468882 |
| \(n^4|D_n^{(II)}|\) | 0.732135414905905 | 5.33394973744921 |

**Answer to the text-versus-tables question:** the sequence definitions, appendix branch functions, and tabulated numerical magnitudes agree with the corrected \(A_3\) and factor **3**. The theorem's stated constants/factor are wrong. Absolute-value tables conceal the additional sign error in branch II.

Independent Table 2 reproduction:

| c | n | \(|x_n^{(I)}-e^c|\) | \(|D_n^{(I)}|\) | \(|D_n^{(II)}|\) |
|---:|---:|---:|---:|---:|
| 2 | 1,000 | 9.51693530568e−11 | 2.84850175946e−13 | 3.96562340310e−12 |
| 2 | 5,000 | 7.61919401394e−13 | 4.56940620114e−16 | 6.36377421185e−15 |
| −1 | 1,000 | 2.36910154356e−12 | 7.09092759208e−15 | 9.87183817722e−14 |
| −1 | 5,000 | 1.89668666640e−14 | 1.13748669468e−17 | 1.58416830882e−16 |

These all agree with the paper after rounding to three significant figures.

## What I checked and found sound

- Positivity of both bases for every integer \(n\ge1\), and hence real-valuedness.
- The telescoping identities and their endpoint indexing.
- Lemma 1.2, including \(K/k\), remainder order, and signed leading term.
- Equations (1)–(3), the normalized cancellation equations, and both exact branch parameter choices.
- The limits \(e^c\), difference order 4, and error order 3 for both branches whenever \(c\ne0\).
- Nonvanishing of the **corrected** \(A_3\) for \(c\ne0\).
- Branch I's smaller asymptotic magnitude.
- Table 1 apart from the single rounding error; all of Table 2 at printed precision.
- Appendix A's branch-function definitions and the validity of regression as a numerical order diagnostic, although its reported fit is inconsistent with its stated grid.
- The Euler and order-3 exponents in Table 3, excluding its false middle row.
- The reality and relevance of the probabilistic Richardson work and the Corless article.

## Recommended repairs

1. **Replace equation (4)** with the correct logarithmic coefficient. Replace all occurrences of the branch \(A_3\) constants, including the abstract, theorem, Section 4.3, proof, and any conclusions about signs.
2. **Replace the multiplier 4 by 3** throughout the order-3 difference asymptotics and magnitude constants. State the signed leading errors explicitly; branch II has the opposite sign to branch I for fixed nonzero \(c\).
3. **Repair Lemma 2.3's hypotheses/proof**, for example by requiring one additional explicit asymptotic coefficient with the stated remainder, and explain why the present analytic families satisfy this. Do not difference a bare big-O remainder as though it were smooth.
4. **Correct the design-principle indexing:** cancel through \(A_{k-1}\), leave \(A_k\ne0\) for order \(k\).
5. **Replace Proposition 3.1 and Section 1.5's classical cancellation claim.** Correct Table 3's middle row, including its target and error/index scaling. Supply an actual derivation rather than the invalid reference [2].
6. **Distinguish signed asymptotics from absolute Theta bounds** when claiming exact tail rates. The general O bound is sound; an exact Theta tail needs further sign/asymptotic information.
7. **Exclude \(c=0\) in the abstract's nontrivial-order claims**, while mentioning the trivial constant case separately if desired.
8. **Regenerate the regression summaries from the published grid** and correct Table 1's \(8.41e-17\) to \(8.40e-17\). Retain the other table entries: they already reflect the actual sequences.
9. **Repair the bibliography:** substantiate or remove [2]; fix [16]'s author list, journal, and article number; fix [13–14]'s author ordering and distinguish online-first from issue year. Do not infer wholesale bibliographic validity from the existence of some genuine references.
10. **Qualify the computational-cost discussion** with an explicit evaluation model and distinguish computing a single endpoint from naively summing all telescoping differences.

**Bottom line:** the useful construction survives independent verification, but the paper in its current form does not establish its claimed explicit constants or its classical comparison. A corrected theorem and repaired supporting lemmas are necessary before acceptance.
