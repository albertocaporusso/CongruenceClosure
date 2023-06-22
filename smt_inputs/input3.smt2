(set-info :smt-lib-version 2.6)
(set-logic QF_UF)
(set-info :category "crafted")
(set-info :status unsat)
(declare-sort S1 0)
(declare-fun f (S1) S1)
(declare-fun a () S1)
(assert (let ((t1 (f a )) (t2 (f t1 )) (t3 (f t2 )) (t4 (f t3 ))) (and (= t3 t2) (= t4 a) (not (= t1 a)))))
(check-sat)
(exit)
