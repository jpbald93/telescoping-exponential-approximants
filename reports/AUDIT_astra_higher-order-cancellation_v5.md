# Higher-Order Cancellation (V5) — adversarial audit

## Verdict

**The principal order-3 theorem and the advertised V4-to-V5 corrections to A3, its branch constants, the finite-difference multiplier, the classical baseline, and Lemma 2.3 are mathematically correct. All entries in Tables 1–2 and both fitted regressions reproduce. However, V5 is not error-free: the printed general A4 formula has its entire gamma contribution negated.** Its separately printed branch A4 constants are nevertheless correct. Thus the text's assertion that these constants follow by substituting into the displayed general formula is false as printed.

The verification driver prints `ALL ASSERTIONS PASS`, but **does not assert the printed general A4 identity**. Its correct internally computed A4 and correct branch checks conceal this manuscript/driver discrepancy. This is a substantive, localized algebraic and verification defect, not a counterexample to the main theorem.

Additional supported findings: a small domain mismatch in the design-principle invocation of Lemma 2.3 at order 1; an unjustified computational-cost discussion; and two definite bibliographic inaccuracies (the arXiv Richardson author order and the title attached to the Princeton reference). Table 3 and its introductory prose need explicit parameter/sign qualifications. No checked reference was established to be fabricated.

**Recommendation:** repair the general A4 formula and verification coverage before accepting the revision; make the smaller qualifications and bibliographic repairs listed below. There is no need to abandon or change the two branch constructions.

### Independent evidence

I read the complete LaTeX and the supplied driver, wrote a separate SymPy/mpmath program, and ran both programs. My numerical calculations use 150 decimal digits and `log1p`/`expm1`, not the supplied driver's direct-power implementation. I compared every table entry at the displayed three-significant-figure precision and recomputed the regressions including R².

Files saved alongside this report:

- `astra_hoc_v5_independent.py` — independent symbolic, numerical, counterexample, and table-rounding checks.
- `astra_hoc_v5_independent_output.txt` — complete results.
- `astra_hoc_v5_supplied_driver_output.txt` — fresh run of the supplied driver.

Locations below use source line numbers and LaTeX labels, avoiding ambiguity between the question's equation numbering and the source's automatically generated numbering.

## Claim-by-claim (with your own computation)

| Requested item | Finding |
|---|---|
| 1. General expansion c0, A1, A2, A3 | **CORRECT.** Independent coefficient differences simplify identically to zero. |
| 1. General A4 as printed | **INCORRECT.** Reverse all three signs in its gamma parenthesis; details below. |
| 2. Both branch cancellations and A3 constants | **CORRECT.** A1=A2=0 identically; A3 values match exactly. |
| 2. Branch A4 constants | **CORRECT**, but do not follow from the incorrect printed general A4. |
| 3. Main theorem, D_n ~ -3 exp(c) A3 n^-4 | **CORRECT** for every fixed real c≠0; independent high-precision limits agree. |
| 4. Revised Lemma 2.3 | **CORRECT and sufficient.** The explicit next coefficient fixes the former problem; its extra condition on the final remainder is redundant. |
| 5. Classical baseline and iff statement | **CORRECT**, on the stated eventually positive-base domain. |
| 6. Table 3 middle row | **CORRECT for fixed c≠0**, with target exp(c²), not exp(c). Add that restriction to the table/caption. |
| 7. Tables 1–2, including 8.40e-17 | **ALL CORRECT at displayed precision.** |
| 8. c=0 in abstract/main theorem | **CORRECTLY HANDLED.** The abstract identifies the constant sequence; the theorem explicitly excludes c=0. |
| 9. Design principle | **CORRECT in the analytic power-series class**, but the lemma as stated excludes the k=0 instance invoked for order 1. Easily repaired. Not a characterization of arbitrary sequences under Definition 2.1 alone. |
| 10. Corrected journal references | **Oates et al. and Yang–Tian journal entries verified.** Smaller errors remain elsewhere in the bibliography. |
| 11. New-error hunt | General A4 sign error; overstated driver coverage; cost-model problem; minor qualification/index/reference issues detailed below. |

