#!/usr/bin/env python3
"""V5 verification driver for
'Higher-Order Cancellation in Exponential Approximants: An Explicit O(n^-4)
 Telescoping Family' (Josh Bald).

Every numeral quoted in the V5 manuscript is regenerated here, and every
claimed sign / constant is ASSERTED (check() fails loudly), so a reversed
direction or a wrong constant crashes the driver rather than printing as prose.

Tiers: [sym] exact symbolic (sympy); [num] high-precision numeric (mpmath).
"""
import sys
import sympy as sp
import mpmath as mp

FAILS = []
def check(cond, msg):
    ok = bool(cond)
    print(("  [ok ] " if ok else "  [FAIL] ") + msg)
    if not ok:
        FAILS.append(msg)

print("=" * 72)
print("PART 1  [sym] log-expansion coefficients of (beta n + gamma) log(1 + a1/n + a2/n^2)")
print("=" * 72)
t = sp.symbols('t', positive=True)
a1, a2, b, g, c = sp.symbols('a1 a2 beta gamma c')
s3 = sp.sqrt(3)
u = a1*t + a2*t**2
logx = sp.expand((b/t + g)*sp.series(sp.log(1 + u), t, 0, 8).removeO())
c0 = sp.simplify(logx.coeff(t, 0))
A1 = sp.simplify(logx.coeff(t, 1))
A2 = sp.simplify(logx.coeff(t, 2))
A3 = sp.simplify(sp.expand(logx.coeff(t, 3)))
A4 = sp.simplify(sp.expand(logx.coeff(t, 4)))
print("  c0 =", c0)
print("  A1 =", sp.expand(A1))
print("  A2 =", sp.expand(A2))
print("  A3 =", sp.expand(A3))
print("  A4 =", sp.expand(A4))
check(sp.simplify(c0 - a1*b) == 0, "eq(1) c0 = a1*beta")
check(sp.simplify(A1 - (a1*g + b*a2 - a1**2*b/2)) == 0, "eq(2) A1")
check(sp.simplify(A2 - (g*a2 - a1**2*g/2 + a1**3*b/3 - a1*a2*b)) == 0, "eq(3) A2")
check(sp.simplify(A3 - (g*(a1**3/3 - a1*a2) + b*(a1**2*a2 - a1**4/4 - a2**2/2))) == 0,
      "eq(4) A3 (CORRECTED form)")
check(sp.simplify(A4 - (g*(a1**2*a2 - a1**4/4 - a2**2/2) + b*(a1**5/5 - a1**3*a2 + a1*a2**2))) == 0,
      "eq(4b) general A4 (printed form) matches the expansion")

print()
print("=" * 72)
print("PART 2  [sym] branches: a1=1, beta=c, a2=+/-sqrt3/6, gamma=c(1/2 -/+ sqrt3/6)")
print("=" * 72)
branch = {"I": (s3/6, c*(sp.Rational(1,2) - s3/6)),
          "II": (-s3/6, c*(sp.Rational(1,2) + s3/6))}
A3v, A4v = {}, {}
for name, (a2v, gv) in branch.items():
    sub = {a1: 1, b: c, a2: a2v, g: gv}
    check(sp.simplify(A1.subs(sub)) == 0, f"branch {name}: A1 = 0")
    check(sp.simplify(A2.subs(sub)) == 0, f"branch {name}: A2 = 0")
    A3v[name] = sp.simplify(A3.subs(sub)); A4v[name] = sp.simplify(A4.subs(sub))
    print(f"    branch {name}: A3 = {A3v[name]}   A4 = {A4v[name]}")
check(sp.simplify(A3v["I"] - c*(2*s3 - 3)/72) == 0, "A3^(I) = c(2sqrt3-3)/72")
check(sp.simplify(A3v["II"] - (-c*(3 + 2*s3)/72)) == 0, "A3^(II) = -c(3+2sqrt3)/72")
check(sp.simplify(A4v["I"] - c*(39 - 25*s3)/720) == 0, "A4^(I) = c(39-25sqrt3)/720")
check(sp.simplify(A4v["II"] - c*(39 + 25*s3)/720) == 0, "A4^(II) = c(39+25sqrt3)/720")
print(f"    numeric c=1:  A3_I = {float(A3v['I'].subs(c,1)):.10f}   A3_II = {float(A3v['II'].subs(c,1)):.10f}")
check(float(A3v["I"].subs(c,1)) > 0 and float(A3v["II"].subs(c,1)) < 0,
      "for c>0 branch I and II have OPPOSITE leading-error signs")

