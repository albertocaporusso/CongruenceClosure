(set-info :smt-lib-version 2.6)
(set-logic QF_UF)
(set-info :category "crafted")
(set-info :status sat)
(declare-sort S1 0)
(declare-fun a () S1)
(declare-fun f (S1) S1)
(assert (let ((f1 (f a)) (f2 (f f1)) (f3 (f f2)) ) (and (not (= f1 a)) (= f2 a) (= f3 f1) ) ))
(check-sat)
(exit)