### Main-theorem numerical check

For c=1, the exact predicted constants are

\[
K_I=-\frac{e(2\sqrt3-3)}{24}=-0.0525649577911438186\ldots,
\quad
K_{II}=\frac{e(3+2\sqrt3)}{24}=0.732135414905905127\ldots.
\]

Independent results:

| n | n⁴ D_I | n⁴ D_II |
|---:|---:|---:|
| 100 | -0.0509023915699937927 | 0.705787501431455399 |
| 1,000 | -0.0523952617719881572 | 0.729435660779543482 |
| 10,000 | -0.0525479531132690785 | 0.731864774128989707 |
| 1,000,000 | -0.0525647877057044114 | 0.732132707764448036 |
| predicted limit | -0.0525649577911438186 | 0.732135414905905127 |

The same checks for c=2 and c=-1 confirm the c exp(c) scaling and the sign reversal. At c=0 all computed errors and differences are exactly zero. Symbolically, positivity of both bases, analyticity near 1/n=0, and nonvanishing of A3 for c≠0 prove the theorem for all fixed real c, rather than merely the tested values.

The endpoint error is independently

\[
x_n-e^c=e^c A_3 n^{-3}+O(n^{-4}),
\]

so its Theta(n^-3) rate also follows without any potentially ambiguous unsigned-tail inference.

## The A3 constants and eq (4)

Put t=1/n. Independent expansion gives

\[
\begin{aligned}
\log(1+a_1t+a_2t^2)
={}&a_1t+(a_2-a_1^2/2)t^2+(a_1^3/3-a_1a_2)t^3\\
&+(-a_1^4/4+a_1^2a_2-a_2^2/2)t^4\\
&+(a_1^5/5-a_1^3a_2+a_1a_2^2)t^5+O(t^6).
\end{aligned}
\]

Multiplication by beta/t+gamma confirms the printed c0, A1, A2 and, in particular,

\[
\boxed{A_3=\gamma(a_1^3/3-a_1a_2)
+\beta(a_1^2a_2-a_1^4/4-a_2^2/2).}
\]

**The A3 correction is fully correct.** On a1=1, beta=c, gamma=c(1/2-a2), the second cancellation constraint becomes c(1/12-a2²)=0. Thus for c≠0 the two roots are ±sqrt(3)/6, and SymPy gives

\[
A_3^I=c(2\sqrt3-3)/72,\qquad
A_3^{II}=-c(3+2\sqrt3)/72.
\]

Both are nonzero for c≠0. The V5 remark's evaluation of the old incorrect A3 expression as c(9-4sqrt(3))/18 is also correct for branch I. At c=0 one must not divide by c in obtaining the two roots: the whole family is trivial when beta=gamma=0. This does not affect the theorem, whose assumption already excludes c=0.

### Substantive remaining defect: general A4

At source lines 367–368, `eq:A4`, the correct expression is

\[
\boxed{A_4=\gamma\left(-\frac{a_1^4}{4}+a_1^2a_2-\frac{a_2^2}{2}\right)
+\beta\left(\frac{a_1^5}{5}-a_1^3a_2+a_1a_2^2\right).}
\]

The manuscript prints the opposite sign on the entire gamma part. Exact symbolic subtraction yields

\[
A_4^{\rm actual}-A_4^{\rm printed}
=-\frac{\gamma}{2}(a_1^4-4a_1^2a_2+2a_2^2).
\]

An especially simple falsification is a1=beta=gamma=1, a2=0: `(n+1) log(1+1/n)` has A4=-1/20, whereas the printed expression gives 9/20.

The independently computed branch constants are precisely the manuscript's

\[
A_4^{I,II}=\frac{c(39\mp25\sqrt3)}{720}.
\]

But substituting the branches into the **printed** general A4 instead gives

\[
\frac{c(369\mp215\sqrt3)}{720}.
\]

Therefore lines 416–421 cannot be described as substitution into the displayed formula until that formula is repaired.

For clarity, the actual subleading difference expansion is