print()
print("=" * 72)
print("PART 3  [num] the families, the limit, and the difference/error asymptotics")
print("=" * 72)
mp.mp.dps = 150
M3 = mp.sqrt(3)
def xI(n, cc):
    n = mp.mpf(n); return mp.power(1 + 1/n + M3/(6*n**2), cc*n + cc*(mp.mpf(1)/2 - M3/6))
def xII(n, cc):
    n = mp.mpf(n); return mp.power(1 + 1/n - M3/(6*n**2), cc*n + cc*(mp.mpf(1)/2 + M3/6))
XF = {"I": xI, "II": xII}
A3n = {k: float(v.subs(c, 1)) for k, v in A3v.items()}

for cc in [mp.mpf(1)]:
    for k, f in XF.items():
        check(mp.fabs(f(10**7, cc) - mp.e**cc) < mp.mpf('1e-21'), f"lim x_n^({k}) = e^c (c=1), error ~ n^-3")
# c = 0 is the trivial exception
check(xI(10**6, mp.mpf(0)) == 1 and xII(10**6, mp.mpf(0)) == 1, "c=0: both sequences are identically 1")
check((xI(10**6+1, mp.mpf(0)) - xI(10**6, mp.mpf(0))) == 0, "c=0: D_n = 0 (Theta claims excluded)")

for k, f in XF.items():
    n = 300000
    D = f(n+1, mp.mpf(1)) - f(n, mp.mpf(1))
    lim = -3*mp.e*A3n[k]                       # predicted n^4 D_n
    got = D*n**4
    check(mp.fabs(got - lim) < mp.mpf('1e-4'), f"n^4 D_n^({k}) -> -3 e^c A3 = {mp.nstr(lim,10)}  (got {mp.nstr(got,10)})")
    check((got > 0) == (A3n[k] < 0), f"sign of n^4 D_n^({k}) matches -sign(A3)")
    E = f(n, mp.mpf(1)) - mp.e
    check(mp.fabs(E*n**3 - mp.e*A3n[k]) < mp.mpf('1e-3'), f"n^3 (x_n^({k})-e^c) -> e^c A3 = {mp.nstr(mp.e*A3n[k],10)}")
    check((E > 0) == (A3n[k] > 0), f"sign of x_n^({k})-e^c matches sign(A3)")

print()
print("=" * 72)
print("PART 4  [num] Table 1 (c=1) and Table 2 (c=2,-1), 3 s.f.")
print("=" * 72)
def sf(v, d=3):
    return mp.nstr(v, d)
print("  Table 1 (c=1):   n   |xI-e|   |DI|   |xII-e|   |DII|")
T1 = {}
for n in [100, 500, 1000, 5000]:
    row = (mp.fabs(xI(n,mp.mpf(1))-mp.e), mp.fabs(xI(n+1,mp.mpf(1))-xI(n,mp.mpf(1))),
           mp.fabs(xII(n,mp.mpf(1))-mp.e), mp.fabs(xII(n+1,mp.mpf(1))-xII(n,mp.mpf(1))))
    T1[n] = row
    print(f"      {n:>5}  {sf(row[0])}  {sf(row[1])}  {sf(row[2])}  {sf(row[3])}")
check(sf(T1[5000][1]) == '8.4e-17' or sf(T1[5000][1]).startswith('8.40'),
      f"Table1 n=5000 |D_I| rounds to 8.40e-17 (got {sf(T1[5000][1])})")
print("  Table 2:")
for cc in [mp.mpf(2), mp.mpf(-1)]:
    for n in [1000, 5000]:
        print(f"      c={int(cc):>2}  n={n:>5}  |xI-e^c|={sf(mp.fabs(xI(n,cc)-mp.e**cc))}"
              f"  |DI|={sf(mp.fabs(xI(n+1,cc)-xI(n,cc)))}  |DII|={sf(mp.fabs(xII(n+1,cc)-xII(n,cc)))}")

# assert every tabulated value against the manuscript (3 s.f., rel tol 0.5%)
def rounds_to(v, s):
    return mp.nstr(v, 3) == mp.nstr(mp.mpf(s), 3)

# assert every tabulated value ROUNDS to the manuscript's printed 3-s.f. string
EXP1 = {100:('1.74e-8','5.09e-10','2.41e-7','7.06e-9'),
        500:('1.40e-10','8.36e-13','1.95e-9','1.16e-11'),
        1000:('1.75e-11','5.24e-14','2.44e-10','7.29e-13'),
        5000:('1.40e-13','8.40e-17','1.95e-12','1.17e-15')}
