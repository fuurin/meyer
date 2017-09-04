; General Types
(declare-datatypes (T1 T2) ((Pair (mk-pair (first T1) (second T2)))))

; Types for Meyer's Formalization
; (declare-sort U)
(declare-datatypes () ((U A B C))) ; U has 3 elements
(define-sort Set () (Array U Bool))
(define-sort Pre () (Array U Bool))
; real-pre is the intersection of set and pre.
(define-sort Post () (Array U U Bool))

(declare-datatypes () ((Prog (mk-prog (set Set) (pseudo-pre Pre) (post Post)))))
; "intersect" often does not work well.
;(define-fun pre ((p Prog)) Pre (intersect (set p) (pseudo-pre p)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Useful functions and relations

; f is a Skolem function.
;(define-fun domin ((post Post) (x U) (f (Array U U))) Bool
;  (select post x (select f x)))

; f is a Skolem function.
;(define-fun ranin ((post Post) (y U) (f (Array U U))) Bool
;  (select post (select f y) y))

(define-fun subseteq ((s1 Set) (s2 Set)) Bool
(forall ((x U)) (=> (select s1 x)
                    (select s2 x))))

(define-fun subposteq ((post1 Post) (post2 Post)) Bool
(forall ((xy (Pair U U)))
 (=> (select post1 (first xy) (second xy)) (select post2 (first xy) (second xy)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: feasibility
(define-fun isfeasible ((p Prog) (f (Array U U))) Bool
 (forall ((x U)) (=> (and (select (set p) x) (select (pseudo-pre p) x))
                     (select (post p) x (select f x)))))
; Skolemization: f is a dummy variable. add (declare-fun f () (Array U U)) when you use isfeasible function.

; p is not feasible <=> \exists x(Pre_p(x)\land (\forall y\lnot Post_p(x,y))) is true
(define-fun isnotfeasible ((p Prog)(x U)) Bool
 (and (and (select (set p) x) (select (pseudo-pre p) x)) (forall ((y U)) (not (select (post p) x y)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: program equality
(define-fun eqprog ((p1 Prog) (p2 Prog)) Bool
 (and (= (intersect (set p1) (pseudo-pre p1)) (intersect (set p2) (pseudo-pre p2)))
      (forall ((xy (Pair U U))) (=> (and (select (set p1) (first xy)) (select (pseudo-pre p1) (first xy)))
                                    (= (select (post p1) (first xy) (second xy)) (select (post p2) (first xy) (second xy)))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: refines, specifies, abstracts
(define-fun refines ((p1 Prog) (p2 Prog)) Bool ; p2 refines p1.
 (and (subseteq (set p1) (set p2))
 (and (subseteq (intersect (set p1) (pseudo-pre p1)) (intersect (set p2) (pseudo-pre p2)))
      (forall ((x (Pair U U)))
               (=> (and (select (set p1) (first x)) (select (pseudo-pre p1) (first x)))
                   (=> (select (post p2) (first x) (second x)) (select (post p1) (first x) (second x))))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Theorem: Refinement Theorem (proven) the assertions (antisymmetric and transitive) must be unsat
; P4 Refinement is an order relation.
; reflexive
;(assert (forall ((p Prog)) (refines p p)))
;; antisymmetric (naive) unlknown
;;(assert (forall ((p1 Prog)(p2 Prog)) (=> (and (refines p1 p2) (refines p2 p1)) (eqprog p1 p2))))
; antisymmetric (smt) unsat
;(declare-const p41 Prog)
;(declare-const p42 Prog)
;(assert (and (refines p41 p42) (and (refines p42 p41) (not (eqprog p41 p42)))))
; transitive (smt)  unsat
;(declare-const p11 Prog)
;(declare-const p12 Prog)
;(declare-const p13 Prog)
;(assert (and (refines p11 p12) (and (refines p12 p13) (not (refines p11 p13)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: implementation
; An implementation of p is a feasible refinement of p.
(define-fun isimplementation ((p1 Prog) (p2 Prog) (f2 (Array U U))) Bool ; p2 is an implementation of p1.
  (and (isfeasible p2 f2) (refines p2 p1)))
; Skolemization: f2 is a dummy variable. add (declare-fun f2 () (Array U U)) when you use isfeasible function.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Theorem: Implementation Thorem
; P5 A specification/program having an implementation is feasible.
; There are no p51 and p52 s.t. (p52 refines p51) and (p52,f52 is feasible) and not (p51,f51 is feasible).
;(declare-const p51 Prog)
;(declare-const p52 Prog)
;(declare-const f52 (Array U U))
;(declare-const x51 U)
;(assert (and (refines p51 p52) (and (isfeasible p52 f52) (isnotfeasible p51 x51))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; 2 Operations on specifications and programs
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; 2.1 Basic constructs

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: choice, (composition, restriction)
(define-fun choice ((p1 Prog)(p2 Prog)) Prog
 (mk-prog (union (set p1) (set p2)) (union (pseudo-pre p1) (pseudo-pre p2)) (union (post p1) (post p2))))

; Theorem: P6 For feasible operands and arbitrary conditions, the above operators yields feasible programs.
; Theorem: P61 choice case
;(define-fun isfeasibleunion ((p1 Prog) (p2 Prog) (f (Array U U))) Bool
; (forall ((x U)) (=> (or (and (select (set p1) x) (select (pseudo-pre p1) x))
;                         (and (select (set p2) x) (select (pseudo-pre p2) x)))
;                     (or (select (post p1) x (select f x))
;                         (select (post p2) x (select f x))))))
;(define-fun isnotfeasibleunion ((p1 Prog) (p2 Prog) (x U)) Bool
; (and (or (and (select (set p1) x) (select (pseudo-pre p1) x))
;          (and (select (set p2) x) (select (pseudo-pre p2) x)))
;      (forall ((y U)) (not (or (select (post p1) x y) (select (post p2) x y))))))
;(declare-const p61 Prog)
;(declare-const p62 Prog)
;(declare-const f61 (Array U U))
;(declare-const f62 (Array U U))
;(declare-const x63 U)
;(assert (and (isfeasible p61 f61) (and (isfeasible p62 f62) (isnotfeasibleunion p61 p62 x63))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: (choice,) composition(, restriction)
;(define-fun composition_rel ((x U)(y U)(p1 Prog)(p2 Prog)(u U)) Bool
; (and (select (post p2) x u) (and (select (post p1) u y) (and (select (pseudo-pre p2) y) (select (set p2) y)))))
;(define-fun IsNotFeasibleComp ((p1 Prog)(p2 Prog)(u1 U)(u4 U)) Bool
; (and (and (select (pseudo-pre p1) u1) (select (set p1) u1))
; (and (and (select (post p1) u1 u4) (and (select (pseudo-pre p2) u4) (select (set p2) u4)
; (and (forall ((u2u3 (Pair U U))) (not (and (select (post p1) u1 (first u2u3))
;                                       (and (and (select (pseudo-pre p2) (first u2u3)) (select (set p2) (first u2u3)))
;                                            (select (post p2) (first u2u3) (second u2u3))))))))))))

; Theorem: P6 For feasible operands and arbitrary conditions, the above operators yields feasible programs.
; Theorem: P62 composition case
;(declare-const p621 Prog)
;(declare-const f621 (Array U U))
;(declare-const p622 Prog)
;(declare-const f622 (Array U U))
;(declare-const u621 U)
;(declare-const u624 U)
;(assert (and (isfeasible p621 f621) (and (isfeasible p622 f622) (IsNotFeasibleComp p621 p622 u621 u624))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Definition: (choice, composition,) restriction
(define-fun restriction_rel ((x U)(y U)(p Prog)(c Set)) Bool
 (and (and (and (select (pseudo-pre p) x) (select (set p) x)) (select c x)) (select (post p) x y)))
(define-fun isnotfeasiblerest ((p Prog)(c Set)(x U)) Bool
 (and (and (select (pseudo-pre p) x) (select (set p) x))
      (forall ((y U)) (not (restriction_rel x y p c)))))

; Theorem: P6 For feasible operands and arbitrary conditions, the above operators yields feasible programs.
; Theorem: P63 restriction case
;(declare-const p631 Prog)
;(declare-const f631 (Array U U))
;(declare-const c631 Set)
;(declare-const x631 U)
;(assert (and (isfeasible p631 f631) (isnotfeasiblerest p631 c631 x631)))
; the following assertion is required, i.e. C\land pre(p) must not be empty.
;(declare-const x632 U)
;(assert (and (select c631 x632) (and (select (pseudo-pre p631) x632) (select (set p631) x632))))
; ƒIƒŠƒWƒiƒ‹‚Ì’è‹`‚É‚Í”½—á—LFƒm[ƒgŽQÆ

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Fact: a feasible program py have an infeasible refinement px of it.
;(declare-const px Prog)
;(declare-fun f0 () (Array U U))
;(assert (not (isfeasible px f0)))
;(declare-const py Prog)
;(declare-fun f1 () (Array U U))
;(assert (isfeasible py f1))
;(assert (refines px py))
;(assert (not (= px py)))

; forall (p Prog) ‚Íƒ_ƒH
;(declare-fun ff (Prog) (Array U U))
;(assert (forall ((p Prog)) (isfeasible2 p (ff p))))
;(declare-const q Prog)
;(assert (forall ((p Prog)) (= p q)))

;(declare-const post0 Post) sat
;(assert (forall ((post Post)) (subposteq post0 post)))

;(declare-const p0 Prog) ;unknown
;(assert (forall ((p1 Prog)) (implementationof p0 p1)))

(check-sat)
(get-model)