\[
D_n=e^c\left[-3A_3 n^{-4}+(6A_3-4A_4)n^{-5}\right]+O(n^{-6}),
\]

with

\[
6A_3^I-4A_4^I=c(-84+55\sqrt3)/180,
\quad
6A_3^{II}-4A_4^{II}=c(-84-55\sqrt3)/180.
\]

At c=1, the predicted n^-5 coefficients are 0.170085829997035291… and -2.70714886989214418…. Independent values of n⁵(D_n-K/n⁴) at n=10⁶ are 0.170085439407214012… and -2.70714145709160179…, respectively.

### Why the supplied driver misses this

The driver correctly derives A4 directly from the logarithmic series. It checks c0, A1, A2 and the printed A3, then proceeds to branch checks. **There is no assertion comparing that derived A4 with the manuscript's general A4 expression.** Its branch assertions compare the internally correct A4 with the correct branch constants, so they pass.

Accordingly, Appendix B's claim that the driver symbolically confirms `eq:c0` through `eq:A4` is false as printed. Claims that it asserts every numeral/constant are also too strong: most table entries are printed rather than checked against manuscript values, and the supplied driver's regression routine does not calculate R². My independent calculation confirms those values, but that does not make the stated test coverage accurate.

## The classical baseline

**Proposition 3.1 is correct.** Direct expansion gives

\[
\log x_n=ab-\frac{a^2b}{2n}+\frac{a^3b}{3n^2}+O(n^{-3}),
\]

and hence

\[
x_n=e^{ab}\left[1-\frac{a^2b}{2n}
+\left(\frac{a^3b}{3}+\frac{a^4b^2}{8}\right)n^{-2}+O(n^{-3})\right].
\]

Differencing gives e^(ab) a²b/(2n²)+O(n^-3). For real a,b this coefficient vanishes iff a=0 or b=0; in either case the sequence is 1 on its positive-base domain. The fact that a=b does not cancel anything is correctly repaired.

| (a,b) | n²D_n at n=10⁶ | predicted limit |
|---|---:|---:|
| (1,1) | 1.35913706333893014 | 1.35914091422952262 |
| (2,3) | 2420.54936223646287 | 2420.57276095641074 |
| (-2,1/2) | 0.367879686424770982 | 0.367879441171442322 |
| (1,-1) | -0.183939383363428913 | -0.183939720585721161 |
| (-1,-1) | -1.35914204684814039 | -1.35914091422952262 |
| (0,3), (2,0) | 0 | 0 |

For the middle row of Table 3, a=b=c gives limit e^(c²), leading difference coefficient e^(c²)c³/2, and endpoint error coefficient -e^(c²)c³/2. Thus its rates are correct for **fixed c≠0**. For c=0 both are zero, not Theta of the listed powers. For c<0 the base is positive only eventually, which Proposition 3.1 already states. No error in the asymptotic baseline remains.

The remark at lines 529–531 should say that an order-2 construction requires enlarging the classical two-parameter family (e.g. an affine exponent). No nonconstant member of `(1+a/n)^(bn)` can have order 2; the corrected proposition itself proves this. This is a wording/antecedent clarification, not a new failure of the proposition.

## Lemma 2.3

**The new hypothesis is sufficient, the conclusion is correct, and the old counterexample is excluded.**

Write the hypothesized logarithmic expansion as

\[
\log x_n=c+A n^{-(k+1)}+B n^{-(k+2)}+r_n,
\qquad r_n=O(n^{-(k+3)}).
\]

For k≥1, exponentiation actually gives the stronger intermediate result

\[
e^{-c}x_n=1+A n^{-(k+1)}+B n^{-(k+2)}+q_n,
\qquad q_n=O(n^{-(k+3)}),
\]

because 2k+2≥k+3. Every sequence q_n=O(n^(-k-3)) automatically satisfies Δq_n=O(n^(-k-3)) by the triangle inequality. Also Δ(Bn^(-k-2))=O(n^(-k-3)). Therefore the proof's R_n has exactly the claimed forward-difference bound, and the stated conclusion follows.