for n, exp in EXP1.items():
    for got, s in zip(T1[n], exp):
        check(rounds_to(got, s), f"Table1 n={n}: {mp.nstr(got,3)} == {s}")
EXP2 = {(2,1000):('9.52e-11','2.85e-13','3.97e-12'), (2,5000):('7.62e-13','4.57e-16','6.36e-15'),
        (-1,1000):('2.37e-12','7.09e-15','9.87e-14'), (-1,5000):('1.90e-14','1.14e-17','1.58e-16')}
for (cc, n), exp in EXP2.items():
    got = (mp.fabs(xI(n,mp.mpf(cc))-mp.e**cc), mp.fabs(xI(n+1,mp.mpf(cc))-xI(n,mp.mpf(cc))),
           mp.fabs(xII(n+1,mp.mpf(cc))-xII(n,mp.mpf(cc))))
    for g, s in zip(got, exp):
        check(rounds_to(g, s), f"Table2 c={cc} n={n}: {mp.nstr(g,3)} == {s}")

print()
print("=" * 72)
print("PART 5  [num] log-log regression over the appendix grid n=100..10000 step 25")
print("=" * 72)
def fit(f):
    ns = list(range(100, 10001, 25))
    xs = [mp.log(n) for n in ns]; ys = [mp.log(mp.fabs(f(n+1,1)-f(n,1))) for n in ns]
    m = len(ns); mx = mp.fsum(xs)/m; my = mp.fsum(ys)/m
    a = mp.fsum((xs[i]-mx)*(ys[i]-my) for i in range(m))/mp.fsum((xs[i]-mx)**2 for i in range(m))
    b0 = my - a*mx
    sst = mp.fsum((ys[i]-my)**2 for i in range(m))
    ssr = mp.fsum((ys[i]-(a*xs[i]+b0))**2 for i in range(m))
    return a, b0, 1 - ssr/sst
EXP5 = {"I": (-3.9973, -2.9696, 0.9999997), "II": (-3.9969, -0.3391, 0.9999996)}
for k, f in XF.items():
    a, bb, r2 = fit(f)
    print(f"    branch {k}: slope={mp.nstr(a,8)}  intercept={mp.nstr(bb,8)}  R2={mp.nstr(r2,8)}")
    check(abs(float(a) + 4) < 0.01, f"branch {k}: slope consistent with -4")
    check(abs(float(a)-EXP5[k][0]) < 5e-4 and abs(float(bb)-EXP5[k][1]) < 5e-4,
          f"branch {k}: slope/intercept match the manuscript {EXP5[k][:2]}")
    check(abs(float(r2)-EXP5[k][2]) < 1e-7, f"branch {k}: R^2 matches the printed value {EXP5[k][2]}")

print()
print("=" * 72)
print("PART 6  [num] classical baseline:  x_n=(1+a/n)^(bn),  D_n ~ e^{ab} a^2 b/(2n^2)")
print("=" * 72)
def xab(a, bb, n):
    a = mp.mpf(a); bb = mp.mpf(bb); n = mp.mpf(n)
    return mp.power(1 + a/n, bb*n)
for (a, bb) in [(1,1),(1,2),(2,1),(2,3),(3,5),(-1,2)]:
    n = 10**6
    D = xab(a,bb,n+1) - xab(a,bb,n)
    got = D*n**2/mp.e**(mp.mpf(a)*mp.mpf(bb))
    want = mp.mpf(a)**2*mp.mpf(bb)/2
    check(mp.fabs(got-want) < mp.mpf('1e-3'), f"(a,b)=({a},{bb}): n^2 D_n/e^ab -> a^2 b/2 = {mp.nstr(want,8)} (got {mp.nstr(got,8)})")
# a=b=1 (Euler): NOT O(n^-3)
D = xab(1,1,10**6+1) - xab(1,1,10**6)
check(mp.fabs(D*(10**6)**2/mp.e - mp.mpf('0.5')) < mp.mpf('1e-4'),
      "Euler a=b=1: n^2 D_n/e -> 1/2  (Theta(n^-2), NOT O(n^-3))")

print()
print("=" * 72)
if FAILS:
    print(f"RESULT: {len(FAILS)} FAILURE(S): {FAILS}")
    sys.exit(1)
print("RESULT: ALL ASSERTIONS PASS")
print("=" * 72)
