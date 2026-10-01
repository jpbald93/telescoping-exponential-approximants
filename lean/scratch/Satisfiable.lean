import ExpHOC

/-! Satisfiability certificates (outside the library; not imported by it).
For every theorem with hypotheses: a Lean-checked example showing those hypotheses can all be met
simultaneously by concrete values. Theorems whose conclusion is `False` assert that their hypotheses
are jointly impossible; for those we certify that every hypothesis but the last is satisfiable,
so the impossibility is not caused by a trivially inconsistent subset. -/

set_option linter.unusedVariables false
set_option linter.unnecessarySeqFocus false
set_option linter.style.longLine false

-- hypotheses of HOC.branch_I_A3_ne_zero are satisfiable
example : ∃ (c : ℝ) (hc : c ≠ 0), True :=
  ⟨1, by norm_num, trivial⟩

-- hypotheses of HOC.branch_II_A3_ne_zero are satisfiable
example : ∃ (c : ℝ) (hc : c ≠ 0), True :=
  ⟨1, by norm_num, trivial⟩

-- hypotheses of HOC.branch_signs are satisfiable
example : ∃ (c : ℝ) (hc : 0 < c), True :=
  ⟨1, by norm_num, trivial⟩