There is **no remaining hidden smoothness assumption** at this order. The extra sentence demanding Δr_n=O(n^(-k-3)) is redundant, not false: it follows already from the size bound on r_n. The proof would be clearer if it retained B for one more line instead of immediately absorbing it into an O-term, but its omitted justification is valid.

For the old counterexample

\[
x_n=\exp(n^{-3}+2(-1)^n n^{-4}),
\]

the relevant index is k=2. The proposed next coefficient would have to satisfy

\[
n^4(\log x_n-n^{-3})=2(-1)^n=B+O(n^{-1}),
\]

which is impossible for a fixed B. It is outside the revised hypotheses. Independently, n⁴D_n tends to -7 along even n and +1 along odd n (at n=100000 and 100001 I obtain -6.999860003… and 0.9999800012…). This confirms both the old failure mechanism and the effectiveness of the fix.

I also tested permissible oscillatory remainders `2(-1)^n n^(-k-3)` for k=1,2,3: they do not change the predicted leading limit, consistent with the proof.

### Design principle and the small index mismatch

For an analytic expansion at t=1/n=0, the first nonzero logarithmic coefficient A_k produces

\[
D_n=-k e^c A_k n^{-(k+1)}+O(n^{-(k+2)}).
\]

Thus the claimed coefficient-cancellation criterion is correct in this class, including its converse by considering the first nonzero coefficient. It is not an equivalence for all convergent sequences under Definition 2.1 alone: arbitrary sequences need not have such coefficients.

At source lines 308–314 the proof invokes Lemma 2.3 with its index k-1. For order k=1 this is index 0, whereas the lemma explicitly assumes index≥1. Proposition 3.1 also mentions the same out-of-range invocation, although it allows direct differencing as an alternative. **This is a minor formal gap, not a false order-1 claim.** Extend the lemma to k≥0: in that extra case exponentiation changes the next coefficient from B to B+A²/2, and the conclusion is still valid. Alternatively give the order-1 case separately.

### Tail qualifications

The signed tail lemma is correct, and the manuscript's warning about absolute Theta bounds is correct. Section 6.1 nevertheless returns to the shorthand “if D_n=Theta(n^(-k-1)) then |x_N-L|=Theta(N^-k)” without restating the sign/expansion assumption. Under the manuscript's definition of order through |D_n|, that general implication is not valid. Its own example `x_n=1+(-1)^n n^-4` disproves it: |D_n|~2n^-4, but the error is n^-4, not Theta(n^-3). My independent code confirms these scalings. Qualify this sentence by the signed asymptotic already established for the compared families. **The actual Table 3 families do satisfy the needed condition**, so their rates remain correct.

## Tables

**Every displayed value in Tables 1 and 2 rounds correctly to three significant figures.** Independently computed values (extra digits shown):

### Table 1

| n | abs(x_I−e) | abs(D_I) | abs(x_II−e) | abs(D_II) |
|---:|---:|---:|---:|---:|
| 100 | 1.73603167491e-8 | 5.09023915700e-10 | 2.40974810718e-7 | 7.05787501431e-9 |
| 500 | 1.39913735849e-10 | 8.35621476272e-13 | 1.94740150320e-9 | 1.16280099868e-11 |
| 1000 | 1.75054242095e-11 | 5.23952617720e-14 | 2.43734791386e-10 | 7.29435660780e-13 |
| 5000 | 1.40147241801e-13 | 8.40495299880e-17 | 1.95186407454e-12 | 1.17055085040e-15 |

In particular, **8.40495299880338836…e-17 rounds to 8.40e-17, not 8.41e-17.** V5 fixes this correctly.

### Table 2

| c | n | abs(x_I−e^c) | abs(D_I) | abs(D_II) |
|---:|---:|---:|---:|---:|
| 2 | 1000 | 9.51693530568e-11 | 2.84850175946e-13 | 3.96562340310e-12 |
| 2 | 5000 | 7.61919401394e-13 | 4.56940620114e-16 | 6.36377421185e-15 |
| -1 | 1000 | 2.36910154356e-12 | 7.09092759208e-15 | 9.87183817722e-14 |
| -1 | 5000 | 1.89668666640e-14 | 1.13748669468e-17 | 1.58416830882e-16 |

