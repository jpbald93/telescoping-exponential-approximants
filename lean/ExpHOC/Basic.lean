import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.Order.Ring.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# Exact algebraic core of *Higher-Order Cancellation in Exponential Approximants*

The paper's log-expansion coefficients (its equations (1)-(4)) are explicit
polynomials in `(a1, a2, beta, gamma)`.  We formalise those polynomials and
verify, over `ℝ` with `s = Real.sqrt 3`, the two-branch closed forms for the
coefficient `A3` and the subleading `A4`, together with nonvanishing and sign.

Scope: this file covers the *exact algebraic core* (the branch constants).  The
derivation of equations (1)-(4) from the Taylor series of `log (1 + x)`, and all
asymptotic content (the limit `e^c`, the finite-difference multiplier `-3 e^c`,
the `Theta` rates), lie outside this file; they are checked by the symbolic /
numerical driver shipped with the paper (`code/verify_hoc.py`).
-/

namespace HOC
noncomputable section

/-- Eq. (1): constant term `a1 * beta`. -/
def c0 (a1 a2 b g : ℝ) : ℝ := a1 * b

/-- Eq. (2): coefficient of `1/n`. -/
def A1 (a1 a2 b g : ℝ) : ℝ := a1 * g + b * a2 - a1 ^ 2 * b / 2

/-- Eq. (3): coefficient of `1/n^2`. -/
def A2 (a1 a2 b g : ℝ) : ℝ := g * a2 - a1 ^ 2 * g / 2 + a1 ^ 3 * b / 3 - a1 * a2 * b

/-- Eq. (4): coefficient of `1/n^3` (corrected form). -/
def A3 (a1 a2 b g : ℝ) : ℝ :=
  g * (a1 ^ 3 / 3 - a1 * a2) + b * (a1 ^ 2 * a2 - a1 ^ 4 / 4 - a2 ^ 2 / 2)

/-- Coefficient of `1/n^4` (subleading correction). -/
def A4 (a1 a2 b g : ℝ) : ℝ :=
  g * (a1 ^ 2 * a2 - a1 ^ 4 / 4 - a2 ^ 2 / 2) + b * (a1 ^ 5 / 5 - a1 ^ 3 * a2 + a1 * a2 ^ 2)

/-- `(Real.sqrt 3)^2 = 3`. -/
theorem sqrt3_sq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)

/-- `3/2 < Real.sqrt 3`. -/
theorem sqrt3_gt : (3 : ℝ) / 2 < Real.sqrt 3 :=
  (Real.lt_sqrt (by norm_num)).mpr (by norm_num)

/-- Branch I cancels `A1`. -/
theorem branch_I_A1 (c : ℝ) :
    A1 1 (Real.sqrt 3 / 6) c (c * (1 / 2 - Real.sqrt 3 / 6)) = 0 := by
  simp only [A1]; ring

/-- Branch II cancels `A1`. -/
theorem branch_II_A1 (c : ℝ) :
    A1 1 (-Real.sqrt 3 / 6) c (c * (1 / 2 + Real.sqrt 3 / 6)) = 0 := by
  simp only [A1]; ring

/-- Branch I cancels `A2`. -/
theorem branch_I_A2 (c : ℝ) :
    A2 1 (Real.sqrt 3 / 6) c (c * (1 / 2 - Real.sqrt 3 / 6)) = 0 := by
  have h : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [A2]
  linear_combination (-(c / 36)) * h

/-- Branch II cancels `A2`. -/
theorem branch_II_A2 (c : ℝ) :
    A2 1 (-Real.sqrt 3 / 6) c (c * (1 / 2 + Real.sqrt 3 / 6)) = 0 := by
  have h : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [A2]
  linear_combination (-(c / 36)) * h

/-- Branch I leading coefficient. -/
theorem branch_I_A3 (c : ℝ) :
    A3 1 (Real.sqrt 3 / 6) c (c * (1 / 2 - Real.sqrt 3 / 6)) = c * (2 * Real.sqrt 3 - 3) / 72 := by
  have h : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [A3]
  linear_combination (c / 72) * h

/-- Branch II leading coefficient. -/
theorem branch_II_A3 (c : ℝ) :
    A3 1 (-Real.sqrt 3 / 6) c (c * (1 / 2 + Real.sqrt 3 / 6)) = -(c * (3 + 2 * Real.sqrt 3) / 72) := by
  have h : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [A3]
  linear_combination (c / 72) * h

/-- Branch I subleading coefficient. -/
theorem branch_I_A4 (c : ℝ) :
    A4 1 (Real.sqrt 3 / 6) c (c * (1 / 2 - Real.sqrt 3 / 6)) = c * (39 - 25 * Real.sqrt 3) / 720 := by
  have h : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [A4]
  linear_combination (c * (Real.sqrt 3 - 3) / 432) * h

/-- Branch II subleading coefficient. -/
theorem branch_II_A4 (c : ℝ) :
    A4 1 (-Real.sqrt 3 / 6) c (c * (1 / 2 + Real.sqrt 3 / 6)) = c * (39 + 25 * Real.sqrt 3) / 720 := by
  have h : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [A4]
  linear_combination (-(c * (Real.sqrt 3 + 3)) / 432) * h

/-- Branch I leading coefficient is nonzero for `c ≠ 0`. -/
theorem branch_I_A3_ne_zero {c : ℝ} (hc : c ≠ 0) :
    A3 1 (Real.sqrt 3 / 6) c (c * (1 / 2 - Real.sqrt 3 / 6)) ≠ 0 := by
  rw [branch_I_A3]
  have h2 : 2 * Real.sqrt 3 - 3 ≠ 0 := by
    have := sqrt3_gt; linarith
  exact div_ne_zero (mul_ne_zero hc h2) (by norm_num)

/-- Branch II leading coefficient is nonzero for `c ≠ 0`. -/
theorem branch_II_A3_ne_zero {c : ℝ} (hc : c ≠ 0) :
    A3 1 (-Real.sqrt 3 / 6) c (c * (1 / 2 + Real.sqrt 3 / 6)) ≠ 0 := by
  rw [branch_II_A3]
  have h2 : 3 + 2 * Real.sqrt 3 ≠ 0 := by
    have := sqrt3_gt; linarith
  intro h
  exact (div_ne_zero (mul_ne_zero hc h2) (by norm_num)) (neg_eq_zero.mp h)

/-- For `c > 0` the two branches have opposite leading-error signs. -/
theorem branch_signs {c : ℝ} (hc : 0 < c) :
    0 < A3 1 (Real.sqrt 3 / 6) c (c * (1 / 2 - Real.sqrt 3 / 6))
    ∧ A3 1 (-Real.sqrt 3 / 6) c (c * (1 / 2 + Real.sqrt 3 / 6)) < 0 := by
  have h := sqrt3_gt
  constructor
  · rw [branch_I_A3]
    have h2 : 0 < 2 * Real.sqrt 3 - 3 := by linarith
    exact div_pos (mul_pos hc h2) (by norm_num)
  · rw [branch_II_A3]
    have h2 : 0 < 3 + 2 * Real.sqrt 3 := by linarith
    exact neg_neg_of_pos (div_pos (mul_pos hc h2) (by norm_num))

end
end HOC