### Regression

On precisely n=100,125,…,10000, c=1:

| branch | slope | intercept | R² |
|---|---:|---:|---:|
| I | -3.9972880009272573 | -2.96963055421594662 | 0.999999724648502687 |
| II | -3.99690394394585583 | -0.339103739861715695 | 0.999999641776658553 |

All printed rounded values are correct. The supplied driver uses 60 decimal digits, and the embedded appendix script sets 170 rather than the prose's 150. My independent 150-digit run reproduces the reported values; the precision-description inconsistency has no effect on their validity.

### Other supported new-error-hunt finding: computational cost

Source lines 534–541 identify one arbitrary real exponentiation with O(log n) arithmetic operations and then attribute an additional factor N≈epsilon^(-1/3) to evaluating **one** endpoint. Neither is justified as written:

1. Repeated squaring supplies an O(log n) operation count for integer powers, not automatically for arbitrary real powers cn+gamma. A real-power cost model must account for exp/log or specify an algorithm.
2. Even accepting the manuscript's assumed per-endpoint cost O(log N M(p)), substituting N≈epsilon^(-1/3) gives O(log(epsilon^-1) M(p)), with no factor epsilon^(-1/3). That extra factor is the natural summation/evaluation-count factor for N terms, which the paragraph expressly says are not being computed.

Because big-O bounds can be deliberately loose, the displayed larger bound is not by itself a logically impossible upper bound. The substantiated defect is that the stated model/derivation does not justify it as the cost of one endpoint, and the underlying real-exponentiation cost is unspecified. Remove the claimed bit complexity or replace it with a clear algorithm and accuracy/precision model. This does not affect any convergence theorem.

## References

Checked against publisher metadata, arXiv, Crossref, DataCite, and institutional/reference sites. Access failures at some DOI landing pages were not treated as invalid DOIs; alternative authoritative metadata was used.

### Corrected entries that are verified

- **Oates, Karvonen, Teckentrup, Strocchi, Niederer, “Probabilistic Richardson extrapolation.” CORRECT.** [Crossref record](https://api.crossref.org/works/10.1093/jrsssb/qkae098) confirms JRSS-B **87(2), 457–479**, print year **2025**, DOI **10.1093/jrsssb/qkae098**, and online date **26 December 2024**. Author order in this journal entry is correct.
- **Yang–Tian, “An accurate approximation formula for gamma function.” CORRECT.** [PubMed Central article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5840229/) and its HTML citation metadata confirm **2018**, article/page **56**, authors **Zhen-Hang Yang and Jing-Feng Tian**, publication **6 March 2018**, DOI **10.1186/s13660-018-1646-6**. [arXiv:1712.08051](https://arxiv.org/abs/1712.08051) is the matching 2017 preprint.
- **Corless, Maple Transactions 3(1) (2023), DOI 10.5206/mt.v3i1.14777: verified** in [Crossref](https://api.crossref.org/works/10.5206/mt.v3i1.14777).
- **DLMF §3.9: verified** at [NIST](https://dlmf.nist.gov/3.9); its contents cover the cited sequence transformations.
- **Brent 1976: verified** against [Brent's publication list](https://maths-people.anu.edu.au/~brent/pub/pub034.html) and ACM metadata: J. ACM 23(2), 242–251.
- **Glaisher 1872, Adams 1878, Mitchell–Strain 1936:** the supplied titles/years/pages are corroborated by standard reference listings, Royal Society metadata, and JSTOR/MathWorld respectively. In particular Glaisher's 25–30, Adams's 88–94, and Mitchell–Strain's 476–496 are supported. No invalid historical entry established.

### Definite remaining bibliographic inaccuracies

1. **Richardson arXiv author order:** the manuscript lists “T. Karvonen, C. J. Oates, et al.” for arXiv:2401.07562. The [actual arXiv HTML](https://arxiv.org/html/2401.07562v1) begins **Chris J. Oates, Toni Karvonen, Aretha L. Teckentrup, Marina Strocchi, Steven A. Niederer**. Correct the author order. The paper and identifier are genuine.
2. **Princeton title mismatch:** `https://aofa.cs.princeton.edu/` is the companion site for **An Introduction to the Analysis of Algorithms**, by **Robert Sedgewick and Philippe Flajolet**, not a work titled *Analytic Combinatorics: Asymptotic Approximations*. Its relevant page is [Chapter 4, “Asymptotic Approximations”](https://aofa.cs.princeton.edu/40asymptotic/). Cite that chapter/booksite accurately, or cite the distinct *Analytic Combinatorics* book using its actual bibliographic details. This is a conflated citation, not evidence that the underlying resource is fabricated.

### Version-specific clarification, not fabrication

The Bald DOI **10.5281/zenodo.17605158** is valid. Its [current DataCite concept record](https://api.datacite.org/dois/10.5281/zenodo.17605158) has the cited title/author but publicationYear **2026**, issued 2026-09-21. The associated [version DOI 10.5281/zenodo.17605159](https://api.datacite.org/dois/10.5281/zenodo.17605159) has publicationYear **2025**. Thus the manuscript's 2025 date is defensible for the initial version, but the reference should pin that version or cite the current version with its date. I do **not** classify the entry as fabricated or the original 2025 dating as disproved.

## What is sound

- Both real-power bases are positive for every integer n≥1; the positivity proof is valid.
- The telescoping identities and their indexing are correct: sum over n≥N equals L-x_N; sum over n>N equals L-x_(N+1).
- The signed p-series tail calculation and its constant K/k are correct.
- The corrected general A3, both branch A3 values, their signs/nonvanishing, and the -3 finite-difference multiplier are correct.
- The branch A4 values are correct despite the erroneous general displayed formula.
- Analytic expansions justify the lemma's use for these families. The main theorem and Theta(N^-3) endpoint errors survive the A4 repair unchanged.
- The c≠0 restriction and c=0 constant-sequence explanation are correct in the abstract and theorem.
- The corrected classical baseline, including Euler's nonvanishing leading term, is correct.
- All table values and reported regressions reproduce independently.
- The specified corrected Oates and Yang–Tian journal references are genuine and accurate.

## Recommended repairs

1. **Required algebraic correction:** replace the gamma parenthesis in general A4 by `-a1^4/4 + a1^2*a2 - a2^2/2`. Keep the displayed branch A4 constants unchanged.
2. **Required verification correction:** add an assertion comparing the derived general A4 with that exact displayed expression. Add assertions for all quoted table/regression values, including R², or narrow the driver/Appendix B claims to its actual coverage. Ensure a failed assertion causes nonzero exit status; the current accumulated-failure reporting alone does not do that.
3. **Small formal repair:** extend Lemma 2.3 to index k≥0, retaining the B+A²/2 term when k=0, or prove the design-principle order-1 case separately. Retain the explicit next coefficient in every invocation.
4. **State qualifications locally:** mark Table 3's parameterized rows as fixed c≠0; retain eventual base positivity for the classical row; restrict the Section 6.1 Theta-tail inference to signed asymptotics/eventually one-signed families. Say explicitly that the order-2 alternative enlarges the classical family.
5. **Repair the cost discussion:** remove the unsupported real-power operation count and extra endpoint N factor, or supply an explicit computational model/algorithm. Do not present the loose larger big-O expression as a derived endpoint complexity.
6. **Repair the bibliography:** restore Oates-first author order in the arXiv entry; identify the Princeton chapter/booksite correctly; pin the intended Bald version/date.
7. Optional clarity: remove the redundant forward-difference condition on the final O(n^-k-3) logarithmic remainder and show the retained B term in the proof. Make the claimed numerical working precision consistent between prose and supplied code.

**Bottom line:** V5 fixes the principal earlier errors and its central construction is sound, but the still-wrong general A4 and the driver's failure to test that printed identity prevent an unqualified clean audit.
